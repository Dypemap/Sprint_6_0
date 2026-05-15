from datetime import datetime, timedelta

import allure
from selenium.webdriver.common.action_chains import ActionChains
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
    ORDER_SUBMIT_BUTTON = (
        By.XPATH,
        "(//button[contains(@class,'Button_Middle') and text()='Заказать'])[last()]",
    )
    CONFIRM_MODAL = (By.XPATH, "//div[contains(@class,'Order_Modal__')]")
    CONFIRM_YES_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'Order_Modal__')]//button[text()='Да']",
    )
    SUCCESS_TITLE = (
        By.XPATH,
        "//div[contains(@class,'Order_Modal')]//div[text()='Заказ оформлен']",
    )

    COLOR_GREY_CHECKBOX = (By.ID, "grey")

    @allure.step("Заполнить второй шаг заказа")
    def fill_form(self, rental_period: str = "сутки"):
        self._select_delivery_date()
        self._select_rental_period(rental_period)
        self.driver.find_element(*self.COLOR_GREY_CHECKBOX).click()

    def _select_delivery_date(self):
        tomorrow = (datetime.now() + timedelta(days=1)).day
        date_input = self.wait_until_visible(self.DATE_INPUT)
        date_input.click()
        for day in self.driver.find_elements(*self.DATEPICKER_DAY):
            if day.text == str(tomorrow):
                day.click()
                return
        self.wait_until_clickable(self.DATEPICKER_DAY).click()

    def _select_rental_period(self, rental_period: str):
        self.driver.find_element(*self.ORDER_HEADER).click()
        dropdown = self.wait_until_clickable(self.RENTAL_DROPDOWN)
        ActionChains(self.driver).click(dropdown).perform()
        rental_option = (
            By.XPATH,
            f"//div[text()='{rental_period}']",
        )
        self.wait_until_clickable(rental_option).click()

    @allure.step("Подтвердить заказ")
    def submit_order(self):
        self.scroll_and_click(self.ORDER_SUBMIT_BUTTON)
        self.wait_until_visible(self.CONFIRM_MODAL)
        modal = self.driver.find_element(*self.CONFIRM_MODAL)
        modal.find_elements(By.TAG_NAME, "button")[1].click()

    @allure.step("Проверить окно успешного заказа")
    def wait_success_message(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        def success_modal_visible(driver):
            modals = driver.find_elements(
                By.XPATH, "//div[contains(@class,'Order_Modal')]"
            )
            for modal in modals:
                if modal.is_displayed() and "Заказ оформлен" in modal.text:
                    return modal
            return False

        return WebDriverWait(self.driver, 15).until(success_modal_visible)

    @allure.step("Получить текст окна успешного заказа")
    def get_success_message(self) -> str:
        return self.wait_success_message().text
