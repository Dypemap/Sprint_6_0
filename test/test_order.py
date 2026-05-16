import allure

from data.order_data import ORDER_USERS
from pages.main_page import MainPage
from pages.order_first_step_page import OrderFirstStepPage
from pages.order_second_step_page import OrderSecondStepPage


@allure.feature("Заказ самоката")
class TestOrderScooter:
    @allure.title(
        "Позитивный сценарий заказа: "
        f"{ORDER_USERS[0].name} {ORDER_USERS[0].surname}, вход: верхняя кнопка"
    )
    def test_order_scooter_positive_flow_via_top_button(self, driver):
        user = ORDER_USERS[0]
        main_page = MainPage(driver).open()
        main_page.click_order_button_top()

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

    @allure.title(
        "Позитивный сценарий заказа: "
        f"{ORDER_USERS[1].name} {ORDER_USERS[1].surname}, вход: нижняя кнопка"
    )
    def test_order_scooter_positive_flow_via_bottom_button(self, driver):
        user = ORDER_USERS[1]
        main_page = MainPage(driver).open()
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

        OrderFirstStepPage(driver).wait_until_loaded()
        main_page.click_samokat_logo()

        assert main_page.is_on_main_page()

    @allure.title("Логотип Яндекса открывает Дзен в новой вкладке")
    def test_yandex_logo_opens_dzen(self, driver):
        main_page = MainPage(driver).open()
        main_page.open_dzen_via_yandex_logo()

        assert main_page.is_dzen_page_opened()
