import allure
from selenium.webdriver.common.action_chains import ActionChains

from src.LocatorsHelper import FormsHelper, ButtonsHelper, CommonFunctions
from src.wait import Wait


class HelperCompanies:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.forms = FormsHelper(man)
        self.function = CommonFunctions()
        self.action = ActionChains
        self.__wait = Wait(man)
        self.__locator_xxlarge = "//*[@class='text-size-xxlarge']"

    # WS-d-014 Проверка карточки компании
    def check_company_card(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        prods = len(
            wd.find_elements_by_xpath("//*[@class='grid-x grid-margin-x small-up-1 medium-up-2 large-up-4']/div"))
        return int(prods)

    def check_form_error(self):
        wd = self.man.wd
        self.forms.form_error_main()
        report_error = "//*[@id='report-error']//h2"
        self.__wait.until_visible_by_xpath_locator(report_error)
        return wd.find_element_by_xpath(report_error).text

    def check_form_error_goods(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.click_tab_goods(wd)
        self.forms.form_error_goods()
        wd.find_element_by_xpath("//*[@class='content']//button").click()
        invalid = ".is-invalid-label"
        self.__wait.until_visible_by_css_selector(invalid)
        label = wd.find_element_by_css_selector(invalid).text
        return label

    def check_company_price(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.click_tab_goods(wd)
        self.button.go_to_list(wd)
        with allure.step('Кликаю Запомнить'):
            wish_button = "//*[@class='product-line__link wish_button has-tip']"
            self.__wait.until_visible_by_xpath_locator(wish_button)
            self.function.click_random_element(wd, wish_button)
        with allure.step('Кликаю Сравнить'):
            compare_button = "//*[@class='product-line__link compare_button has-tip']"
            self.__wait.until_visible_by_xpath_locator(compare_button)
            self.function.click_random_element(wd, compare_button)
        numeral_wishlist = "//*[@id='wishlist_link']//span"
        self.__wait.until_visible_by_xpath_locator(numeral_wishlist)
        count_wishlist = wd.find_element_by_xpath(numeral_wishlist).text
        numeral_cart = "//*[@id='comparelist_link']/span"
        self.__wait.until_visible_by_xpath_locator(numeral_cart)
        count_cart = wd.find_element_by_xpath(numeral_cart).text
        return int(count_wishlist), int(count_cart)

    def click_tab_goods(self, wd):
        with allure.step('Перехожу по вкладке "Товары и услуги"'):
            tabs = "//*[@class='desc-tabs tabs']/li[2]"
            self.__wait.until_visible_by_xpath_locator(tabs)
            wd.find_element_by_xpath("//*[@class='desc-tabs tabs']/li[2]").click()

    def check_search_price(self, query, query_goods):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.click_tab_goods(wd)
        wd.find_element_by_xpath("//*[@class='border-none main-search__input ui-autocomplete-input']").send_keys(
            query_goods)
        self.button.click_magnifier(wd)
        margin = wd.find_elements_by_xpath("//*[@class='margin-vertical-0']//span[@class='ellip']")
        goods = [g.text[:18] for g in margin]
        return goods

    def check_address(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        with allure.step('Кликаю на карте Яндекс, на балун и получаю адрес'):
            ymaps = "//*[@id='map1']//ymaps[@class='ymaps-2-1-75-svg-icon-content']"
            element = wd.find_element_by_xpath(ymaps)
            self.__wait.until_visible_by_xpath_locator(ymaps)
            self.action(wd).move_to_element(element).click(element).perform()
        map1 = "//*[@id='map1']//ymaps/h3"
        self.__wait.until_visible_by_xpath_locator(map1)
        get_address_in_maps = wd.find_element_by_xpath(map1).text
        info = "//*[@class='margin-bottom-2 font-info']//tr[1]/td[2]"
        self.__wait.until_visible_by_xpath_locator(info)
        get_addess_in_card = wd.find_element_by_xpath(info).text
        with allure.step(f'Получил адреса и отправил на сверку \'{get_address_in_maps}\' и \'{get_addess_in_card}\''):
            return get_address_in_maps, get_addess_in_card

    def get_prices_ascending(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.click_tab_goods(wd)
        self.button.go_to_list(wd)
        with allure.step('Сортирую По возрастанию'):
            wd.find_element_by_xpath("//*[@class='padding-2 sort_price_asc']").click()
        self.__wait.until_visible_by_xpath_locator(self.__locator_xxlarge)
        elements = wd.find_elements_by_xpath(self.__locator_xxlarge)
        prices_ascending = [price.text.strip() for price in elements]
        with allure.step('Передал на проверку отсортированные цены'):
            return prices_ascending

    def get_prices_descending(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        self.click_tab_goods(wd)
        self.button.go_to_list(wd)
        with allure.step('Сортирую По убыванию'):
            wd.find_element_by_xpath("//*[@class='padding-2 sort_price_desc']").click()
        self.__wait.until_visible_by_xpath_locator(self.__locator_xxlarge)
        elements = wd.find_elements_by_xpath(self.__locator_xxlarge)
        prices_descending = [price.text.strip() for price in elements]
        with allure.step('Передал на проверку отсортированные цены'):
            return prices_descending
