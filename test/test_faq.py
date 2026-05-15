import allure
import pytest

from data.faq_data import FAQ_DATA
from pages.main_page import MainPage


@allure.feature("FAQ")
@allure.story("Вопросы о важном")
class TestFaqAccordion:
    @allure.title("Открытие ответа на вопрос: {question}")
    @pytest.mark.parametrize(
        "index,question,expected_answer",
        FAQ_DATA,
        ids=[item[1] for item in FAQ_DATA],
    )
    def test_faq_answer_is_displayed(
        self, driver, index, question, expected_answer
    ):
        main_page = MainPage(driver).open()
        main_page.click_faq_question(index)
        assert main_page.is_faq_answer_visible(index)
        assert main_page.get_faq_answer_text(index) == expected_answer
