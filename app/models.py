from flask_login import UserMixin
from app.extensions import db

class User(UserMixin, db.Model):
    
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    portfolio = db.Column(db.String, default='')
    active = db.Column(db.String, default='')
    #historical = db.Column(db.String, default='')
    indicators = db.Column(db.String, default='')
