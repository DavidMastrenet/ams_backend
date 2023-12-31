from flask import Blueprint

fe_bp = Blueprint('fe', __name__)
user_bp = Blueprint('user', __name__)
activity_bp = Blueprint('activity', __name__)

from . import frontend, user, activity
