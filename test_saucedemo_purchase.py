import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_saucedemo_purchase_with_explicit_waits(browser, base_url):
    # Инициализируем явное ожидание до 10 секунд
    wait = WebDriverWait(browser, timeout=10)

    # 1. Открытие стартовой страницы
    browser.get(base_url)

    # =========================================================================
    # Критерий: Явные ожидания для страницы авторизации
    # =========================================================================
    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name")),
        message="Поле логина не отобразилось на странице авторизации",
    )
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password")),
        message="Поле пароля не отобразилось на странице авторизации",
    )
    login_button = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button")),
        message="Кнопка 'Login' не кликабельна",
    )

    username_field.send_keys("standard_user")
    password_field.send_keys("secret_sauce")
    login_button.click()

    # =========================================================================
    # Критерий: Явные ожидания для страницы с товарами
    # =========================================================================
    # Ждём загрузки списка товаров и доступности кнопки добавления в корзину
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")),
        message="Каталог товаров не отобразился",
    )
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack")),
        message="Кнопка добавления товара в корзину недоступна",
    )
    add_to_cart_btn.click()

    # Ждём кликабельности иконки корзины и переходим в неё
    cart_icon = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link")),
        message="Иконка корзины недоступна",
    )
    cart_icon.click()

    # В корзине ожидаем появления кнопки перехода к оформлению
    checkout_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "checkout")),
        message="Кнопка Checkout в корзине недоступна",
    )
    checkout_btn.click()

    # =========================================================================
    # Критерий: Явные ожидания для страницы с оформлением (шаг ввода данных)
    # =========================================================================
    first_name_input = wait.until(
        EC.visibility_of_element_located((By.ID, "first-name")),
        message="Поле имени покупателя не появилось",
    )
    last_name_input = wait.until(
        EC.visibility_of_element_located((By.ID, "last-name")),
        message="Поле фамилии покупателя не появилось",
    )
    zip_input = wait.until(
        EC.visibility_of_element_located((By.ID, "postal-code")),
        message="Поле индекса не появилось",
    )
    continue_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "continue")),
        message="Кнопка 'Continue' не кликабельна",
    )

    first_name_input.send_keys("Иван")
    last_name_input.send_keys("Петров")
    zip_input.send_keys("101000")
    continue_btn.click()

    # =========================================================================
    # Критерий: Явное ожидание для страницы с оплатой/обзором заказа (Overview)
    # =========================================================================
    # Ждём отображения блока с информацией об оплате и доставке (Payment Information)
    wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "summary_info")),
        message="Сводка по оплате и заказу (summary_info) не отобразилась",
    )
    finish_button = wait.until(
        EC.element_to_be_clickable((By.ID, "finish")),
        message="Кнопка 'Finish' для подтверждения покупки не кликабельна",
    )
    finish_button.click()

    # =========================================================================
    # Критерий: Явное ожидание для текста об успешной покупке
    # =========================================================================
    complete_header = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header")),
        message="Заголовок завершения заказа не отобразился",
    )

    expected_text = "Thank you for your order!"
    assert complete_header.text == expected_text, (
        f"Ожидался текст: '{expected_text}', фактически получен: '{complete_header.text}'"
    )