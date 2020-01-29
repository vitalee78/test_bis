import random
import time

from src.LocatorsHelper import ButtonsHelper, CommonFunctions


class ShowData:
    def __init__(self, man):
        self.man = man
        self.button = ButtonsHelper(man)
        self.function = CommonFunctions()

    # WS-d-016 Проверка телефонов на сайте и в БД в карточке товара
    # проверка раскрытия телефонов при клике
    # передаёт id товара, номер телефона для проверки в тест кейс
    def check_phone_in_goods(self, query_order):
        wd = self.man.wd
        self.button.search_goods(wd, query_order)
        self.button.click_magnifier(wd)
        time.sleep(2)
        id_goods = self.click_random_goods(wd)
        phone = wd.find_element_by_xpath("//*[@class='seller__info']/a[2]").text
        return self.function.req_phone(phone), id_goods

    # клик на любой товар в товарной выдаче не зависимо от позицианирования - списоком или галереей
    # передаёт id товара
    def click_random_goods(self, wd):
        try:
            elements = wd.find_elements_by_xpath("//*[@id='goods']//h5/a")
            id_goods = self.random_click(elements)
        except:
            elements = wd.find_elements_by_xpath("//*[@class='prod-container']/div[1]/a[1]")
            id_goods = self.random_click(elements)
        return id_goods

    def random_click(self, elements):
        random_element = random.choice(elements)
        href = random_element.get_attribute("href")
        spl = href.split('/')[-1]
        random_element.click()
        return spl
