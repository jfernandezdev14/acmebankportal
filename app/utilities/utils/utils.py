import json
from flask import Response

from app.utilities.exceptions.acmebank_exceptions import ApiException


def json_response(data, status=200):
    """
    Prepare data and make the response
    :param data: dict, contains the data that is going in he response
    :param status: integer, code status. Ie, 200
    :return: Response, the response object to return
    """

    data_as_str = json.JSONEncoder().encode(data)
    return Response(response=data_as_str, status=status, mimetype='application/json')


def deserialize_and_verify_json_response(response):
    """
    Verifies if the json response of an API contains errors
    :param response: requests HTTP response object
    :return: Dic, deserialized data. Ie, {'data': 1}
    """

    if response.status_code != 200:
        raise ApiException(response.text, status_code=response.status_code)

    return json.loads(response.text)


class ConditionValidator:
    """
    Condition validator
    """
    def __init__(self, obj):
        self.object = obj

    def validate(self, operator, field_id, value):
        return getattr(self, str(operator))(field_id, value)

    def eq(self, field_id, value):
        """
        Operator - equal
        """
        return self.object.__getattribute__(field_id) == value

    def gt(self, field_id, value):
        """
        Operator - greater than
        """
        return self.object.__getattribute__(field_id) > value

    def gte(self, field_id, value):
        """
        Operator - Greater than or equal
        """
        return self.object.__getattribute__(field_id) >= value

    def lt(self, field_id, value):
        """
        Operator - Lower than
        """
        return self.object.__getattribute__(field_id) < value

    def lte(self, field_id, value):
        """
        Operator - Lower than or equal
        """
        return self.object.__getattribute__(field_id) <= value


def get_cop_exchange_rate():
    """
    Returns the current day TRM
    :return: float, the day trm
    """
    # TODO: There aren't free libraries that supports exchange rates conversion for COP, so the value set is a fixed
    #  value of the date 05/03/2021
    return 3804.95
