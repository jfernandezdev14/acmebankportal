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
        raise ApiException(response.message, status_code=response.status_code)

    return json.loads(response.text)
