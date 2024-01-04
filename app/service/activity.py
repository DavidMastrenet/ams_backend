from app.dao.activity import ActivityManager


class ActivityService:
    def __init__(self, cuid):
        self.activity_manager = None
        self.activity_id = 0
        self.cuid = cuid

    def get_activity_permission(self, activity_id):
        self.activity_id = activity_id
        self.activity_manager = ActivityManager(self.cuid, self.activity_id)
        return self.activity_manager.check_activity_permission()

    def get_create_activity_permission(self):
        self.activity_manager = ActivityManager(self.cuid, self.activity_id)
        return self.activity_manager.check_create_activity_permission()

    def create_activity(self, name, time, location, can_sign_up, organizer_id):
        self.activity_manager = ActivityManager(self.cuid, self.activity_id)
        return self.activity_manager.create_activity(name, time, location, can_sign_up, organizer_id)

    def get_valid_activity(self):
        self.activity_manager = ActivityManager(self.cuid, self.activity_id)
        return self.activity_manager.get_valid_activity()

    def get_activity_info(self, activity_id):
        self.activity_id = activity_id
        self.activity_manager = ActivityManager(self.cuid, self.activity_id)
        return self.activity_manager.get_activity_info(self.activity_id)
