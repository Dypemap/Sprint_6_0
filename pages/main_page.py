import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MainPage(BasePage):
    BASE_URL = "https://qa-scooter.education-services.ru/"

    COOKIE_ACCEPT_BUTTON = (By.ID, "rcc-confirm-button")
    ORDER_BUTTON_TOP = (
        By.XPATH,
        "(//button[contains(@class,'Button_Button') and text()='Заказать'])[1]",
    )
    ORDER_BUTTON_BOTTOM = (
        By.XPATH,
        "(//button[text()='Заказать'])[last()]",
    )
    SAMOKAT_LOGO = (By.CSS_SELECTOR, "a[class*='Header_LogoScooter']")
    YANDEX_LOGO = (By.CSS_SELECTOR, "a[class*='Header_LogoYandex']")
    FAQ_ITEMS = (By.CSS_SELECTOR, ".accordion__item")
    FAQ_QUESTION_BUTTON = (By.CSS_SELECTOR, ".accordion__button")
    FAQ_ANSWER_TEXT = (By.CSS_SELECTOR, ".accordion__panel p")

    @allure.step("Открыть главную страницу")
    def open(self):
        self.driver.get(self.BASE_URL)
        self.accept_cookies()
        return self

    @allure.step("Принять cookies")
    def accept_cookies(self):
        try:
            self.wait_until_clickable(self.COOKIE_ACCEPT_BUTTON, timeout=3).click()
        except Exception:
            pass

    @allure.step("Нажать кнопку «Заказать» в шапке")
    def click_order_button_top(self):
        self.scroll_and_click(self.ORDER_BUTTON_TOP)

    @allure.step("Нажать кнопку «Заказать» внизу страницы")
    def click_order_button_bottom(self):
        self.scroll_and_click(self.ORDER_BUTTON_BOTTOM)

    @allure.step("Кликнуть по вопросу FAQ с индексом {index}")
    def click_faq_question(self, index: int):
        self.accept_cookies()
        items = self.driver.find_elements(*self.FAQ_ITEMS)
        item = items[index]
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", item
        )
        question = item.find_element(*self.FAQ_QUESTION_BUTTON)
        self.driver.execute_script("arguments[0].click();", question)
        self.wait_until_clickable(
            (By.CSS_SELECTOR, f"#accordion__heading-{index}[aria-expanded='true']"),
            timeout=5,
        )

    @allure.step("Получить текст ответа FAQ с индексом {index}")
    def get_faq_answer_text(self, index: int) -> str:
        items = self.driver.find_elements(*self.FAQ_ITEMS)
        return items[index].find_element(*self.FAQ_ANSWER_TEXT).text

    @allure.step("Проверить, что ответ FAQ отображается")
    def is_faq_answer_visible(self, index: int) -> bool:
        items = self.driver.find_elements(*self.FAQ_ITEMS)
        button = items[index].find_element(*self.FAQ_QUESTION_BUTTON)
        return button.get_attribute("aria-expanded") == "true"

    @allure.step("Кликнуть по логотипу Самоката")
    def click_samokat_logo(self):
        self.scroll_and_click(self.SAMOKAT_LOGO)

    @allure.step("Кликнуть по логотипу Яндекса")
    def click_yandex_logo(self):
        self.scroll_and_click(self.YANDEX_LOGO)
