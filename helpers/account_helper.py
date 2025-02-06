from http import HTTPStatus

from utils.assertions import assert_status_code, assert_contains_key, assert_equal
from config import BASE_URL
from api.authentication_api import get_token
from ..api.account_api import create_account_request
from ..models.model_accounts import CreateAccount, CreateAccountSNMPV3


def account_factory(account_type, name_creator=None, data_creator=None):
    return CreateAccount(account_type, name_creator, data_creator)

def account_factory_snmpv3(account_type, data_creator=None, name_creator=None, security_level=None,
                 auth_encryption=None, privacy_encryption=None):
    return CreateAccountSNMPV3(account_type, data_creator, name_creator, security_level, auth_encryption, privacy_encryption)




def get_account_by_type(account_type, account_responses):
    """Helper method to find an account by its type."""
    for account in account_responses:
        if account["type"] == account_type:
            return account
    return None


def create_and_return_account(client, account_type):
    """Helper method to create an account and return the response."""
    account_data = account_factory(account_type)
    response = create_account_request(client, account_data)
    assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
    json_response = response.json()

    # Проверка полей и значений ответа
    assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе

    for key in ["name", "type", "data"]:
        assert_equal(json_response[key], getattr(account_data, key))

    return json_response["id"], account_data
