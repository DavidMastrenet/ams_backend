from flask import request, jsonify
from flask_login import login_required, current_user

from app.controller import activity_bp

from app.service.activity import ActivityService
from app.service.message import MessageService

message_service = MessageService()


@activity_bp.route('/api/activity/list', methods=['GET'])
@login_required
def get_activity_list():
    """
    获取活动列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动列表
    """
    activity_service = ActivityService(current_user.id)
    activity_list = activity_service.get_valid_activity()
    return jsonify(activity_list)


@activity_bp.route('/api/activity/create', methods=['POST'])
@login_required
def create_activity():
    """
    创建活动

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: info
        description: 活动信息
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            time:
              type: string
            location:
              type: string
            can_sign_up:
              type: integer
    responses:
      200:
        description: 活动创建成功
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.get_create_activity_permission():
        return message_service.send_unauthorized_message('无权限创建活动')
    name = request.json.get('name')
    time = request.json.get('time')
    location = request.json.get('location')
    can_sign_up = request.json.get('can_sign_up')
    organizer_id = current_user.id
    activity_service.create_activity(name, time, location, can_sign_up, organizer_id)
    return message_service.send_message('活动创建成功')


@activity_bp.route('/api/activity/category', methods=['GET'])
@login_required
def get_category_list():
    """
    获取活动分类列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动分类列表
    """
    activity_service = ActivityService(current_user.id)
    category_list = activity_service.get_category_list()
    return jsonify(category_list)


@activity_bp.route('/api/activity/edit/<activity_id>', methods=['POST'])
@login_required
def edit_activity(activity_id):
    """
    修改活动信息

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: info
        description: 活动信息
    responses:
      200:
        description: 活动修改成功
      401:
        description: 无权限修改活动
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.get_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限修改活动')
    name = request.json.get('name')
    location = request.json.get('location')
    time = request.json.get('time')
    category = request.json.get('category')
    description = request.json.get('description')
    can_sign_up = request.json.get('can_sign_up')
    start_register = request.json.get('start_register')
    end_register = request.json.get('end_register')
    max_register = request.json.get('max_register')
    can_quit = request.json.get('can_quit')
    need_approval = request.json.get('need_approval')
    activity_service.edit_activity(activity_id, name, location, time, category, description, can_sign_up, start_register,
                                   end_register, max_register, can_quit, need_approval)
    return message_service.send_message('活动修改成功')


@activity_bp.route('/api/activity/register/<activity_id>', methods=['GET'])
@login_required
def register_activity(activity_id):
    """
    报名活动

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动报名成功
      404:
        description: 无法报名活动
    """
    activity_service = ActivityService(current_user.id)
    status, msg = activity_service.register_activity(activity_id)
    if not status:
        return message_service.send_error_message(msg)
    return message_service.send_message(msg)


@activity_bp.route('/api/activity/quit/<activity_id>', methods=['GET'])
@login_required
def quit_activity(activity_id):
    """
    退出活动

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动退出成功
      404:
        description: 无法退出活动
    """
    activity_service = ActivityService(current_user.id)
    status, msg = activity_service.quit_activity(activity_id)
    if not status:
        return message_service.send_error_message(msg)
    return message_service.send_message(msg)
