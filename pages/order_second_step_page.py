from datetime import datetime, timedelta

import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class OrderSecondStepPage(BasePage):
    DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    DATEPICKER_DAY = (
        By.CSS_SELECTOR,
        ".react-datepicker__day:not(.react-datepicker__day--outside-month)"
        ":not(.react-datepicker__day--disabled)",
    )
    ORDER_HEADER = (By.CSS_SELECTOR, ".Order_Header__BZXOb")
    RENTAL_DROPDOWN = (By.CSS_SELECTOR, ".Dropdown-control")
    RENTAL_OPTION = (By.XPATH, "//div[text()='{period}']")
    ORDER_SUBMIT_BUTTON = (
        By.XPATH,
        "(//button[contains(@class,'Button_Middle') and text()='Заказать'])[last()]",
    )
    CONFIRM_MODAL = (By.XPATH, "//div[contains(@class,'Order_Modal__')]")
    CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'Order_Modal__')]//button[text()='Да']",
    )
    SUCCESS_MODAL = (By.XPATH, "//div[contains(@class,'Order_Modal')]")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")

    @classmethod
    def rental_period_locator(cls, period: str):
        xpath = cls.RENTAL_OPTION[1].format(period=period)
        return (cls.RENTAL_OPTION[0], xpath)

    @allure.step("Заполнить второй шаг заказа")
    def fill_form(self, rental_period: str = "сутки"):
        self._select_delivery_date()
        self._select_rental_period(rental_period)
        self.find_element(self.COLOR_GREY_CHECKBOX).click()

    def _select_delivery_date(self):
        tomorrow = (datetime.now() + timedelta(days=1)).day
        date_input = self.wait_until_visible(self.DATE_INPUT)
        date_input.click()
        for day in self.find_elements(self.DATEPICKER_DAY):
            if day.text == str(tomorrow):
                day.click()
                return
        self.wait_until_clickable(self.DATEPICKER_DAY).click()

    def _select_rental_period(self, rental_period: str):
        self.find_element(self.ORDER_HEADER).click()
        dropdown = self.wait_until_clickable(self.RENTAL_DROPDOWN)
        self.click_with_action_chains(dropdown)
        self.wait_until_clickable(self.rental_period_locator(rental_period)).click()

    @allure.step("Подтвердить заказ")
    def submit_order(self):
        self.scroll_and_click(self.ORDER_SUBMIT_BUTTON)
        self.wait_until_visible(self.CONFIRM_MODAL)
        self.scroll_and_click(self.CONFIRM_YES_BUTTON)

    def _find_visible_success_modal(self):
        for modal in self.find_elements(self.SUCCESS_MODAL):
            if modal.is_displayed() and "Заказ оформлен" in modal.text:
                return modal
        return False

    @allure.step("Проверить окно успешного заказа")
    def wait_success_message(self):
        return self.wait_until(lambda _: self._find_visible_success_modal(), timeout=15)

    @allure.step("Получить текст окна успешного заказа")
    def get_success_message(self) -> str:
        return self.wait_success_message().text
