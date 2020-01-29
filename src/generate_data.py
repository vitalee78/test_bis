import random
import string

from models.Data import DateApp
from src.modules import load_config

dir_file = '../queries_search.json'

# списки товаров/услуг/компаний для поиска
# отдельные запросы для поиска фирмы, товара
path_queries = load_config(dir_file)['queries']
queries_positive = path_queries['goods_positive']
queries_negative = path_queries['goods_negative']
name_companies = path_queries['name_companies']
service = path_queries['service']
query_filtr = path_queries['query_filtr']
limit_filtr = path_queries['limit_filtr']

name_company_D = path_queries['name_company_D']
id_company_D = path_queries['id_company_D']


def get_new_company():
    """
        Функция принимает словарь с позитивными данными для заполнения новой фирмы
    """
    data = load_config(dir_file)['new_company'][0]
    name_urid = data['name_urid']
    name = data['name']
    code_phone = data['code_phone']
    phone = data['phone']
    code_mobile = data['code_mobile']
    phone_mobile = data['phone_mobile']
    mail = data['mail']
    www = data['www']
    city = data['city']
    street = data['street']
    house = data['house']
    way = data['way']
    position = data['position']
    manager = data['manager']
    rubric = data['rubric']
    return name_urid, name, code_phone, phone, code_mobile, phone_mobile, mail, www, city, street, house, way, position, \
           manager, rubric


def get_current_company():
    """
       Функция принимает словарь с позитивными данными для заполнения зарегистриованой фирмы в БД
       После проверятся функция сравнения контактных данных
    """
    data = load_config(dir_file)['current_company'][0]
    name_urid = data['name_urid']
    code_phone = data['code_phone']
    phone = data['phone']
    mail = data['mail']
    www = data['www']
    city = data['city']
    street = data['street']
    house = data['house']
    return name_urid, code_phone, phone, mail, www, city, street, house


def get_edit_company():
    """
       Функция принимает словарь с позитивными данными для изменения контактных данных у фирмы
    """
    data = load_config(dir_file)['edit_company'][0]
    code_phone = data['code_phone']
    phone = data['phone']
    street = data['street']
    house = data['house']
    manager = data['manager']
    return code_phone, phone, street, house, manager


def random_string(prefix, maxlen):
    symbos = string.ascii_letters + string.digits + " " * 20  # string.punctuation + генерится случайные символы
    return prefix + "".join([random.choice(symbos) for i in range(random.randrange(maxlen))])


# для заполнения формы заявки, негативными данными
data_form_negative = DateApp(order_name=random_string("name", 20), order_phone=random_string("+7 ", 11),
                             order_email=random_string("test_", 10) + ".ru",
                             commit_window=random_string("comment - ", 20))

# для заполнения формы заявки, позитивными данными
data_form_posiitive = DateApp(order_name="Тестер Тестович", order_phone="8-777-123-45-67",
                              order_email="test@test.ru",
                              order_comment="Тестовый заказ, через оформление заказа в Корзине.",
                              commit_window="Тестовый заказ, оформлен в окне Заказать")

order_positive = DateApp(id_goods="2017562", order_name="Тестер Тестович", order_phone="077",
                         order_email="test@bis077.ru",
                         order_comment="Тестовая проверка отправки заказа через API")
