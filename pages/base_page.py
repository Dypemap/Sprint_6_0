import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть URL")
    def open_url(self, url: str):
        self.driver.get(url)

    @allure.step("Дождаться видимости элемента")
    def wait_until_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Дождаться кликабельности элемента")
    def wait_until_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def scroll_into_view(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )

    def click_via_script(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Прокрутить к элементу и кликнуть")
    def scroll_and_click(self, locator):
        element = self.wait_until_clickable(locator)
        self.scroll_into_view(element)
        element.click()
        return element

    def click_with_action_chains(self, element):
        ActionChains(self.driver).click(element).perform()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_normalized_current_url(self) -> str:
        return self.get_current_url().rstrip("/")

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    @allure.step("Дождаться открытия {count} вкладок")
    def wait_for_window_count(self, count: int, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.number_of_windows_to_be(count)
        )

    @allure.step("Переключиться на другую вкладку")
    def switch_to_other_window(self, current_handle):
        for handle in self.driver.window_handles:
            if handle != current_handle:
                self.driver.switch_to.window(handle)
                return
        raise RuntimeError("Другая вкладка не найдена")

    @allure.step("Дождаться загрузки URL новой вкладки")
    def wait_until_url_not_blank(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: "about:blank" not in driver.current_url.lower()
        )

    def wait_until(self, condition, timeout=10):
        return WebDriverWait(self.driver, timeout).until(condition)
