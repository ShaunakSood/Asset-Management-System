from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(128), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
