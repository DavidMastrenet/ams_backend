from flask import request
from flask_login import login_required, current_user

from app.controller import activity_bp

from app.service.activity import ActivityService
from app.service.message import MessageService

message_service = MessageService()


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
