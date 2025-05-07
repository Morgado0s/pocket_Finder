from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admin'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

def create_admin(name, email, password):
    admin = Admin(name=name, email=email, password=password)
    db.session.add(admin)
    db.session.commit()
    return admin

def get_admin(admin_id):
    return Admin.query.get(admin_id)

def get_admin_by_email(email):
    return Admin.query.filter_by(email=email).first()

def update_admin(admin_id, data):
    admin = get_admin(admin_id)
    if admin:
        if 'name' in data:
            admin.name = data['name']
        if 'email' in data:
            admin.email = data['email']
        if 'password' in data:
            admin.password = generate_password_hash(data['password'])
        db.session.commit()
    return admin

def delete_admin(admin_id):
    admin = get_admin(admin_id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        return True
    return False 