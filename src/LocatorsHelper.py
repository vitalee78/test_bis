import random
import re

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from src.wait import Wait

class FormsHelper:
    def __init__(self, man):
        self.man = man
        self.function = CommonFunctions()

    def form_error_main(self):
        wd = self.man.wd
        with allure.step('Кликаю, произзвольно, на пиктограмму "Сообщить об ошибке" в основной выдаче'):
            form = wd.find_elements_by_xpath("//*[@class='prod__links has-tip']")
            random_element = random.choice(form)
            random_element.click()

    def form_error_goods(self):
        wd = self.man.wd
        with allure.step('Кликаю, на пиктограмму "Сообщить об ошибке" в карточке фирмы'):
            is_prod_links = self.function.is_element_present(wd, By.CSS_SELECTOR, ".prod__links svg")
            if is_prod_links:
                wd.find_element_by_css_selector(".prod__links svg").click()
            else:
                wd.find_element_by_class_name("product-line__link.error_button").click()


class ButtonsHelper:
    def __init__(self, man):
        self.man = man
        self.__wait = Wait(man)

    def close_left_page(self, wd):
        with allure.step('Закрываю левое-боковое, выдвигающиеся окно'):
            try:
                canvas_close = "//*[@class='close-button off-canvas__close']"
                self.__wait.until_visible_by_xpath_locator(canvas_close)
                wd.find_element_by_xpath(canvas_close).click()
            except (ElementNotInteractableException, NoSuchElementException):
                pass

    def search_goods(self, wd, query):
        with allure.step('Открываю главную страницу сайта'):
            self.man.open_mainpage()
        with allure.step(f'Ввожу поисковой запрос - \'{query}\''):
            # wd.find_element_by_class_name("main-search__reset").click()
            wd.find_element_by_id("q").send_keys(query)

    def click_enter_keys(self, wd):
        with allure.step('Кликаю по клавише "Enter"'):
            wd.find_element_by_id("q").send_keys(Keys.ENTER)

    def click_magnifier(self, wd):
        with allure.step('Кликаю на кнопку "лупа" в поисковой форме'):
            wd.find_element_by_css_selector(".main-search__button").click()

    def go_to_cart(self, wd):
        with allure.step('Кликаю на кнопку "Перейти в корзину" в модальном окне'):
            button_red = "//*[@class='button button_red text-size-default margin-bottom-8']"
            self.__wait.until_visible_by_xpath_locator(button_red)
            wd.find_element_by_xpath(button_red).click()

    def continue_shopping(self, wd):
        with allure.step('Кликаю продолжить покупки'):
            button_regular_green = "//*[@class='button button_regular_green text-size-default margin-bottom-8']"
            self.__wait.until_visible_by_xpath_locator(button_regular_green)
            wd.find_element_by_xpath(button_regular_green).click()

    def go_to_list(self, wd):
        with allure.step('Переключаю товарную выдачу в список'):
            try:
                goods_view = "//*[@class='button-group margin-bottom-2']//i[@class='fa fa-lg fa-th-list goods_view_style']"
                self.__wait.until_visible_by_xpath_locator(goods_view)
                wd.find_element_by_xpath(goods_view).click()
            except:
                pass


class CommonFunctions:

    def select_card_or_book(self, wd):
        try:
            with allure.step("Кликнул в Корзину"):
                self.click_random_element(wd, "//*[@class='product-line__buy']//span[text()='В корзину']")
        except:
            with allure.step("Кликнул Заказать"):
                self.click_random_element(wd,
                                          "//*[@class='product-line__buy shop margin-bottom-2']/a[@aria-haspopup='true']")

    def count_in_result(self, wd):
        '''
            Общая функция,
            передаёт количество товаров/услуг или компаний в товарной выдаче
            Условия определяют на какой странице находятся товары: список или плитка
        :param wd:
        :return : возвращает количество товаров или компаний
        '''
        prod_container = "//*[@class='prod-container']"
        prod_company = "//*[@id='ui-tabs-3']//h5"
        is_prod_container = self.is_element_present(wd, By.XPATH, prod_container)
        is_prod_company = self.is_element_present(wd, By.XPATH, prod_company)
        if is_prod_container:
            count = len(wd.find_elements_by_xpath(prod_container))
        elif is_prod_company:
            count = len(wd.find_elements_by_xpath(prod_company))
        else:
            count = len(wd.find_elements_by_xpath("//*[@class='grid-x grid-padding-x product-line']"))
        with allure.step(f'Получаю количество товаров - \'{count}\''):
            return int(count)

    def get_text_not_found(self, wd):
        text_not_found = wd.find_element_by_css_selector("err-box__head").text
        return text_not_found

    def is_element_present(self, wd, *args):
        '''
            Общая функция для определения истиности
            т.е. есть ли локатор (xpath, css, name, id) в DOM
        :param args:
        :return : возврощает True or False
        '''
        try:
            wd.find_element(*args)
            return True
        except NoSuchElementException:
            return False

    def click_random_element(self, wd, locator):
        '''
            Общая функция для произвольного клика
            по какому-либо элементу
        :param wd:
        :param locator: принимает локатор xpath
        :return: возвращает произвольный объект .click()
        '''
        elements = wd.find_elements_by_xpath(locator)
        random.choice(elements).click()

    def req_phone(self, get_phone):
        '''
            Осуществляет поиск телефона в карточе фирмы,
            оставляет только цифры,
            объединяет в одну строку
        :param get_phone : получает номер телефона, +7(383)277-77-74
        :return : возвращает номер телефона для сравнения
        '''
        req = re.findall(r'\d', get_phone)
        phone = ("".join(req)).split(',')
        return phone[0]
