from app import db


class Class(db.Model):
    __tablename__ = 'class'
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(255), nullable=False)


class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(255), nullable=False)


class ClassDepartmentMapping(db.Model):
    __tablename__ = 'class_department_mapping'
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'), primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    cuid = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.Enum('teacher', 'student'), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    last_update = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class UserRole(db.Model):
    __tablename__ = 'user_role'
    user_role_id = db.Column(db.Integer, primary_key=True)
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    role = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    auth_by = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))


class Activity(db.Model):
    __tablename__ = 'activity'
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    can_sign_up = db.Column(db.Enum('no', 'yes', 'conditional'), nullable=False)
    need_approval = db.Column(db.Boolean, default=False)
    start_register = db.Column(db.DateTime)
    end_register = db.Column(db.DateTime)
    max_register = db.Column(db.Integer)
    can_quit = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)
    organizer_id = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))


class ActivityPermission(db.Model):
    __tablename__ = 'activity_permission'
    permission_id = db.Column(db.Integer, primary_key=True)
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))


class GroupActivity(db.Model):
    __tablename__ = 'group_activity'
    activity_participation_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'))


class GroupActivityRegistration(db.Model):
    __tablename__ = 'group_activity_registration'
    registration_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'))


class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    user_activity_id = db.Column(db.Integer, primary_key=True)
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    is_approved = db.Column(db.Boolean, default=False)
    registration_time = db.Column(db.DateTime, nullable=False)
    approved_time = db.Column(db.DateTime)


class CheckInMethod(db.Model):
    __tablename__ = 'check_in_method'
    method_id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(255), nullable=False)


class CheckIn(db.Model):
    __tablename__ = 'check_in'
    check_in_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    method_id = db.Column(db.Integer, db.ForeignKey('check_in_method.method_id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class CheckInRecord(db.Model):
    __tablename__ = 'check_in_record'
    check_in_record_id = db.Column(db.Integer, primary_key=True)
    check_in_id = db.Column(db.Integer, db.ForeignKey('check_in.check_in_id'))
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    check_in_time = db.Column(db.DateTime, nullable=False)


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    content = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime, nullable=False)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    satisfaction_level = db.Column(db.Integer)
    suggestions = db.Column(db.Text)
    feedback_time = db.Column(db.DateTime, nullable=False)


class Notification(db.Model):
    __tablename__ = 'notification'
    notification_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    message = db.Column(db.Text, nullable=False)
    notification_time = db.Column(db.DateTime, nullable=False)


class ActivityCategory(db.Model):
    __tablename__ = 'activity_category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)


class ActivityCategoryMapping(db.Model):
    __tablename__ = 'activity_category_mapping'
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('activity_category.category_id'), primary_key=True)


class FinancialTransaction(db.Model):
    __tablename__ = 'financial_transaction'
    transaction_id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))
    cuid = db.Column(db.Integer, db.ForeignKey('user_info.cuid'))
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_time = db.Column(db.DateTime, nullable=False)
