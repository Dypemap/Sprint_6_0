**Base (pages/base_page.py)**

Вынесены обращения к driver и WebDriverWait: open_url, find_element / find_elements, scroll_into_view, click_via_script, работа с вкладками, wait_until_url_not_blank, wait_until и др.

**Page objects**

- **main_page.py** — без прямых вызовов driver; шаблон локатора FAQ вынесен в FAQ_EXPANDED_HEADING и faq_expanded_heading_locator(); добавлены is_on_main_page(), open_dzen_via_yandex_logo(), is_dzen_page_opened().
- **order_first_step_page.py, order_second_step_page.py** — взаимодействие через методы base; шаблон RENTAL_OPTION вынесен в константу и rental_period_locator().
Тесты (test/test_order.py)
- Убраны if в тестах — два отдельных метода: test_order_scooter_positive_flow_via_top_button и ..._via_bottom_button.
- Убраны прямые обращения к driver и WebDriverWait — только методы страниц.
- Удалён дубликат tests/test_order.py.
