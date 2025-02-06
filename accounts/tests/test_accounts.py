from datetime import datetime, timedelta, timezone

import allure
import pytest
from http import HTTPStatus

from accounts.model_accounts import (create_100_length_string, create_101_length_string, \
                                     create_russian_symbols_string, create_diff_symbols_string,
                                     create_simple_string, \
                                     create_all_special_symbols_string, create_50_length_string,
                                     create_51_length_string, create_mix_symbols_letters_numbers_string)
from assertions import assert_status_code, assert_contains_key, assert_equal, assert_not_equal
from accounts.account_api import create_account_request, get_account_by_id_request, delete_account_request, \
    get_accounts_list_request, patch_account_request
from accounts.account_helper import account_factory, get_account_by_type, account_factory_snmpv3


@pytest.mark.parametrize("account_type", ["ipmi", "snmpv2c", "snmpv3"])
@allure.feature('Accounts API')
class TestAccounts:

    @allure.story('Method Post')
    class TestPostMethod:

        @allure.title('Create account with valid data')
        def test_create_account(self, client, account_type):
            account_data = account_factory(account_type)
            response = create_account_request(client, account_data)

            assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
            json_response = response.json()

            # Проверка полей и значений ответа
            assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе

            for key in ["name", "type", "data"]:
                assert_equal(json_response[key], getattr(account_data, key))

            # Проверка даты создания (created_at)
            created_at_str = json_response.get("created_at")
            assert created_at_str is not None, "created_at field is missing in response"
            created_at = datetime.fromisoformat(created_at_str).astimezone(timezone.utc)
            now = datetime.now(timezone.utc)
            print(created_at)
            print(now)

            # Проверка на разницу в пределах одной минуты
            time_difference = abs((created_at - now).total_seconds())
            print(time_difference)
            assert time_difference <= 120, f"created_at date {created_at} does not match current date {now}"

        @allure.title('Get account by id')
        def test_get_account_by_id(self, client, account_type):
            account_data = account_factory(account_type)
            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()

            response = get_account_by_id_request(client, response_post['id'])
            assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
            get_response = response.json()

            # Сравнение ответа от GET с данными от POST
            assert_equal(get_response["id"], response_post['id'])  # Проверяем совпадение идентификатора
            # Сравниваем остальные ключи
            assert_equal(get_response, response_post)

        @allure.title('Get accounts list')
        def test_get_accounts_list(self, client, account_type):
            account_data = account_factory(account_type)
            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()

            response = get_accounts_list_request(client, query=response_post['name'])

            assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
            get_response = response.json()
            assert_equal(get_response['accounts'][0], response_post)

        def test_create_duplicate_account(self, client, account_type):
            account_data = account_factory(account_type)
            response = create_account_request(client, account_data)

            assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
            response_second_try = create_account_request(client, account_data)
            assert_status_code(response_second_try, HTTPStatus.BAD_REQUEST)


        """Check necessary fields"""
        @pytest.mark.parametrize("field, expected_error", [
            ("name", None),  # Убираем имя
            ("type", None),  # Убираем тип
            ("data", None),  # Убираем data
        ])
        @allure.title('Create account with missing fields')
        def test_create_account_missing_fields(self, client, field, expected_error, account_type):
            account_data = account_factory(account_type)  # Создаем аккаунт с валидными данными
            setattr(account_data, field, expected_error)  # Убираем значение у указанного поля
            response = create_account_request(client, account_data)

            assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа

        """Name validation"""
        @allure.title('Create account name max')
        def test_create_account_name_max(self, client, account_type):
            account_data = account_factory(account_type, name_creator=create_100_length_string)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()
            assert_equal(response_post['name'], account_data.to_dict()['name'])

        @allure.title('Create account name more than max')
        def test_create_account_name_more_than_max(self, client, account_type):
            account_data = account_factory(account_type, name_creator=create_101_length_string)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)
            response_post = response.json()
            assert_equal(response_post['message'], "неверное тело запроса: name: the length must be no more than 100.")

        @allure.title('Create account name with all valid symbols')
        def test_create_account_name_all_valid_symbols(self, client, account_type):
            account_data = account_factory(account_type, name_creator=create_all_special_symbols_string)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.CREATED)
            response_post = response.json()
            assert_equal(response_post['name'], account_data.to_dict()['name'])

        @allure.title('Create account name with russian symbols')
        def test_create_account_name_russian_symbols(self, client, account_type):
            account_data = account_factory(account_type, name_creator=create_russian_symbols_string)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)
            response_post = response.json()
            assert_equal(response_post['message'], "неверное тело запроса: name: must be in a valid format.")

        @allure.title('Create account name with special symbols')
        def test_create_account_name_diff_symbols(self, client, account_type):
            account_data = account_factory(account_type, name_creator=create_diff_symbols_string)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)
            response_post = response.json()
            assert_equal(response_post['message'], "неверное тело запроса: name: must be in a valid format.")

        """Type validation"""
        @pytest.mark.parametrize("field, expected_error", [
            ("type", create_simple_string()),
            ("type", create_russian_symbols_string()),
            ("type", create_diff_symbols_string()),
            ("type", create_all_special_symbols_string())
        ])
        @allure.title('Create invalid account type')
        def test_create_invalid_account_type(self, client, account_type, field, expected_error):
            account_data = account_factory(account_type)
            setattr(account_data, field, expected_error)

            response = create_account_request(client, account_data)
            assert_status_code(response, HTTPStatus.BAD_REQUEST)
            response_post = response.json()
            assert_equal(response_post['message'], "неверное тело запроса: type: must be a valid value.")



        """Check necessary fields in data"""
        @allure.title('Create account with missing data fields')
        def test_create_account_missing_data_fields(self, client, account_type):
            account_data = account_factory(account_type)


            # Задаём обязательные поля для проверки
            required_fields = {
                'snmpv2c': ['community'],
                'ipmi': ['username', 'auth_password'],
                'snmpv3': ['username', 'security_level']
            }

            fields_to_check = required_fields.get(account_type, [])

            for field in fields_to_check:
                invalid_account_data = account_data.to_dict().copy()

                removed_value = account_data.to_dict()['data'].pop(field, None)

                print(account_data.to_dict())
                response = create_account_request(client, account_data)
                response_post = response.json()
                assert_status_code(response, HTTPStatus.BAD_REQUEST)
                assert_equal(response_post['message'], "неверное тело запроса: неверные данные учетной записи")
                invalid_account_data['data'][field] = removed_value

        """Validation data fields"""
        @allure.title('Create account with max data length')
        def test_create_account_with_max_data_length(self, client, account_type):
            account_data = account_factory(account_type, data_creator=create_50_length_string())
            response = create_account_request(client, account_data)
            print(account_data.to_dict())

            assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
            json_response = response.json()

            # Проверка полей и значений ответа
            assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе

            for key in ["name", "type", "data"]:
                assert_equal(json_response[key], getattr(account_data, key))


        @allure.title('Create account with more than max data length')
        def test_create_account_with_more_than_max_data_length(self, client, account_type):
            account_data = account_factory(account_type, data_creator=create_51_length_string())
            response = create_account_request(client, account_data)

            assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
            response_post = response.json()
            assert_equal(response_post['message'], "неверное тело запроса: неверные данные учетной записи")

        @pytest.mark.parametrize("data", [create_simple_string(), create_diff_symbols_string(),
                                          create_all_special_symbols_string(), create_mix_symbols_letters_numbers_string()])
        @allure.title('Create account with valid data')
        def test_create_account_with_valid_data(self, client, account_type, data):
            account_data = account_factory(account_type, data_creator=data)
            response = create_account_request(client, account_data)

            assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
            response_post = response.json()

        """"Fail"""
        # @allure.title('Create account with russian data')
        # def test_create_account_with_russian_data(self, client, account_type):
        #     account_data = account_factory(account_type, data_creator=create_russian_symbols_string())
        #     response = create_account_request(client, account_data)
        #
        #     assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
        #     response_post = response.json()

        """Create snmpv3 valid accounts"""
        def test_create_valid_snmpv3_account(self, client, account_type):
            if account_type in ('ipmi', 'snmpv2c'):
                pass
            else:
                account_data = account_factory_snmpv3(account_type, data_creator=create_simple_string,
                                                      security_level='md5')
                print(account_data.to_dict())
                response = create_account_request(client, account_data)

                assert_status_code(response, HTTPStatus.CREATED)  # Ожидаемый статус ответа
                json_response = response.json()

                # Проверка полей и значений ответа
                assert_contains_key(json_response, "id")  # Проверяем наличие идентификатора в ответе

                for key in ["name", "type", "data"]:
                    assert_equal(json_response[key], getattr(account_data, key))















    @allure.title('Get account by id')
    def test_get_account_by_id(self, client, account_type):
        account_data = account_factory(account_type)
        response = create_account_request(client, account_data)
        assert_status_code(response, HTTPStatus.CREATED)
        response_post = response.json()


        response = get_account_by_id_request(client, response_post['id'])
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        get_response = response.json()

        # Сравнение ответа от GET с данными от POST
        assert_equal(get_response["id"], response_post['id'])  # Проверяем совпадение идентификатора
        # Сравниваем остальные ключи
        for key in ["name", "type", "data"]:
            assert_equal(get_response[key], response_post[key])

    @allure.title('Get accounts list')
    def test_get_accounts_list(self, client, account_type):
        response = get_accounts_list_request(client)

        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        get_response = response.json()

    @allure.title('Update account')
    @pytest.mark.parametrize("new_type", ["ipmi", "snmpv3", "snmpv2c"])
    def test_update_account(self, client, account_type, new_type):
        account_data = account_factory(account_type)
        response = create_account_request(client, account_data)
        assert_status_code(response, HTTPStatus.CREATED)
        response_post = response.json()

        # Обновляем тип аккаунта
        account_data = account_factory(new_type)
        response = patch_account_request(client, account_data, response_post['id'])
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа
        patch_response = response.json()

        for key in ["name", "type", "data"]:
            assert_equal(patch_response[key], getattr(account_data, key))

        # Сравнение ответа от GET с данными от POST
        assert_equal(patch_response["id"], response_post['id'])  # Проверяем совпадение идентификатора
        assert_not_equal(patch_response, response_post)

    @allure.title('Delete account')
    def test_delete_account(self, client, account_type):
        account_data = account_factory(account_type)
        response = create_account_request(client, account_data)
        assert_status_code(response, HTTPStatus.CREATED)
        response_post = response.json()


        response = delete_account_request(client, response_post['id'])
        assert_status_code(response, HTTPStatus.OK)  # Ожидаемый статус ответа

    @allure.title('Get account by id after delete')
    def test_get_account_after_delete(self, client, account_type):
        account_data = account_factory(account_type)
        response = create_account_request(client, account_data)
        assert_status_code(response, HTTPStatus.CREATED)
        response_post = response.json()

        response = delete_account_request(client, response_post['id'])
        assert_status_code(response, HTTPStatus.OK)


        response = get_account_by_id_request(client, response_post['id'])
        assert_status_code(response, HTTPStatus.NOT_FOUND)



 ### Негативные тесты
    @pytest.mark.parametrize("field, expected_error", [
        ("name", None),  # Убираем имя
        ("type", None),  # Убираем тип
        ("data", None),  # Убираем data
    ])
    @allure.title('Create account with missing fields')
    def test_create_account_missing_fields(self, client, field, expected_error, account_type):
        account_data = account_factory(account_type)  # Создаем аккаунт с валидными данными
        setattr(account_data, field, expected_error)  # Убираем значение у указанного поля
        response = create_account_request(client, account_data)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа


    # @allure.title('Create account with invalid parameters')
    # def test_create_account_invalid_parameters(self, client):
    #     account_data = account_factory("ipmi")  # Создаем аккаунт с валидными данными
    #     account_data.type = 'invalid_type'  # Убираем имя
    #     response = create_account_request(client, account_data)
    #
    #     assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
    #
    @allure.title('Get account by non-existent id')
    def test_get_account_by_non_existent_id(self, client, account_type):
        non_existent_id = "1234567890"
        response = get_account_by_id_request(client, non_existent_id)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа
    #
    @allure.title('Delete non-existent account')
    def test_delete_non_existent_account(self, client, account_type):
        non_existent_id = "00000000"
        response = delete_account_request(client, non_existent_id)

        assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответа



    # @pytest.mark.parametrize("field, expected_error", [
    #     ("name", None),  # Убираем имя
    #     ("type", None),  # Убираем тип
    #     ("data", None),  # Убираем data
    # ])
    # @allure.title('Update account with missing fields')
    # def test_update_account_missing_fields(self, client):
    #     if not self.account_responses:  # Проверяем наличие созданных аккаунтов
    #         pytest.skip("Нет аккаунтов для обновления")
    #
    #     account_data = account_factory("snmpv3")  # Создаем аккаунт с валидными данными
    #     account_id = self.account_responses[0]["id"]  # Получаем ID существующего аккаунта
    #
    #     setattr(account_data, field, expected_error)  # Убираем значение у указанного поля
    #     response = patch_account_request(client, account_data, account_id)
    #
    #     assert_status_code(response, HTTPStatus.BAD_REQUEST)  # Ожидаемый статус ответ