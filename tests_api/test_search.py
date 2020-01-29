import allure
import pytest
import datetime

from src.generate_data import queries_positive, order_positive as op

index_q = "/index/q/"
price_id = "/price/id/"

queries_negative = [156161616516123444444, 'вапвап456654sdgfsdg654']

suite_search = allure.feature('Проверка поиска товаров')
suite_order = allure.feature('Проверка статуса отправки заказа')
suite_updater = allure.feature('Проверка статуса и даты подготовки/обновления синонимов и морфов')
suite_company = allure.feature('Проверка выдачи по компаниям - договорной/недоговрной')


@suite_search
@allure.title('Проверка выдачи по названию товаров - позитивный')
@pytest.mark.parametrize('name', queries_positive)
def test_check_search_goods(base_api, name):
    check = base_api.search_goods(name, 'name')
    assert len(check) >= 1


@suite_search
@allure.title('Проверка выдачи по названию товаров - негативные запросы')
@pytest.mark.parametrize('name', queries_negative)
def test_json(base_api, name):
    check = base_api.search_goods(str(name), 'goods')
    assert str(check) == str(0)


@suite_search
@allure.title('Проверка выдачи по id_goods')
def test_check_id_goods(base_api):
    check = base_api.get_card_goods(str(71416184))
    assert check['id_goods'] == str(71416184)


limit = 2


@suite_company
@allure.title('Проверка наличия договорных компаний')
def test_company_D(base_api, db):
    ids = db.get_companies_ids('D', limit)
    for id in ids:
        check = base_api.get_company(str(id))
        assert check in 'D'


@suite_company
@allure.title('Проверка наличия недоговорных компаний')
def test_company_X(base_api, db):
    ids = db.get_companies_ids('X', limit)
    for id in ids:
        check = base_api.get_company(str(id))
        assert check in 'X'


@suite_company
@allure.title('Проверка системы на ложную выдачу по фирмам')
def test_check_company_negative(base_api, db):
    """
        специально подставляем ids договорной фирмы в недоговорную и наоборот
        и проверям, чтобы система выдала ошибку
    :param base_api:
    :param db:
    :return:
    """
    ids_D = db.get_companies_ids('D', limit)
    for id in ids_D:
        check = base_api.get_company(str(id))
        assert check not in 'X', 'ошибка, договрную фирму выдаёт как Недоговорпную'
    ids_X = db.get_companies_ids('X', limit)
    for id in ids_X:
        check = base_api.get_company(str(id))
        assert check not in 'D', 'ошибка, Недоговрную фирму выдаёт как договорпную'


@suite_company
@allure.title('Проверка выдачи компаний с неготивными данными')
@pytest.mark.parametrize('id_company', queries_negative)
def test_company_price_negative(base_api, id_company):
    check = base_api.get(price_id,
                         params={'id_company': id_company}
                         ).json()
    assert check == []


@suite_order
@allure.title('Проверка заявки, статуса "ok"')
def test_send_order(base_api):
    '''
      Для отправки заказа, проверка статуса "ok" если все поля заполнены корректно.
          пример GET запроса -
          http://www.bis077.ru/api/order/id/2017562?id=123&username=testname&phone=8922111111&email=aaa@aaa.ru&comment=textxxzczxcx
    :param id_goods:
    :param username:
    :param phone:
    :param email:
    :param comment:
    :return:
    '''
    order = base_api.send_order(op.id_goods, op.order_name, op.order_phone, op.order_email, op.order_comment)
    assert order == 'ok'


no = 'no'


@suite_order
@allure.title('Проверка заявки, статуса "no"')
def test_send_order_negative(base_api):
    '''
        Проверка статуса "no" если не заполнены обязательные поля
       :param id_goods:
       :param username:
       :param phone:
    '''
    order_1 = base_api.send_order('', '', '', op.order_email, op.order_comment)
    assert order_1 == no
    order_2 = base_api.send_order(op.id_goods, '', '', op.order_email, op.order_comment)
    assert order_2 == no
    order_3 = base_api.send_order(op.id_goods, op.order_name, '', op.order_email, op.order_comment)
    assert order_3 == no
    order_4 = base_api.send_order(op.id_goods, '', op.order_phone, op.order_email, op.order_comment)
    assert order_4 == no


@suite_updater
@allure.title('Проверка обновления морфов и синонимов, должен быть статус - 1')
def test_status_update(ws_api):
    status_update = ws_api.get_update_info()
    get_status = [status.text for status in status_update[0]]
    assert get_status[1] == '1', 'Не обновились морфы и синонимы, статус 0'


@pytest.mark.env("not_run")
@suite_updater
@allure.title('Проверка подготовки морфов и синонимов, должен быть статус - 1')
def test_status_prepare(ws_api):
    status_prepare = ws_api.get_prepare_info()
    get_status = [status.text for status in status_prepare[0]]
    assert get_status[1] == '1', 'Не прошла подготовка дынных на B2 Mssql, статус 0'


date_now = datetime.datetime.today().strftime("%Y-%m-%d")


@suite_updater
@allure.title('Проверка подготовки морфов и синонимов, должна быть текущая дата')
def test_date_prepare(ws_api):
    date_prepare = ws_api.get_prepare_info()
    get_date = [date.text for date in date_prepare[1]]
    check_date = get_date[1].split()[0]
    assert check_date == date_now, 'Не прошла подготовка дынных на B2 Mssql, дата обновления не соответсвует текущей даты'


@suite_updater
@allure.title('Проверка обновления морф и синонимов, должна быть текущая дата')
def test_date_update(ws_api):
    date_update = ws_api.get_update_info()
    get_date = [date.text for date in date_update[1]]
    check_date = get_date[1].split()[0]
    assert check_date == date_now, 'Не обновились морфы и синонимы, дата обновления не соответсвует текущей даты'
