import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class OrderFirstStepPage(BasePage):
    NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    SURNAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_OPTION = (By.CLASS_NAME, "select-search__option")
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    @allure.step("Заполнить первый шаг заказа")
    def fill_form(self, name, surname, address, metro, phone):
        self.wait_until_visible(self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.SURNAME_INPUT).send_keys(surname)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)
        metro_input = self.driver.find_element(*self.METRO_INPUT)
        metro_input.send_keys(metro)
        self.wait_until_clickable(self.METRO_OPTION).click()
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)

    @allure.step("Перейти ко второму шагу")
    def click_next(self):
        self.scroll_and_click(self.NEXT_BUTTON)
