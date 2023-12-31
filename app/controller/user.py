from flask import request, redirect, jsonify
from flask_login import login_required, logout_user

from app.controller import user_bp
from app.auth.login import Login

from app.dao.user import UserManager

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

@user_bp.route('/api/role', methods=['GET'])
def get_role():
    user_manager = UserManager("1000555508")
    return user_manager.get_user_role()