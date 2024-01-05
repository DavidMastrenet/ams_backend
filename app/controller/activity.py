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


@activity_bp.route('/api/activity/participate/<activity_id>', methods=['GET'])
@login_required
def get_participate_list(activity_id):
    """
    获取活动参与者列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动参与者列表
      401:
        description: 无权限查看活动
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限查看活动')
    activity_service = ActivityService(current_user.id)
    participate_list = activity_service.get_participate_list(activity_id)
    return jsonify(participate_list)

@activity_bp.route('/api/activity/unapproved/<activity_id>', methods=['GET'])
@login_required
def get_unapproved_list(activity_id):
    """
    获取未审核的名单

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动未审核列表
      401:
        description: 无权限查看活动
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限查看活动')
    unapproved_list = activity_service.get_unapproved_list(activity_id)
    return jsonify(unapproved_list)


@activity_bp.route('/api/activity/approve/<activity_id>', methods=['POST'])
@login_required
def approve_activity(activity_id):
    """
    审核活动

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动审核成功
      401:
        description: 无权限审核活动
    """
    activity_service = ActivityService(current_user.id)
    cuid = request.json.get('cuid')
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限审核活动')
    status, msg = activity_service.approve_activity(activity_id, cuid)
    if not status:
        return message_service.send_error_message(msg)
    return message_service.send_message(msg)

@activity_bp.route('/api/activity/class', methods=['GET'])
@login_required
def get_department_class_list():
    """
    获取学院和班级列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 学院和班级列表
    """
    activity_service = ActivityService(current_user.id)
    department_class_list = activity_service.get_department_class_list()
    return jsonify(department_class_list)

@activity_bp.route('/api/activity/list_group/<activity_id>', methods=['GET'])
@login_required
def get_activity_group_list(activity_id):
    """
    获取活动安排班级列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动组列表
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限查看活动')
    activity_group_list = activity_service.get_activity_group_list(activity_id)
    return jsonify(activity_group_list)


@activity_bp.route('/api/activity/add_group/<activity_id>', methods=['POST'])
@login_required
def add_activity_group(activity_id):
    """
    修改活动组

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动组修改成功
      401:
        description: 无权限修改活动组
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限修改活动组')
    classes = request.json.get('class')
    activity_service.add_activity_group(activity_id, classes)
    return message_service.send_message('活动组修改成功')


@activity_bp.route('/api/activity/add_condition/<activity_id>', methods=['POST'])
@login_required
def add_register_condition(activity_id):
    """
    修改活动报名条件

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动报名条件修改成功
      401:
        description: 无权限修改活动报名条件
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限修改活动报名条件')
    classes = request.json.get('class')
    activity_service.add_register_condition(activity_id, classes)
    return message_service.send_message('活动报名条件修改成功')


@activity_bp.route('/api/activity/condition/<activity_id>', methods=['GET'])
@login_required
def get_activity_condition(activity_id):
    """
    获取活动报名条件

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动报名条件
      401:
        description: 无权限查看活动报名条件
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限查看活动报名条件')
    activity_condition = activity_service.get_activity_condition(activity_id)
    return jsonify(activity_condition)


@activity_bp.route('/api/activity/group_list/<activity_id>', methods=['GET'])
@login_required
def get_group_activity_list(activity_id):
    """
    获取活动组列表

    ---
    tags:
      - 活动
    security:
      - BearerAuth: []
    responses:
      200:
        description: 活动组列表
      401:
        description: 无权限查看活动组列表
    """
    activity_service = ActivityService(current_user.id)
    if not activity_service.check_activity_permission(activity_id):
        return message_service.send_unauthorized_message('无权限查看活动组列表')
    group_activity_list = activity_service.get_group_activity_list(activity_id)
    return jsonify(group_activity_list)
