# model.py
from mongoengine import Document, StringField, BooleanField, ReferenceField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    is_admin = BooleanField(default=False)

class Album(Document):

    title = StringField(required=True)
    artist = StringField(required=True)
    available = BooleanField(default=True)

class Rental(Document):
    user = ReferenceField(User, required=True)
    album = ReferenceField(Album, required=True)
    rented_at = DateTimeField(default=datetime.utcnow)
    returned_at = DateTimeField(null=True)
