from app.utilities.exceptions.exceptions import HttpUnauthorized, HttpNotFound


class ApiException(Exception):
    def __init__(self, message='', status_code=500):
        self.description = message
        self.code = status_code

