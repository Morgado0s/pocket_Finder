from extensions import db
from datetime import datetime
import pytz
from typing import Dict, Optional

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    # Relacionamentos
    category = db.relationship('Category', foreign_keys=[category_id])
    size = db.relationship('Size', foreign_keys=[size_id])
    gender = db.relationship('Gender', foreign_keys=[gender_id])
    room = db.relationship('Room', foreign_keys=[room_id])

    def __repr__(self):
        return f"<Product {self.id}, Name: {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'size_id': self.size_id,
            'gender_id': self.gender_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'room_id': self.room_id
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "size_id": self.size_id,
            "gender_id": self.gender_id,
            "room_id": self.room_id
        }

def create_product(name, description, category_id, size_id, gender_id, room_id):
    product = Product(
        name=name,
        description=description,
        category_id=category_id,
        size_id=size_id,
        gender_id=gender_id,
        room_id=room_id
    )
    db.session.add(product)
    db.session.commit()
    return product

def get_product(product_id):
    return Product.query.get(product_id)

def update_product(product_id, data):
    product = get_product(product_id)
    if product:
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category_id' in data:
            product.category_id = data['category_id']
        if 'size_id' in data:
            product.size_id = data['size_id']
        if 'gender_id' in data:
            product.gender_id = data['gender_id']
        if 'room_id' in data:
            product.room_id = data['room_id']
        db.session.commit()
    return product

def delete_product(product_id):
    product = get_product(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False 