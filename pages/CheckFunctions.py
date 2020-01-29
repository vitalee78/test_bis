import time

import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from src.LocatorsHelper import ButtonsHelper, CommonFunctions
from src.wait import Wait


class Locators:
    def __init__(self, man):
        self.man = man
        self.__wait = Wait(man)
        self.get_h1 = "//*[@class='margin-top-0']"
        self.in_table_wishlist = "//*[@class='grid-x grid-padding-x product-line']"

    def open_left_panel(self):
        wd = self.man.wd
        with allure.step("Открываю боковую панель"):
            panel = "main-search__goods-text"
            self.__wait.until_visible_by_class_name(panel)
            wd.find_element_by_class_name(panel).click()

    def click_header_button(self):
        wd = self.man.wd
        buttons = wd.find_elements_by_xpath("//*[@class='cell shrink header__buttons']/a")
        return buttons


class FunctionComparison:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.function = CommonFunctions()
        self.locator = Locators(man)

    # Проверка функции "Сравнение" добавить товар
    def check_comparison_enable_item(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_enter_keys(wd)
        time.sleep(2)
        with allure.step("Кликаю на любую пиктограмму 'Сравнение'"):
            self.select_random_element(wd)
        header = self.locator.click_header_button()
        header[1].click()
        self.locator.open_left_panel()
        time.sleep(1)
        get_h1 = wd.find_element_by_xpath(self.locator.get_h1).text
        badge_left = wd.find_element_by_xpath("//*[@id='comparelist_link_left']//span[@class='badge']").text
        return get_h1, int(badge_left)

    # Проверка функции "Сравнение" снять товары
    def check_comparison_disable_item(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_enter_keys(wd)
        with allure.step("Кликаю на любую пиктограмму 'Сравнение'"):
            self.select_random_element(wd)
        header = self.locator.click_header_button()
        header[1].click()
        with allure.step("Полностью очищаю список товаров"):
            wd.find_element_by_id("compare_delete_all").click()
        is_numeral = self.function.is_element_present(wd, By.XPATH, "//*[@id='comparelist_link']//span[@class='badge']")
        if is_numeral:
            return True
        else:
            return False

    def select_random_element(self, wd):
        try:
            self.function.click_random_element(wd, "//*[@class='prod__img-buttons']/li[2]")
        except Exception:
            self.function.click_random_element(wd, "//*[@class='product-line__link compare_button has-tip']")


class FunctionMemorized:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.function = CommonFunctions()
        self.locator = Locators(man)
        self.__wait = Wait(man)

    # Проверка функции "Запомнено"
    def check_remember_goods(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.button.go_to_list(wd)
        with allure.step("Кликаю на любую пиктограмму 'Запомнено'"):
            self.select_random_element(wd)
        header = self.locator.click_header_button()
        header[0].click()
        self.locator.open_left_panel()
        h1 = "//*[@class='cell']/h1"
        self.__wait.until_visible_by_xpath_locator(h1)
        get_h1 = wd.find_element_by_xpath(h1).text
        link_left = "//*[@id='wishlist_link_left']//span[@class='badge']"
        self.__wait.until_visible_by_xpath_locator(link_left)
        badge_left_wishlist = wd.find_element_by_xpath(link_left).text
        wishlist_link = "//*[@id='wishlist_link']//span"
        self.__wait.until_visible_by_xpath_locator(wishlist_link)
        badge_header_wishlist = wd.find_element_by_xpath(wishlist_link).text
        count = len(wd.find_elements_by_xpath(self.locator.in_table_wishlist))
        return get_h1, int(badge_left_wishlist), int(badge_header_wishlist), int(count)

    # Проверка функции "Запомнено" снять товар
    def check_remember_disable_item(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        with allure.step("Кликаю на любую пиктограмму 'Запомнено'"):
            self.select_random_element(wd)
        header = self.locator.click_header_button()
        header[0].click()
        with allure.step("Отключаю все запомненные товары"):
            all_buttons = wd.find_elements_by_xpath("//*[@class='product-line__link wish_button has-tip']/i")
            len(all_buttons)
            for button in all_buttons:
                button.click()
                time.sleep(0.3)
        with allure.step("Кликаю на вкладку 'Товары', чтобы обновить страницу"):
            wd.find_element_by_xpath("//*[@class='tabs-title desc-tabs__title active']").click()
        count = len(wd.find_elements_by_xpath(self.locator.in_table_wishlist))
        return int(count)

    def select_random_element(self, wd):
        try:
            self.function.click_random_element(wd, "//*[@class='prod__img-buttons']/li[1]")
        except Exception:
            self.function.click_random_element(wd, "//*[@class='margin-bottom-6']/a[1]")


class FunctonCart:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.function = CommonFunctions()
        self.action = ActionChains
        self.locator = Locators(man)
        self.__wait = Wait(man)

    # Проверка функции "Корзина"
    def check_goods_cart(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.button.go_to_list(wd)
        with allure.step("Кликаю на любую кнопку 'В корзину'"):
            self.function.select_card_or_book(wd)
        self.button.go_to_cart(wd)
        self.locator.open_left_panel()
        self.__wait.until_visible_by_xpath_locator(self.locator.get_h1)
        get_h1 = wd.find_element_by_xpath(self.locator.get_h1).text
        badge = "//*[@class='off-canvas__user-link cart-icon']//span[@class='badge']"
        self.__wait.until_visible_by_xpath_locator(badge)
        badge_left_cart = wd.find_element_by_xpath(badge).text
        has_tip = "//*[@class='header__buttons-link has-tip']//span"
        self.__wait.until_visible_by_xpath_locator(has_tip)
        badge_header_cart = wd.find_element_by_xpath(has_tip).text
        div_cart = "//*[@class='div_cart']"
        count = len(wd.find_elements_by_xpath(div_cart))
        return get_h1, int(badge_left_cart), int(badge_header_cart), int(count)

    # Проверка функции "Корзина" снять товар
    def check_cart_disable_item(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.button.go_to_list(wd)
        with allure.step("Кликаю на любую кнопку 'В корзину'"):
            self.function.select_card_or_book(wd)
        try:
            self.button.go_to_cart(wd)
        except ElementNotInteractableException:
            wd.find_element_by_xpath("//*[@id='one-click-order']//span[@aria-hidden='true']").click()
        all_buttons = wd.find_elements_by_xpath("//*[@class='cart_del_button']")
        len(all_buttons)
        for button in all_buttons:
            button.click()
            time.sleep(0.3)
        count = len(wd.find_elements_by_xpath("//*[@class='div_cart']"))
        return int(count)

    def check_send_order_from_cart(self, query, data):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        title = "//*[@title='Косметика для лица и тела']"
        self.__wait.until_visible_by_xpath_locator(title)
        wd.find_element_by_xpath(title).click()
        self.button.go_to_list(wd)
        with allure.step("Кликаю на любую кнопку 'В корзину'"):
            self.function.select_card_or_book(wd)
        self.button.go_to_cart(wd)
        margin = "//*[@class='button text-size-default margin-bottom-8']"
        self.__wait.until_visible_by_xpath_locator(margin)
        wd.find_element_by_xpath(margin).click()
        self.fill_form(data, wd)
        lead = "//*[@class='grid-container']//p[@class='lead']"
        self.__wait.until_visible_by_xpath_locator(lead)
        text_message = wd.find_element_by_xpath(lead).text
        return text_message

    def fill_order(self, query_order, data):
        wd = self.man.wd
        self.button.search_goods(wd, query_order)
        self.button.click_magnifier(wd)
        self.button.go_to_list(wd)
        self.function.select_card_or_book(wd)
        with allure.step("Заполняю форму тестовыми данными"):
            self.fill_form(data, wd)

    # Проверка функции "Оформление заказа"
    def check_send_order(self, query_order, data):
        wd = self.man.wd
        self.fill_order(query_order, data)
        confirmation = "//*[@id='order-confirmation']//p"
        self.__wait.until_visible_by_xpath_locator(confirmation)
        return wd.find_element_by_xpath(confirmation).text

    def check_send_order_negative(self, query_order, data):
        wd = self.man.wd
        self.fill_order(query_order, data)
        red_error = "//*[@class='red red_error']"
        self.__wait.until_visible_by_xpath_locator(red_error)
        return wd.find_element_by_xpath(red_error).text

    def fill_form(self, data, wd):
        try:
            wd.find_element_by_id("one_click_name").send_keys(data.order_name)
        except ElementNotInteractableException:
            wd.find_element_by_id("order_name").send_keys(data.order_name)
        try:
            wd.find_element_by_id("one_click_email").send_keys(data.order_email)
        except ElementNotInteractableException:
            wd.find_element_by_id("order_email").send_keys(data.order_email)
        try:
            wd.find_element_by_id("one_click_phone").send_keys(data.order_phone)
        except ElementNotInteractableException:
            wd.find_element_by_id("order_phone").send_keys(data.order_phone)
        try:
            wd.find_element_by_id("one_click_comment").send_keys(data.commit_window)
        except ElementNotInteractableException:
            wd.find_element_by_id("order_comment").send_keys(data.order_comment)
        try:
            wd.find_element_by_id("one_click_send").click()
        except (ElementNotInteractableException, NoSuchElementException):
            wd.find_element_by_id("order_send").click()
