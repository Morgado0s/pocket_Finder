from extensions import db
from datetime import datetime

class Size(db.Model):
    __tablename__ = 'size'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "abbreviation": self.abbreviation
        }

def create_size(name, abbreviation):
    size = Size(name=name, abbreviation=abbreviation)
    db.session.add(size)
    db.session.commit()
    return size

def get_size(size_id):
    return Size.query.get(size_id)

def update_size(size_id, data):
    size = get_size(size_id)
    if size:
        if 'name' in data:
            size.name = data['name']
        if 'abbreviation' in data:
            size.abbreviation = data['abbreviation']
        db.session.commit()
    return size

def delete_size(size_id):
    size = get_size(size_id)
    if size:
        db.session.delete(size)
        db.session.commit()
        return True
    return False 