from http import HTTPStatus

from utils.assertions import assert_status_code, assert_contains_key, assert_equal
from config import BASE_URL
from api.authentication_api import get_token



def create_account_request(client, account_data):
    """Создание запроса для создания аккаунта."""
    token = get_token(client)
    response = client.post(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
        json=account_data.to_dict()
    )
    return response

def patch_account_request(client, account_data, account_id):
    """Создание запроса для изменения аккаунта."""
    token = get_token(client)
    response = client.patch(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
        json=account_data.to_dict()
    )
    return response

def get_account_by_id_request(client, account_id):
    """Создание запроса для получения аккаунта по ID."""
    token = get_token(client)
    response = client.get(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
    )
    return response

def delete_account_request(client, account_id):
    """Создание запроса для удаления аккаунта по ID."""
    token = get_token(client)
    response = client.delete(
        f'{BASE_URL}/{account_id}',
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
    )
    return response

def get_accounts_list_request(client, query):
    """Создание запроса для получения списка аккаунтов."""
    token = get_token(client)
    params = {'q': query}
    response = client.get(
        BASE_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f'Bearer {token}'
        },
        params=params
    )
    return response


