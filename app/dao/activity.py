from app import db
from app.models import UserInfo, UserRole, Activity, ActivityCategory, ActivityCategoryMapping, ActivityPermission, \
    GroupActivity, UserActivity, Department, Class, ClassDepartmentMapping, GroupActivityRegistration
from datetime import datetime


class ActivityManager:
    def __init__(self, cuid, activity_id):
        self.cuid = cuid
        self.activity_id = activity_id

    def check_activity_permission(self):
        # 先查询cuid和创建者是否相同
        if self.cuid == Activity.query.filter_by(activity_id=self.activity_id).first().organizer_id:
            return True
        # 是否是admin
        if UserInfo.query.filter_by(cuid=self.cuid).first().is_admin:
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
        if UserInfo.query.filter_by(cuid=self.cuid).first().is_admin:
            return True
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

        def append(activity):
            organizer_name = UserInfo.query.filter_by(cuid=activity.organizer_id).first().username

            category_list = []
            category_list_query = ActivityCategoryMapping.query.filter_by(activity_id=activity.activity_id).all()
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

            is_approved = None
            group_activity = GroupActivity.query.filter_by(activity_id=activity.activity_id).all()
            is_participate = 0
            for group in group_activity:
                if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                    is_participate = 1
                    is_approved = 1
            for user_activity in UserActivity.query.filter_by(cuid=self.cuid).all():
                if user_activity.activity_id == activity.activity_id:
                    is_participate = 1
                    if user_activity.is_approved:
                        is_approved = 1
                    else:
                        is_approved = 0

            # 检测管理权限
            can_manage = 0
            self.activity_id = activity.activity_id
            if self.check_activity_permission():
                can_manage = 1

            # 当前活动的全部参与人数
            # 班级的要算全部
            current_register = 0
            for _ in UserActivity.query.filter_by(activity_id=activity.activity_id).all():
                current_register += 1
            # 班级的
            for group in group_activity:
                for _ in UserInfo.query.filter_by(class_id=group.class_id).all():
                    current_register += 1

            # 格式化时间
            if activity.start_register is not None:
                if type(activity.start_register) is datetime:
                    activity.start_register = activity.start_register.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    activity.start_register = datetime.strptime(activity.start_register, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S')
            if activity.end_register is not None:
                if type(activity.end_register) is datetime:
                    activity.end_register = activity.end_register.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    activity.end_register = datetime.strptime(activity.end_register, '%Y-%m-%d %H:%M:%S').strftime(
                        '%Y-%m-%d %H:%M:%S')

            valid_activities.append(
                {'activity_id': activity.activity_id, 'name': activity.name, 'category_display': category_display,
                 'location': activity.location, 'time': activity.time.strftime('%Y-%m-%d %H:%M:%S'),
                 'description': activity.description,
                 'can_sign_up': activity.can_sign_up, 'can_quit': activity.can_quit, 'organizer_name': organizer_name,
                 'start_register': activity.start_register, 'end_register': activity.end_register,
                 'max_register': activity.max_register, 'category': category_list, 'is_participate': is_participate,
                 'is_approved': is_approved, 'can_manage': can_manage, 'current_register': current_register,
                 'need_approval': activity.need_approval})

        # 管理员列出全部
        if UserInfo.query.filter_by(cuid=self.cuid).first().is_admin:
            for activity in Activity.query.all():
                append(activity)
            return valid_activities

        # 列出当前用户有效的全局权限
        user_role = UserRole.query.filter_by(cuid=self.cuid).all()
        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date:
                if role.role == 'school_admin':
                    for activity in Activity.query.all():
                        append(activity)
                    return valid_activities

        # 老师直接给出所有的
        if UserInfo.query.filter_by(cuid=self.cuid).first().user_type == 'teacher':
            for activity in Activity.query.all():
                append(activity)
            return valid_activities

        department_admin = False
        department_id = UserInfo.query.filter_by(cuid=self.cuid).first().department_id

        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date and role.role == 'department_admin':
                department_admin = True

        for activity in Activity.query.all():
            for permission in ActivityPermission.query.filter_by(activity_id=activity.activity_id).all():
                if permission.cuid == int(self.cuid):
                    append(activity)
                    continue

            if department_admin:
                activity_department_id = UserInfo.query.filter_by(cuid=activity.organizer_id).first().department_id
                if department_id == activity_department_id:
                    append(activity)
                    continue

            if activity.can_sign_up == 'yes' or activity.can_sign_up == 'conditional':
                if activity.can_sign_up == 'conditional':
                    group_activity = GroupActivity.query.filter_by(activity_id=activity.activity_id).all()
                    for group in group_activity:
                        if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                            append(activity)
                            continue
                    group_activity_registration = GroupActivityRegistration.query.filter_by(
                        activity_id=activity.activity_id).all()
                    for group in group_activity_registration:
                        if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                            append(activity)
                            continue
                else:
                    append(activity)
                    continue

        valid_activities = list({activity['activity_id']: activity for activity in valid_activities}.values())

        return valid_activities

    def get_category_list(self):
        category_list = []
        category_list_query = ActivityCategory.query.all()
        for category in category_list_query:
            category_list.append({'category_id': category.category_id, 'category_name': category.category_name})
        return category_list

    def edit_activity(self, name, location, time, category, description, can_sign_up, start_register, end_register,
                      max_register, can_quit, need_approval):
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
        if can_quit is not None:
            activity.can_quit = can_quit
        if need_approval is not None:
            activity.need_approval = need_approval
        for category_id in ActivityCategoryMapping.query.filter_by(activity_id=self.activity_id).all():
            db.session.delete(category_id)
            db.session.commit()
        if category:
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

    def check_register_permission(self):
        activity = Activity.query.filter_by(activity_id=self.activity_id).first()
        # 检测是否已经参加了
        if UserActivity.query.filter_by(activity_id=self.activity_id, cuid=self.cuid).first():
            return False, "您已经参加了该活动"
        # 检测所在学院或班级是否安排了，安排了也不能参加
        group_activity = GroupActivity.query.filter_by(activity_id=activity.activity_id).all()
        for group in group_activity:
            if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                return False, "您所在的班级已经安排了该活动"
        if activity.can_sign_up == 'no':
            return False, "活动不允许报名"
        if activity.start_register and activity.end_register:
            if datetime.now() < activity.start_register or datetime.now() > activity.end_register:
                return False, "不在活动报名时间内"
        current_register = 0
        for _ in UserActivity.query.filter_by(activity_id=activity.activity_id).all():
            current_register += 1
        for group in group_activity:
            current_register += UserInfo.query.filter_by(class_id=group.class_id).count()
        if activity.max_register and current_register >= activity.max_register:
            return False, "活动报名人数已满"
        if activity.can_sign_up == 'yes':
            return True, "活动允许报名"
        if activity.can_sign_up == 'conditional':
            group_activity_registration = GroupActivityRegistration.query.filter_by(
                activity_id=activity.activity_id).all()
            for group in group_activity_registration:
                if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                    return True, "活动允许报名"
            return False, "您所在的班级不允许报名该活动"
        return False, "活动不允许报名"

    def register_activity(self):
        # 如果不用审核，就直接写is_approved
        current_task = Activity.query.filter_by(activity_id=self.activity_id).first()
        if not current_task.need_approval:
            user_activity = UserActivity(cuid=self.cuid, activity_id=self.activity_id, is_approved=True,
                                         registration_time=datetime.now())
        else:
            user_activity = UserActivity(cuid=self.cuid, activity_id=self.activity_id, is_approved=False,
                                         registration_time=datetime.now())
        db.session.add(user_activity)
        db.session.commit()
        return True, "报名成功"

    def quit_activity(self):
        # 班级安排的不允许退出
        group_activity = GroupActivity.query.filter_by(activity_id=self.activity_id).all()
        for group in group_activity:
            if group.class_id == UserInfo.query.filter_by(cuid=self.cuid).first().class_id:
                return False, "统一安排的活动不允许退出"
        # 不在报名时间内的活动不允许退出
        activity = Activity.query.filter_by(activity_id=self.activity_id).first()
        if activity.start_register and activity.end_register:
            if datetime.now() < activity.start_register or datetime.now() > activity.end_register:
                return False, "不在活动报名时间内"
        # 开始后的活动不允许退出
        if datetime.now() > activity.time:
            return False, "活动已经开始，不能退出"
        user_activity = UserActivity.query.filter_by(activity_id=self.activity_id, cuid=self.cuid).first()
        if user_activity:
            db.session.delete(user_activity)
            db.session.commit()
            return True, "退出成功"
        return False, "您还没有参加该活动"

    def get_participate_list(self):
        participate_list = []

        def append(user):
            participate_list.append({
                'cuid': user.cuid,
                'username': UserInfo.query.filter_by(cuid=user.cuid).first().username,
                'department_name': Department.query.filter_by(department_id=UserInfo.query.filter_by(
                    cuid=user.cuid).first().department_id).first().department_name,
                'class_name': Class.query.filter_by(
                    class_id=UserInfo.query.filter_by(cuid=user.cuid).first().class_id).first().class_name,
                'register_method': user.registration_method
            })

        # 活动参与情况（加载通过的），加载CUID和姓名、学院、班级的名称
        user_activity = UserActivity.query.filter_by(activity_id=self.activity_id).all()
        for user in user_activity:
            if user.is_approved:
                user.registration_method = '个人报名'
                append(user)

        # 查询学院的
        group_activity = GroupActivity.query.filter_by(activity_id=self.activity_id).all()
        for group in group_activity:
            for user in UserInfo.query.filter_by(class_id=group.class_id).all():
                user.registration_method = '班级统一安排'
                append(user)
        return participate_list

    def get_unapproved_list(self):
        unapproved_list = []

        def append(user):
            unapproved_list.append({
                'cuid': user.cuid,
                'username': UserInfo.query.filter_by(cuid=user.cuid).first().username,
                'department_name': Department.query.filter_by(department_id=UserInfo.query.filter_by(
                    cuid=user.cuid).first().department_id).first().department_name,
                'class_name': Class.query.filter_by(
                    class_id=UserInfo.query.filter_by(cuid=user.cuid).first().class_id).first().class_name,
            })

        unapproved_object = UserActivity.query.filter_by(activity_id=self.activity_id, is_approved=False).all()
        for user in unapproved_object:
            append(user)
        return unapproved_list

    def approve_activity(self, cuid):
        user_activity = UserActivity.query.filter_by(activity_id=self.activity_id, cuid=cuid).first()
        if user_activity:
            user_activity.is_approved = True
            user_activity.approved_time = datetime.now()
            db.session.commit()
            return True, "审核成功"
        return False, "审核失败"

    def get_department_class_list(self):
        department_class_list = []
        for department in Department.query.all():
            department_class_list.append({
                'label': department.department_name,
                'children': []
            })
            for class_department in ClassDepartmentMapping.query.filter_by(
                    department_id=department.department_id).all():
                department_class_list[-1]['children'].append({
                    'label': Class.query.filter_by(class_id=class_department.class_id).first().class_name,
                    'value': class_department.class_id
                })
        return department_class_list

    def get_activity_group_list(self):
        group_activity = GroupActivity.query.filter_by(activity_id=self.activity_id).all()
        # 返回值{"class":"1,2"}，是个json
        return {
            'class': ','.join([str(group.class_id) for group in group_activity])
        }

    def add_group_activity(self, classes):
        # 先删去所有的安排并提交
        group_activity = GroupActivity.query.filter_by(activity_id=self.activity_id).all()
        for group in group_activity:
            db.session.delete(group)
        db.session.commit()

        if classes:
            class_id = [int(class_id) for class_id in classes.split(',')]
        else:
            class_id = []

        for class_id in class_id:
            group_activity = GroupActivity(class_id=class_id, activity_id=self.activity_id)
            db.session.add(group_activity)

            # 如果个人报名过，要删掉
            for user in UserInfo.query.filter_by(class_id=class_id).all():
                user_activity = UserActivity.query.filter_by(activity_id=self.activity_id, cuid=user.cuid).first()
                if user_activity:
                    db.session.delete(user_activity)

        db.session.commit()
        return True, "添加成功"

    def add_register_condition(self, classes):
        # 先删去所有的条件并提交
        register_condition = GroupActivityRegistration.query.filter_by(activity_id=self.activity_id).all()
        for group in register_condition:
            db.session.delete(group)
        db.session.commit()

        if classes:
            class_id = [int(class_id) for class_id in classes.split(',')]
        else:
            class_id = []

        for class_id in class_id:
            group_activity = GroupActivityRegistration(class_id=class_id, activity_id=self.activity_id)
            db.session.add(group_activity)

        db.session.commit()
        return True, "添加成功"

    def get_activity_condition(self):
        condition_list = {"class" : ""}
        for group in GroupActivityRegistration.query.filter_by(activity_id=self.activity_id).all():
            if condition_list["class"]:
                condition_list["class"] += "," + str(group.class_id)
            else:
                condition_list["class"] = str(group.class_id)
        return condition_list

    def get_group_activity_list(self):
        group_activity_list = {"class" : ""}
        for group in GroupActivity.query.filter_by(activity_id=self.activity_id).all():
            if group_activity_list["class"]:
                group_activity_list["class"] += "," + str(group.class_id)
            else:
                group_activity_list["class"] = str(group.class_id)
        return group_activity_list
