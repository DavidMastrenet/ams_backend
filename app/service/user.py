from app.dao.user import UserManager


class UserService:
    def __init__(self, cuid):
        self.cuid = cuid
        self.user_manager = UserManager(cuid)

    def get_user_info(self):
        return self.user_manager.get_user_info()
