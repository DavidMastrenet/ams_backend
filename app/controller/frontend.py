from flask import render_template, redirect
from flask_login import current_user, login_required

import app.config
from app.controller import fe_bp

from app.service.user import UserService


@fe_bp.route('/')
@login_required
def index():
    user = UserService(current_user.id)
    user = user.get_user_info()
    return render_template('index.html', env_name=app.config.ENV_NAME, username=user.username, user_type=user.user_type,
                           department_name=user.department_name, class_name=user.class_name)


@fe_bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect('/')
    return render_template('login.html', env_name=app.config.ENV_NAME)


@fe_bp.route('/create_activity')
@login_required
def create_activity():
    return render_template('create_activity.html', env_name=app.config.ENV_NAME)


@fe_bp.route('/list_activity')
@login_required
def list_activity():
    user = UserService(current_user.id)
    user = user.get_user_info()
    return render_template('list_activity.html', env_name=app.config.ENV_NAME, username=user.username)
