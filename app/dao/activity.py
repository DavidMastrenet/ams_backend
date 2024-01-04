from app import db
from app.models import UserInfo, UserRole, Activity, ActivityCategory, ActivityCategoryMapping, ActivityPermission, \
    GroupActivity
from datetime import datetime


class ActivityManager:
    def __init__(self, cuid, activity_id):
        self.cuid = cuid
        self.activity_id = activity_id

    def check_activity_permission(self):
        # 先查询cuid和创建者是否相同
        if self.cuid == Activity.query.filter_by(activity_id=self.activity_id).first().organizer_id:
            return True
        # 列出当前用户有效的全局权限
        user_role = UserRole.query.filter_by(cuid=self.cuid).all()
        # 注意UserRole的有效期start_date和end_date
        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date:
                if role.role == 'school_admin':
                    return True
                elif role.role == 'department_admin':
                    organizer_department = UserInfo.query.filter_by(cuid=Activity.organizer_id).first().department_id
                    if organizer_department == role.department_id:
                        return True

        activity_permission = ActivityPermission.query.filter_by(cuid=self.cuid, activity_id=self.activity_id).first()
        if activity_permission is None:
            return False
        else:
            return True

    def check_create_activity_permission(self):
        # 检查是否是老师
        if UserInfo.query.filter_by(cuid=self.cuid).first().user_type == 'teacher':
            return True
        # 列出当前用户有效的全局权限
        user_role = UserRole.query.filter_by(cuid=self.cuid).all()
        # 注意UserRole的有效期start_date和end_date
        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date:
                if role.role == 'school_admin':
                    return True
                elif role.role == 'department_admin':
                    return True
                elif role.role == 'create_activity':
                    return True
                return False
        return False

    def create_activity(self, name, time, location, can_sign_up, organizer_id):
        activity = Activity(name=name, time=time, location=location, can_sign_up=can_sign_up, organizer_id=organizer_id)
        db.session.add(activity)
        db.session.commit()
        return activity

    def get_valid_activity(self):
        valid_activities = []

        def append():
            organizer_name = UserInfo.query.filter_by(cuid=Activity.organizer_id).first().username
            category_list = []
            category_list_query = ActivityCategoryMapping.query.filter_by(activity_id=Activity.activity_id).all()
            if category_list_query is None:
                category_list.append('未分类')
            else:
                for category in category_list_query:
                    category_list.append({'category_id': category.category_id,
                                          'category_name': ActivityCategory.query.filter_by(
                                              category_id=category.category_id).first().category_name})
            category_display = []
            for category in category_list:
                category_display.append(category['category_name'])
            valid_activities.append(
                {'activity_id': activity.activity_id, 'name': activity.name, 'category_display': category_display,
                 'location': activity.location, 'time': activity.time.strftime('%Y-%m-%d %H:%M:%S'),
                 'description': activity.description,
                 'can_sign_up': activity.can_sign_up, 'can_quit': activity.can_quit, 'organizer_name': organizer_name,
                 'start_register': activity.start_register, 'end_register': activity.end_register,
                 'max_register': activity.max_register, 'category': category_list})

        # 列出当前用户有效的全局权限
        user_role = UserRole.query.filter_by(cuid=self.cuid).all()
        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date:
                if role.role == 'school_admin':
                    for activity in Activity.query.all():
                        append()
                    return valid_activities

        # 老师直接给出所有的
        if UserInfo.query.filter_by(cuid=self.cuid).first().user_type == 'teacher':
            for activity in Activity.query.all():
                append()
            return valid_activities

        department_admin = False
        department_id = UserInfo.query.filter_by(cuid=self.cuid).first().department_id

        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date and role.role == 'department_admin':
                department_admin = True

        for activity in Activity.query.all():

            if department_admin:
                activity_department_id = UserInfo.query.filter_by(cuid=activity.organizer_id).first().department_id
                if department_id == activity_department_id:
                    append()

            if activity.can_sign_up == 'yes' or activity.can_sign_up == 'conditional':
                if activity.can_sign_up == 'conditional':
                    group_activity = GroupActivity.query.filter_by(activity_id=activity.activity_id).all()
                    for group in group_activity:
                        if (group.department_id == UserInfo.query.filter_by(cuid=self.cuid).first().department_id or
                                group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id):
                            append()
                else:
                    append()

        return valid_activities

    def get_category_list(self):
        category_list = []
        category_list_query = ActivityCategory.query.all()
        for category in category_list_query:
            category_list.append({'category_id': category.category_id, 'category_name': category.category_name})
        return category_list

    def edit_activity(self, name, location, time, category, description, can_sign_up, start_register, end_register,
                      max_register, can_quit):
        activity = Activity.query.filter_by(activity_id=self.activity_id).first()
        # 空的不传，利用model遍历
        if name:
            activity.name = name
        if location:
            activity.location = location
        if time:
            activity.time = time
        if description:
            activity.description = description
        if can_sign_up:
            activity.can_sign_up = can_sign_up
        if start_register:
            activity.start_register = start_register
        if end_register:
            activity.end_register = end_register
        if max_register:
            activity.max_register = max_register
        if can_quit:
            activity.can_quit = can_quit
        for category_id in ActivityCategoryMapping.query.filter_by(activity_id=self.activity_id).all():
            db.session.delete(category_id)
            db.session.commit()
        if not isinstance(category, list):
            for category_id in category.split(','):
                category_id = int(category_id)
                category_mapping = ActivityCategoryMapping(activity_id=self.activity_id, category_id=category_id)
                db.session.add(category_mapping)
        else:
            for category_id in category:
                category_id = int(category_id['category_id'])
                category_mapping = ActivityCategoryMapping(activity_id=self.activity_id, category_id=category_id)
                db.session.add(category_mapping)
        db.session.commit()
        return activity
