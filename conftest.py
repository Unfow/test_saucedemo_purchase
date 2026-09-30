import pytest
from selenium import webdriver


def pytest_addoption(parser):
    """Регистрация параметров командной строки."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для запуска тестов: chrome, firefox, edge",
    )
    parser.addoption(
        "--url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Базовый адрес тестируемого веб-сайта",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Фикстура получения базового URL."""
    return request.config.getoption("--url")


@pytest.fixture
def browser(request):
    """Фикстура управления браузером с нулевым неявным ожиданием."""
    browser_name = request.config.getoption("--browser").lower()
    driver = None

    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    elif browser_name == "edge":
        driver = webdriver.Edge()
    else:
        raise pytest.UsageError(
            f"Неподдерживаемый браузер: '{browser_name}'. "
            f"Допустимые варианты: chrome, firefox, edge."
        )

    driver.maximize_window()

    # Критерий: неявное ожидание выставлено в 0
    driver.implicitly_wait(0)

    yield driver

    driver.quit()