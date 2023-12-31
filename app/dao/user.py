import datetime

from app import db
from app.models import UserInfo, Department, Class, ClassDepartmentMapping, UserRole


class UpdateInfo:
    def __init__(self, cuid, uid, name, password, user_type, class_name, department_name):
        self.cuid = cuid
        self.uid = uid
        self.username = name
        self.password = password
        self.user_type = user_type
        self.class_name = class_name
        self.department_name = department_name

    def update_user_info(self):
        class_instance = Class.query.filter_by(class_name=self.class_name).first()
        if not class_instance:
            class_instance = Class(class_name=self.class_name)
            db.session.add(class_instance)
            db.session.commit()

        department_instance = Department.query.filter_by(department_name=self.department_name).first()
        if not department_instance:
            department_instance = Department(department_name=self.department_name)
            db.session.add(department_instance)
            db.session.commit()

        class_department_mapping = ClassDepartmentMapping.query.filter_by(class_id=class_instance.class_id,
                                                                          department_id=department_instance.department_id).first()
        if not class_department_mapping:
            class_department_mapping = ClassDepartmentMapping(class_id=class_instance.class_id,
                                                              department_id=department_instance.department_id)
            db.session.add(class_department_mapping)
            db.session.commit()

        user_info = UserInfo.query.filter_by(cuid=self.cuid).first()

        if not user_info:
            user_info = UserInfo(
                cuid=self.cuid,
                uid=self.uid,
                username=self.username,
                password=self.password,
                user_type=self.user_type,
                class_id=class_instance.class_id,
                department_id=department_instance.department_id
            )
            db.session.add(user_info)
        else:
            user_info.uid = self.uid
            user_info.username = self.username
            user_info.password = self.password
            user_info.user_type = self.user_type
            user_info.class_id = class_instance.class_id
            user_info.department_id = department_instance.department_id

        db.session.commit()


class UserManager:
    def __init__(self, cuid):
        self.cuid = cuid

    def get_user_info(self):
        user_info = UserInfo.query.filter_by(cuid=self.cuid).first()
        department_name = None
        if user_info:
            if user_info.department_id is not None:
                department = Department.query.get(user_info.department_id)
                department_name = department.department_name
            user_info.department_name = department_name

            class_name = None
            if user_info.class_id is not None:
                class_obj = Class.query.get(user_info.class_id)
                class_name = class_obj.class_name
            user_info.class_name = class_name

            # 数据脱敏
            user_info.password = None

        return user_info

    def get_user_role(self):
        user_roles = UserRole.query.filter(UserRole.start_date <= datetime.date.today(),
                                           UserRole.end_date >= datetime.date.today(), UserRole.cuid == self.cuid).all()
        user_role_list = [{'role': user_role.role} for user_role in user_roles]
        return user_role_list
