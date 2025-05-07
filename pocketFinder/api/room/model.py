from extensions import db
from datetime import datetime
import pytz
from typing import Dict, Optional

class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shift = db.Column(db.String(20), nullable=False)  # manhã, tarde, noite
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Room {self.id}, Name: {self.name}, Shift: {self.shift}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'shift': self.shift,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "shift": self.shift
        }

def create_room(name, shift):
    room = Room(name=name, shift=shift)
    db.session.add(room)
    db.session.commit()
    return room

def get_room(room_id):
    return Room.query.get(room_id)

def update_room(room_id, data):
    room = get_room(room_id)
    if room:
        if 'name' in data:
            room.name = data['name']
        if 'shift' in data:
            room.shift = data['shift']
        db.session.commit()
    return room

def delete_room(room_id):
    room = get_room(room_id)
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    return False 