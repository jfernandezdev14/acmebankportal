import json
import requests

from app import VALIDATE_USER_API_URL
from app.utilities.decorators.decorators import handle_api_exceptions
from app.utilities.utils.utils import deserialize_and_verify_json_response


@handle_api_exceptions()
def validate_user_wrapper(user_id, pin):
    """
    Calls the endpoint to validate the user authentication data
    :param user_id: string, User identifier. Ie, "gs8dfg70s867h9"
    :param pin: integer, User pin. Ie, 6543
    :return:
    """
    user_data = {
        'user_id': user_id,
        'pin': pin,
    }

    response = requests.get(
        VALIDATE_USER_API_URL,
        data=json.dumps(user_data, cls=json.JSONEncoder)
    )

    json_response = deserialize_and_verify_json_response(response)
    return json_response
