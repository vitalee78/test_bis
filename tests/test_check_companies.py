import allure

query_com = 'Аутсорсинговый контакт-центр БИС-Новосибирск'
query_goods = 'Услуги Call-центра'
numeral = 1

name_suite = allure.feature('Проверка карточки компании')


@name_suite
@allure.title('WS-d-015-1 Открытие карточки компании и наличие товаров в разделе "Предложения компании:"')
def test_check_company_tabs(man):
    check_prods = man.check_company.check_company_card(query_com)
    assert check_prods == 4, 'Нет товаров в разделе "Предложения компании:"'
    # вызываю окно и проверяю его появления
    report_error = man.check_company.check_form_error()
    assert report_error == 'Сообщить об ошибке или пожаловаться'


@name_suite
@allure.title('WS-d-015-2 проверяем в прайсе компании клики кнопок "Запомненные", "К сравнению"')
def test_check_buttons_in_price(man):
    get_nums = man.check_company.check_company_price(query_com)
    for num in get_nums:
        assert num >= numeral, 'Нет счётчика товаров или не работают функции'


@name_suite
@allure.title('WS-d-015-3 проверяем в прайсе результат выдачи услуг')
def test_check_result_in_price(man):
    check_relevant = man.check_company.check_search_price(query_com, query_goods)
    for g in check_relevant:
        assert g == query_goods


@name_suite
@allure.title('WS-d-015-4 проверка верификации - если не ввели текст в обязательном поле')
# отрицательный сценарий
def test_check_varification_in_message(man):
    empty_message = man.check_company.check_form_error_goods(query_com)
    assert 'Опишите ошибку / проблему:' == empty_message


@name_suite
@allure.title('WS-d-015-5 сверяет адрес на карте Яндекс с адресом в карточке фирмы')
def test_address_map(man):
    get_address = man.check_company.check_address(query_com)
    address_map = get_address[0]
    spl_map = address_map.split()[1].strip()
    address_card = get_address[1]
    spl_card = address_card.split('.')[2].replace('д', '').strip()
    assert spl_map == spl_card


def rep_prices(s):
    return s.replace('  /месяц', '').replace('-', '0').replace(' ', '')


@name_suite
@allure.title('WS-d-015-6 проверка сортировки в поисковой выдаче - "По возростанию"')
def test_sort_ascending(man, db):
    prices_by_webpage = man.check_company.get_prices_ascending(query_com)
    ascending_by_webpage = [rep_prices(ascend) for ascend in prices_by_webpage if rep_prices(ascend) != '0']
    prices_in_db = db.sort_ascending(query_com)
    assert ascending_by_webpage == prices_in_db, 'В функциональности есть баги'


@name_suite
@allure.title('WS-d-015-7 проверка сортировки в поисковой выдаче - "По убыванию"')
def test_sort_descending(man, db):
    prices_by_webpage = man.check_company.get_prices_descending(query_com)
    descending_by_webpage = [rep_prices(descend) for descend in prices_by_webpage]
    prices_in_db = db.sort_descending(query_com)
    assert descending_by_webpage == prices_in_db
