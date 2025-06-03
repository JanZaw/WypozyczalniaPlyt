from mongoengine import Document, StringField, BooleanField, ReferenceField, DateTimeField, IntField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    user_id = StringField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)

class Album(Document):
    album_id = StringField(required=True, unique=True)
    title = StringField(required=True)
    artist = StringField(required=True)
    DateOfProduction = DateTimeField(required=True)
    Sells = IntField(default=0)
    available = BooleanField(default=True)

class Rental(Document):
    user = ReferenceField(User, required=True)
    album = ReferenceField(Album, required=True)
    user_id = StringField(required=True)
    album_id = StringField(required=True)
    rented_at = DateTimeField(default=datetime.utcnow)
    returned_at = DateTimeField(null=True)