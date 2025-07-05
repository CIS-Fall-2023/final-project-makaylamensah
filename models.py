# backend/models.py
from database import db

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)

class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
