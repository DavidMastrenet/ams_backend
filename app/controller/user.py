from flask import request, redirect
from flask_login import login_required, logout_user

from app.controller import user_bp
from app.auth.login import Login


@user_bp.route('/api/login', methods=['POST'])
def login():
    """
    用户登录

    ---
    tags:
      - 认证
    parameters:
      - in: body
        name: credentials
        description: 用户登录凭据
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: 登录成功
      404:
        description: 用户名或密码错误、校园网接口请求失败
    """
    username = request.json.get('username')
    password = request.json.get('password')
    cas = Login(username, password)
    return cas.login()


@user_bp.route('/api/logout')
@login_required
def logout():
    """
    用户注销

    ---
    tags:
      - 认证
    security:
      - BearerAuth: []
    responses:
      200:
        description: 注销成功
    """
    logout_user()
    return redirect('/')
