from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.config import db



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Роль {self.name}"

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    fullname = db.Column(db.String(100), nullable=True, unique=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    hash_password = db.Column(db.String(256), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    role = db.relationship('Role', backref='users')

    @property
    def password(self):
        raise AttributeError('password is not a readably attribute!')

    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


    def __repr__(self):
        return f"Пользователь {self.username} -> Электронная почта: {self.email}"

