import string
from random import choice, randint, random, shuffle
from string import ascii_letters, digits

""""Numbers"""
def random_number(start: int = 100, end: int = 1000) -> int:
    return randint(start, end)

""""Strings"""

def random_string(start: int = 9, end: int = 15) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(randint(start, end)))

def random_string_length_100(length: int = 100) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_string_length_50(length: int = 50) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_string_length_51(length: int = 51) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_string_length_101(length: int = 101) -> str:
    return ''.join(choice(ascii_letters + digits) for _ in range(length))

def random_string_with_some_symbols(start: int = 10, end: int = 20) -> str:
    mandatory_characters = [
        choice(string.ascii_uppercase),  # Заглавная буква
        choice(string.ascii_lowercase),  # Строчная буква
        choice(string.digits),  # Цифра
        '.', '-', '_'
    ]
    length = randint(start, end) - len(mandatory_characters)
    additional_characters = [choice(string.ascii_letters + string.digits + '._-') for _ in range(length)]
    # Собираем все символы и перемешиваем
    all_characters = mandatory_characters + additional_characters
    shuffle(all_characters)
    return ''.join(all_characters)


def random_string_russian_symbols(start: int = 10, end: int = 20) -> str:
    lower_case = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    upper_case = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Строчная буква
    return ''.join(choice(lower_case + upper_case) for _ in range(randint(start, end)))

def random_string_diff_symbols(start: int = 10, end: int = 20) -> str:
    symbols = '.-!"@#$;%^:&?*()+=/<>\\'
    return ''.join(choice(symbols) for _ in range(randint(start, end)))

def random_string_mix_symbols_letters_numbers(start: int = 10, end: int = 20) -> str:
    symbols = '.-!"@#$;%^:&?*()+=/<>\\'
    return ''.join(choice(ascii_letters + digits + symbols) for _ in range(randint(start, end)))

def random_list_of_strings(start: int = 9, end: int = 15) -> list[str]:
    return [random_string() for _ in range(randint(start, end))]






