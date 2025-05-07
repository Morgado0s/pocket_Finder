from extensions import db
from datetime import datetime
import pytz
from typing import Dict, Optional

class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    product = db.relationship('Product', foreign_keys=[product_id])
    room = db.relationship('Room', foreign_keys=[room_id])
    admin = db.relationship('Admin', foreign_keys=[admin_id])

    def __repr__(self):
        return f"<Student {self.id}, Name: {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'product_id': self.product_id,
            'room_id': self.room_id,
            'admin_id': self.admin_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "product_id": self.product_id,
            "room_id": self.room_id,
            "admin_id": self.admin_id
        }

def create_student(name, product_id, room_id, admin_id):
    student = Student(
        name=name,
        product_id=product_id,
        room_id=room_id,
        admin_id=admin_id
    )
    db.session.add(student)
    db.session.commit()
    return student

def get_student(student_id):
    return Student.query.get(student_id)

def update_student(student_id, data):
    student = get_student(student_id)
    if student:
        if 'name' in data:
            student.name = data['name']
        if 'product_id' in data:
            student.product_id = data['product_id']
        if 'room_id' in data:
            student.room_id = data['room_id']
        if 'admin_id' in data:
            student.admin_id = data['admin_id']
        db.session.commit()
    return student

def delete_student(student_id):
    student = get_student(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return True
    return False 