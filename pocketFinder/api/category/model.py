from extensions import db
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }

def create_category(name, code):
    category = Category(name=name, code=code)
    db.session.add(category)
    db.session.commit()
    return category

def get_category(category_id):
    return Category.query.get(category_id)

def update_category(category_id, data):
    category = get_category(category_id)
    if category:
        if 'name' in data:
            category.name = data['name']
        if 'code' in data:
            category.code = data['code']
        db.session.commit()
    return category

def delete_category(category_id):
    category = get_category(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
        return True
    return False 