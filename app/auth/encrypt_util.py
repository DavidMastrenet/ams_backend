import hashlib

import app.config


class Encryptor:
    def __init__(self, algorithm='sha256'):
        self.algorithm = algorithm
        self.salt = app.config.SALT

    def hash_password(self, password):

        if isinstance(self.salt, str):
            self.salt = self.salt.encode('utf-8')

        if isinstance(password, str):
            password = password.encode('utf-8')

        hashed_password = hashlib.new(self.algorithm)
        hashed_password.update(self.salt)
        hashed_password.update(password)

        return hashed_password.hexdigest()

    def verify_password(self, password, stored_hash):
        if isinstance(self.salt, str):
            self.salt = self.salt.encode('utf-8')

        if isinstance(password, str):
            password = password.encode('utf-8')

        hashed_password = hashlib.new(self.algorithm)
        hashed_password.update(self.salt)
        hashed_password.update(password)

        return hashed_password.hexdigest() == stored_hash
