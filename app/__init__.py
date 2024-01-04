from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


from app import models


@login_manager.user_loader
def load_user(id):
    return User(id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


from app.controller import fe_bp
from app.controller import user_bp
from app.controller import activity_bp

from app.controller import frontend
from app.controller import user
from app.controller import activity

app.register_blueprint(fe_bp)
app.register_blueprint(user_bp)
app.register_blueprint(activity_bp)
