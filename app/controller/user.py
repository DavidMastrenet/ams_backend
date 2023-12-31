from flask import request, redirect
from flask_login import login_required, logout_user

from app.controller import user_bp
from app.auth.login import Login


@user_bp.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    cas = Login(username, password)
    return cas.login()


@user_bp.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
