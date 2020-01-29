import datetime

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.LocatorsHelper import CommonFunctions
from src.generate_data import name_company_D, id_company_D, get_new_company, get_current_company, get_edit_company
from src.wait import Wait

date_changed = datetime.datetime.today().strftime("%d.%m.%Y")


class PrivateOffice:
    def __init__(self, man):
        self.man = man
        self.function = CommonFunctions()
        self.__wait = Wait(man)

    def locator_message(self):
        wd = self.man.wd
        message = "message"
        self.__wait.until_not_visible_by_id(message)
        send_message = wd.find_element_by_id(message).text
        with allure.step(f"Отправил текст для проверки - {send_message}"):
            return send_message

    # метод для заполнения полей
    def fill_company(self):
        wd = self.man.wd
        self.select_add_company()
        data = get_new_company()
        with allure.step("Открываю форму и заполняю все необходимые поля"):
            wd.find_element_by_id("name_urid").send_keys(data[0])
            wd.find_element_by_id("name").send_keys(data[1])
            wd.find_element_by_xpath("//*[@id='phones']/div/input[1]").send_keys(data[2])
            wd.find_element_by_xpath("//*[@id='phones']/div/input[2]").send_keys(data[3])
            wd.find_element_by_id("add_phone").click()
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[1]").send_keys(data[4])
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[2]").send_keys(data[5])
            wd.find_element_by_id("mail").send_keys(data[6])
            wd.find_element_by_xpath("//*[@id='sites']/div/input").send_keys(data[7])
            wd.find_element_by_id("city").send_keys(data[8])
            wd.find_element_by_id("street").send_keys(data[9])
            wd.find_element_by_id("house").send_keys(data[10])
            wd.find_element_by_id("way").send_keys(data[11])
            self.scrolling()
            wd.find_element_by_id("position").send_keys(data[12])
            wd.find_element_by_id("manager").send_keys(data[13])
            wd.find_element_by_xpath("//*[@id='busines_annoninput']/input").send_keys(data[14])

    # метод выбор меню Зарегистрировать компанию
    def select_add_company(self):
        wd = self.man.wd
        with allure.step("Кликаю на кнопку 'Добавить компанию'"):
            button_add = "button_add"
            self.__wait.until_visible_by_class_name(button_add)
            wd.find_element_by_class_name(button_add).click()

    # метод для прокрутки страницы
    def scrolling(self):
        wd = self.man.wd
        wd.find_element_by_xpath("//*[@id='registercompanyform']//input[@id='reg_auth']").send_keys(Keys.PAGE_DOWN)

    # Тест-кейс WS - 014 test_cab_add_company. Добавить новую компанию в БД bis_core_seven.company_register
    def add_company(self):
        wd = self.man.wd
        self.fill_company()
        busines_feed = "//*[@id='busines_feed']/li/em"
        self.__wait.until_visible_by_xpath_locator(busines_feed)
        wd.find_element_by_xpath(busines_feed).click()
        wd.find_element_by_id("reg_auth").click()
        return self.locator_message().split('.')[0]

    #  Тест-кейс WS - 015 test_cab_check_company. Проверка функции на наличие существующей компании в БД БИС
    def check_company(self):
        wd = self.man.wd
        self.select_add_company()
        data = get_current_company()
        with allure.step("Открываю форму и заполняю поля"):
            wd.find_element_by_id("name_urid").send_keys(data[0])
            wd.find_element_by_xpath("//*[@id='phones']/div/input[1]").send_keys(data[1])
            wd.find_element_by_xpath("//*[@id='phones']/div/input[2]").send_keys(data[2])
            wd.find_element_by_xpath("//*[@id='sites']/div/input").send_keys(data[4])
            wd.find_element_by_id("mail").send_keys(data[3])
            wd.find_element_by_id("city").send_keys(data[5])
            wd.find_element_by_id("street").send_keys(data[6])
            wd.find_element_by_id("house").send_keys(data[7])
            wd.find_element_by_id("office").click()
        exist_company = "//*[@id='exist_company']/p[1]"
        self.__wait.until_visible_by_xpath_locator(exist_company)
        message = wd.find_element_by_xpath(exist_company).text.split(',')[0]
        self.click_my_companies(wd)
        with allure.step(f"Отправил текст для проверки - {message}"):
            return message

    def click_my_companies(self, wd):
        with allure.step("Перешёл в общий список компаний"):
            my_company = "//*[contains(text(), 'Мои Компании')]"
            self.__wait.until_visible_by_xpath_locator(my_company)
            wd.find_element_by_xpath(my_company).click()

    #  Тест-кейс WS - 016 test_cab_confirm_company. Подтверждение обновления действующей компании.
    def confirm_active_company(self):
        wd = self.man.wd
        self.select_firm()
        wd.find_element_by_xpath(
            "//*[@id='center_cont_content']//a[contains(text(), 'Редактировать данные компании')]").click()
        wd.find_element_by_id("without_refresh").click()
        message = self.locator_message()
        self.click_my_companies(wd)
        return message

    #  Для проверки даты в Тест-кейс WS - 016 test_cab_confirm_company.
    def check_date(self):
        with allure.step(f"Отправил текущею дату на проверку - {date_changed}"):
            return date_changed

    def select_firm(self):
        """
            Вспомогательный метод для выбора из списка фирмы
            Если фирма отсутствует в списке, то првязывает фирму к пользователю в админке
        """
        wd = self.man.wd
        is_company = "//*[@class='menu_company_list']//a[contains(text(), '" + name_company_D + "')]"
        self.__wait.until_visible_by_xpath_locator(is_company)
        if self.function.is_element_present(wd, By.XPATH, is_company):
            with allure.step(f"Выбераю фирму {name_company_D}"):
                wd.find_element_by_xpath(is_company).click()
        else:
            wd.find_element_by_xpath("//*[@class='menu_office']//a[contains(text(),'Мой профиль')]").click()
            self.binding_company()
            wd.find_element_by_xpath(is_company).click()

    #  Тест-кейс WS - 017 test_cab_edit_company. Редактирование действующей компании.
    def edit_active_company(self):
        wd = self.man.wd
        self.select_firm()
        data = get_edit_company()
        with allure.step("Открываю форму и редактирую поля в действующей компании"):
            wd.find_element_by_xpath("//*[@id='center_cont_content']/div[1]/div[1]/div[3]/a[1]").click()
            wd.find_element_by_id("add_phone").click()
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[1]").clear()
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[1]").send_keys(data[0])
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[2]").clear()
            wd.find_element_by_xpath("//*[@id='phones']/div[2]/input[2]").send_keys(data[1])
            wd.find_element_by_id("street").clear()
            wd.find_element_by_id("street").send_keys(data[2])
            wd.find_element_by_id("house").clear()
            wd.find_element_by_id("house").send_keys(data[3])
            wd.find_element_by_id("manager").clear()
            wd.find_element_by_id("manager").send_keys(data[4])
        with allure.step("Регистрирую форму"):
            wd.find_element_by_id("reg_auth").click()
        message = self.locator_message().split('.')[0]
        self.click_my_companies(wd)
        return message

    # если отсутствует привязка копмпании в ЛК, привязываем к пользователю
    def binding_company(self):
        wd = self.man.wd
        wd.find_element_by_xpath(
            "//*[@class='menu_office']//a[contains(text(),'Привязка компаний к личному кабинету')]").send_keys(
            Keys.PAGE_DOWN)
        wd.find_element_by_xpath(
            "//*[@class='menu_office']//a[contains(text(),'Привязка компаний к личному кабинету')]").click()
        wd.find_element_by_id("company_id").send_keys(id_company_D)
        wd.find_element_by_xpath("//*[@id='center_cont_content']/table[2]/tbody/tr/td/span[2]/a").click()
        wd.find_element_by_id("addPerson").click()
        wd.find_element_by_id("user").send_keys('vitalee@bis077.ru')
        wd.find_element_by_xpath("//*[@id='center_cont_content']//a[contains(text(),'Добавить')]").click()
        wd.find_element_by_xpath("//*[@id='center_cont_content']/a").click()
        self.click_my_companies(wd)

    def send_price(self):
        wd = self.man.wd
        self.select_firm()
        wd.find_element_by_xpath("//*[contains(text(), 'Мои товары/услуги')]").click()

    # Тест-кейс WS - 018. Отправка статистики на эл. ящик
    def send_stat_no_contract(self):
        wd = self.man.wd
        with allure.step("Выбераю фирму 'Балканская къшта'"):
            self.select_firm()
        with allure.step("Перехожу в статистику компании"):
            wd.find_element_by_xpath("//*[contains(text(), 'Cтатистика компании')]").click()
        with allure.step("Заказал статистику"):
            wd.find_element_by_id("order_stat").click()
        message = self.locator_message().split('.')[0]
        return message

    def check_stat(self):
        wd = self.man.wd
        with allure.step("Перешёл в список Заказные документы"):
            wd.find_element_by_xpath("//*[contains(text(), 'Заказанные документы')]").click()
        get_date = wd.find_element_by_xpath("//*[@class='contacts']//tr//td[@align='center'][1]").text.split()[0]
        with allure.step(f"Отправил дату на проверку {get_date}"):
            return get_date

    def delete_order_document(self):
        wd = self.man.wd
        with allure.step("Удалил документ в списке Заказные документы"):
            wd.find_element_by_xpath("//*[@class='contacts']//tr//td[@align='center'][2]//img").click()
        return self.locator_message()
