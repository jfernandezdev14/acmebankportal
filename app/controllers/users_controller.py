from app.wrappers.userservice_wrapper import validate_user_wrapper


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
        :return: Dict, contains information of the user validated. Ie, {"user_id": "687548756"}
        """
        user_id = params.get('user_id', '')
        pin = params.get('pin', '')
        user = validate_user_wrapper(user_id, pin)
        workflow_log.append("User validated: {}".format(user))
        return user
