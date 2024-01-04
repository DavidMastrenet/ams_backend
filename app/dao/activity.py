from app import db
from app.models import UserInfo, UserRole, Activity, ActivityCategory, ActivityCategoryMapping, ActivityPermission
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
        # 列出当前用户有效的全局权限
        user_role = UserRole.query.filter_by(cuid=self.cuid).all()
        # 注意UserRole的有效期start_date和end_date
        for role in user_role:
            if role.start_date <= datetime.now().date() <= role.end_date:
                if role.role =='school_admin':
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

