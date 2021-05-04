from app.wrappers.userservice_wrapper import validate_user_wrapper


class User(object):
    def __init__(self, user_id=None, pin=None):
        self.user_id = user_id
        self.pin = pin
        self.is_valid = False


class UsersController(object):
    """
    Contains the logic related to the account functionalities
    """

    @staticmethod
    def validate_user(params, workflow_log=[]):
        """
        Validates if the user data received matches with an existing user
        :param params: Dict, contains the information of the user to validate. Ie, {"user_id": "8754096", "pin": 7845}
        :param workflow_log: List, contains the history of the workflow. Ie, ["Transaction 1", ...]
        :return: Bool, if the information of the user is valid True ,otherwise an exception is raised. Ie, True
        """
        user_id = params.get('user_id', '')
        pin = params.get('pin', '')
        response = validate_user_wrapper(user_id, pin)
        is_valid = response.get('is_valid', False)
        workflow_log.append("User {}: Validation {}".format(user_id, 'success' if is_valid else 'failed'))
        return is_valid
