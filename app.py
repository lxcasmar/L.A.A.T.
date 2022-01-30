from app import app
# from flask import Flask
# from flask_login import LoginManager
# from models import User, db
# from main import main
# import os

# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#     db.init_app(app)
#     login_manager = LoginManager()
#     login_manager.init_app(app)
    
#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))
    
#     app.register_blueprint(main)
    
#     return app

# app = create_app()

# use escape() there are no scripts being run
# ex escape(name)