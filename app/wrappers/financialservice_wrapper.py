import json
import requests

from app import BANK_ACCOUNT_API_URL
from app.utilities.decorators.decorators import handle_api_exceptions
from app.utilities.utils.utils import deserialize_and_verify_json_response


@handle_api_exceptions()
def get_bank_account(user_id):
    """
    Calls the endpoint to retrieve a bank account data
    :param user_id: string, User identifier. Ie, "gs8dfg70s867h9"
    :return: Dict, contains the information of a bank account
    """
    data = {
        'user_id': user_id
    }

    response = requests.get(
        BANK_ACCOUNT_API_URL,
        data=json.dumps(data, cls=json.JSONEncoder)
    )

    json_response = deserialize_and_verify_json_response(response)
    return json_response


@handle_api_exceptions()
def update_bank_account_balance(user_id, balance):
    """
    Calls the endpoint to update the balance of a bank account
    :param user_id: string, User identifier. Ie, "gs8dfg70s867h9"
    :param balance: float, Balance of the account. Ie, 200.0
    :return: Dict, contains the response of updating a bank account
    """
    data = {
        'filters': {
            'user_id': user_id
        },
        'data_updated': {
            'balance': balance
        }
    }

    response = requests.patch(
        BANK_ACCOUNT_API_URL,
        data=json.dumps(data, cls=json.JSONEncoder)
    )

    json_response = deserialize_and_verify_json_response(response)
    return json_response
