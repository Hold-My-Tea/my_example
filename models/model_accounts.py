
from utils.fakers import random_string, random_string_length_100, random_string_length_101, random_string_with_some_symbols, \
    random_string_russian_symbols, random_string_diff_symbols, random_string_length_50, random_string_length_51, \
    random_string_mix_symbols_letters_numbers


def create_simple_string():
    return random_string()


def create_100_length_string():
    return random_string_length_100()

def create_50_length_string():
    return random_string_length_50()

def create_51_length_string():
    return random_string_length_51()

def create_101_length_string():
    return random_string_length_101()

def create_all_special_symbols_string():
    return random_string_with_some_symbols()

def create_russian_symbols_string():
    return random_string_russian_symbols()

def create_diff_symbols_string():
    return random_string_diff_symbols()

def create_mix_symbols_letters_numbers_string():
    return random_string_mix_symbols_letters_numbers()



# def set_simple_data(account_type: str):
#     if account_type == "ipmi":
#         data = {
#             "username": create_simple_string(),
#             "auth_password": create_simple_string()
#         }
#     elif account_type == "snmpv3":
#         data = {
#             "username": create_simple_string(),
#             "security_level": "noauth",  # Можно изменить на другой уровень безопасности
#             "context_name": "",
#             "auth_password": "",
#             "auth_encryption": "",
#             "privacy_password": "",
#             "privacy_encryption": ""
#         }
#     elif account_type == "snmpv2c":
#         data = {
#             "community": create_simple_string()
#         }
#     else:
#         raise ValueError(f"Unknown account type: {account_type}")
#     return data


class CreateAccount:
    def __init__(self, account_type: str, name_creator=None, data_creator=None):
        self.type = account_type

        if name_creator is None:
            # Если функция не передана, используем create_simple_name по умолчанию
            self.name = create_simple_string()
        else:
            # Используем переданную функцию для создания имени
            self.name = name_creator()

        if data_creator is None:
            if account_type == "ipmi":
                self.data = {
                    "username": create_simple_string(),
                    "auth_password": create_simple_string()
                }
            elif account_type == "snmpv3":
                self.data = {
                    "username": create_simple_string(),
                    "security_level": "noauth",  # Можно изменить на другой уровень безопасности
                    "context_name": "",
                    "auth_password": "",
                    "auth_encryption": "",
                    "privacy_password": "",
                    "privacy_encryption": ""
                }
            elif account_type == "snmpv2c":
                self.data = {
                    "community": create_simple_string()
                }
            else:
                raise ValueError(f"Unknown account type: {account_type}")
        else:
            if account_type == "ipmi":
                self.data = {
                    "username": data_creator,
                    "auth_password": data_creator
                }
            elif account_type == "snmpv3":
                self.data = {
                    "username": data_creator,
                    "security_level": "noauth",  # Можно изменить на другой уровень безопасности
                    "context_name": "",
                    "auth_password": "",
                    "auth_encryption": "",
                    "privacy_password": "",
                    "privacy_encryption": ""
                }
            elif account_type == "snmpv2c":
                self.data = {
                    "community": data_creator
                }
            else:
                raise ValueError(f"Unknown account type: {account_type}")



    def to_dict(self):
        """Преобразует объект в словарь для сериализации в JSON."""
        return {
            "name": self.name,
            "type": self.type,
            "data": self.data
        }



class CreateAccountSNMPV3:
    def __init__(self, account_type: str, name_creator=None, data_creator=None, security_level=None,
                 auth_encryption=None, privacy_encryption=None):
        self.type = account_type

        if name_creator is None:
            # Если функция не передана, используем create_simple_name по умолчанию
            self.name = create_simple_string()
        else:
            # Используем переданную функцию для создания имени
            self.name = name_creator()


        if security_level is None:
            self.data = {
                "username": data_creator,
                "security_level": "noauth",  # Можно изменить на другой уровень безопасности
                "context_name": "",
                "auth_password": "",
                "auth_encryption": "",
                "privacy_password": "",
                "privacy_encryption": ""
            }

        elif security_level is "nopriv":
            self.data = {
                "username": data_creator,
                "security_level": "nopriv",
                "context_name": data_creator,
                "auth_password": data_creator,
                "auth_encryption": auth_encryption,
                "privacy_password": "",
                "privacy_encryption": ""
            }

        elif security_level is "priv":
            self.data = {
                "username": data_creator,
                "security_level": "priv",
                "context_name": data_creator,
                "auth_password": data_creator,
                "auth_encryption": auth_encryption,
                "privacy_password": data_creator,
                "privacy_encryption": privacy_encryption
            }

        else:
            self.data = {
                "username": data_creator,
                "security_level": data_creator,
                "context_name": data_creator,
                "auth_password": data_creator,
                "auth_encryption": data_creator,
                "privacy_password": data_creator,
                "privacy_encryption": data_creator
            }


    def to_dict(self):
        """Преобразует объект в словарь для сериализации в JSON."""
        return {
            "name": self.name,
            "type": self.type,
            "data": self.data
        }









