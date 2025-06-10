from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from mongoengine import connect
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import timedelta
import jwt
from model import *

SECRET = "SECRET_KEY"

connect(db="music_rental", host="mongodb://mongodb:27017/music_rental")

app = FastAPI()
active_connections: Dict[str, WebSocket] = {}

class UserRequest(BaseModel):
    username: str
    password: str

class AlbumResponse(BaseModel):
    id: str
    title: str
    artist: str
    available: bool

class RentalResponse(BaseModel):
    album_title: str
    artist: str
    rented_at: datetime
    returned_at: Optional[datetime]

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token: str):
    username = verify_token(token)
    user = User.objects(username=username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.post("/register")
def register(data: UserRequest):
    if User.objects(username=data.username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    User(username=data.username, password=data.password).save()
    return {"msg": "User registered"}

@app.post("/login")
def login(data: UserRequest):
    user = User.objects(username=data.username).first()
    if not user or user.password != data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"token": token}

@app.post("/admin/add_album")
def add_album(title: str, artist: str, token: str):
    user = get_current_user(token)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin")
    Album(title=title, artist=artist).save()
    return {"msg": "Album added"}

@app.delete("/admin/remove_album/{album_id}")
def remove_album(album_id: str, token: str):
    user = get_current_user(token)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not an admin")
    album = Album.objects(id=album_id).first()
    if album:
        album.delete()
        return {"msg": "Album deleted"}
    raise HTTPException(status_code=404, detail="Album not found")

@app.get("/albums")
def list_albums(artist: Optional[str] = None):
    albums = Album.objects(artist=artist) if artist else Album.objects()
    return [{"id": str(album.id), "title": album.title, "artist": album.artist, "available": album.available} for album in albums]

@app.post("/rent/{album_id}")
def rent_album(album_id: str, token: str):
    user = get_current_user(token)
    album = Album.objects(id=album_id, available=True).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album unavailable or not found")
    Rental(user=user, album=album).save()
    album.available = False
    album.save()
    return {"msg": "Album rented"}

@app.post("/return/{album_id}")
def return_album(album_id: str, token: str):
    user = get_current_user(token)
    rental = Rental.objects(user=user, album=album_id, returned_at=None).first()
    if not rental:
        raise HTTPException(status_code=404, detail="No such rental found")
    rental.returned_at = datetime.utcnow()
    rental.save()
    album = rental.album
    album.available = True
    album.save()
    return {"msg": "Album returned"}

@app.get("/history")
def rental_history(token: str):
    user = get_current_user(token)
    rentals = Rental.objects(user=user)
    return [{"album_title": rental.album.title, "artist": rental.album.artist, "rented_at": rental.rented_at, "returned_at": rental.returned_at} for rental in rentals]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Music Rental API"}

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        username = verify_token(token)
    except HTTPException:
        await websocket.close()
        return
    await websocket.accept()
    active_connections[username] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.pop(username, None)
