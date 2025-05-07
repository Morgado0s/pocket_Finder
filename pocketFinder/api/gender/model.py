from extensions import db
from datetime import datetime

class Gender(db.Model):
    __tablename__ = 'gender'
    
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

def create_gender(name, abbreviation):
    gender = Gender(name=name, abbreviation=abbreviation)
    db.session.add(gender)
    db.session.commit()
    return gender

def get_gender(gender_id):
    return Gender.query.get(gender_id)

def update_gender(gender_id, data):
    gender = get_gender(gender_id)
    if gender:
        if 'name' in data:
            gender.name = data['name']
        if 'abbreviation' in data:
            gender.abbreviation = data['abbreviation']
        db.session.commit()
    return gender

def delete_gender(gender_id):
    gender = get_gender(gender_id)
    if gender:
        db.session.delete(gender)
        db.session.commit()
        return True
    return False 