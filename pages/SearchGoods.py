from src.LocatorsHelper import ButtonsHelper, CommonFunctions
from src.wait import Wait

class SearchGoods:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.function = CommonFunctions()
        self.__wait = Wait(man)

    #  Поиск товаров/услуг и автокомплит
    def search_goods_autocomplit_to_rubrics(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        id3 = "//*[@id='ui-id-3']"
        self.__wait.until_visible_by_xpath_locator(id3)
        wd.find_element_by_xpath(id3).click()
        count = self.function.count_in_result(wd)
        return int(count)

    #  Поиск товаров/услуг с негативным сценарием - запросы с разными лишнеми символами
    def search_goods_click_to_button(self, query):
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        count = self.function.count_in_result(wd)
        return int(count)

    def check_tabs_in_main_result(self, query):
        '''
            TODO: загатовка для нового теста, чтобы кликать по табам в карточке компании
            получать и сверять количество товаров в табах
        '''
        wd = self.man.wd
        self.button.search_goods(wd, query)
        self.button.click_magnifier(wd)
        tabs = wd.find_elements_by_xpath(".//div[@id='ui-tabs-1']/ul//li")
        for tab in tabs:
            tab.click()
            count = self.function.count_in_result(wd)
            return count
