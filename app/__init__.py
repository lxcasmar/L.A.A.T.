from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.main import main
from app.extensions import db
import os

app = Flask(__name__)
#app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SECRET_KEY'] = '123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
with app.test_request_context():
    db.init_app(app)
    db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
from app.models import User
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

app.register_blueprint(main)