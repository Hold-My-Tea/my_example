import httpx
import pytest



@pytest.fixture(scope="session")
def client():
    with httpx.Client(verify=False) as client:  # Отключение проверки SSL
        yield client


@pytest.fixture(scope='class', autouse=True)
def cleanup():
    """Фикстура для очистки данных после всех тестов класса."""
    yield  # Позволяет выполнить тесты
    # Код для очистки после всех тестов
    # Например, если вы используете список для хранения ответов, его можно очистить
    cleanup.account_responses = []  # Очистка списка ответов