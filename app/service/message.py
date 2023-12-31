class MessageService:

    def send_message(self, msg):
        return {'msg': msg}

    def send_error_message(self, msg):
        return {'msg': msg}, 404

    def send_unauthorized_message(self, msg):
        return {'msg': msg}, 401
