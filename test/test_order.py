import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.order_data import ORDER_USERS
from pages.main_page import MainPage
from pages.order_first_step_page import OrderFirstStepPage
from pages.order_second_step_page import OrderSecondStepPage


@allure.feature("Заказ самоката")
class TestOrderScooter:
    @allure.title("Позитивный сценарий заказа: {user.name} {user.surname}, вход: {entry_point}")
    @pytest.mark.parametrize(
        "user,entry_point",
        [
            (ORDER_USERS[0], "top"),
            (ORDER_USERS[1], "bottom"),
        ],
        ids=["user_1_top_button", "user_2_bottom_button"],
    )
    def test_order_scooter_positive_flow(self, driver, user, entry_point):
        main_page = MainPage(driver).open()

        if entry_point == "top":
            main_page.click_order_button_top()
        else:
            main_page.click_order_button_bottom()

        first_step = OrderFirstStepPage(driver)
        first_step.fill_form(
            user.name,
            user.surname,
            user.address,
            user.metro,
            user.phone,
        )
        first_step.click_next()

        second_step = OrderSecondStepPage(driver)
        second_step.fill_form(user.rental_period)
        second_step.submit_order()

        assert "Заказ оформлен" in second_step.get_success_message()

    @allure.title("Логотип Самоката ведёт на главную страницу")
    def test_samokat_logo_opens_main_page(self, driver):
        main_page = MainPage(driver).open()
        main_page.click_order_button_top()

        OrderFirstStepPage(driver)
        main_page.click_samokat_logo()

        assert driver.current_url.rstrip("/") == MainPage.BASE_URL.rstrip("/")

    @allure.title("Логотип Яндекса открывает Дзен в новой вкладке")
    def test_yandex_logo_opens_dzen(self, driver):
        main_page = MainPage(driver).open()
        main_window = driver.current_window_handle
        main_page.click_yandex_logo()

        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        WebDriverWait(driver, 10).until(
            lambda d: "about:blank" not in d.current_url.lower()
        )
        current_url = driver.current_url.lower()
        assert (
            "dzen" in current_url
            or "zen.yandex" in current_url
            or "ya.ru" in current_url
        )
