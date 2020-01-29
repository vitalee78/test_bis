import allure
import time

from src.generate_data import data_form_negative, data_form_posiitive, service, queries_positive

product = queries_positive[2]

get_h1 = 'Сравнить товары'
get_h1_r = 'Запомненные'
get_h1_c = 'Корзина'
numeral = 1
empty_table = 0

suite_compare = allure.feature('Сравнение')
suite_memore = allure.feature('Запомнено')
suite_basket = allure.feature('Корзина')
suite_order = allure.feature('Проверка оформления заказа')


@suite_compare
@allure.title('WS-d-006  Проверка функции добавить "Сравнение"')
def test_check_comparison(man):
    time.sleep(1)
    check_item = man.check_comparison.check_comparison_enable_item(product)
    assert check_item[0] in get_h1, 'Нет перехода на страницу "Сравнить товары"'
    assert check_item[1] >= numeral, 'Нет счётчика товаров в левом выдвигающем окне'


@suite_compare
@allure.title('WS-d-006-1  Проверка функции "Сравнение" снять товары')
def test_check_comparison_disable(man):
    time.sleep(1)
    disable_item = man.check_comparison.check_comparison_disable_item(product)
    assert disable_item is False


@suite_memore
@allure.title('WS-d-007 Проверка функции "Запомнено"')
def test_check_memorized(man):
    check_item = man.check_remember.check_remember_goods(product)
    assert check_item[0] in get_h1_r, 'Нет перехода на страницу "Запомненные"'
    assert check_item[1] >= numeral, 'Нет счётчика товаров в левом выдвигающем окне'
    assert check_item[2] >= numeral, 'Нет счётчика товаров в header'
    assert check_item[3] >= numeral, 'Не открылась страниц или нет товаров'


@suite_memore
@allure.title('WS-d-007-1  Проверка функции "Запомнено" снять товары')
def test_check_memorized_disable(man):
    disable_item = man.check_remember.check_remember_disable_item(product)
    assert disable_item == empty_table, 'Не открылась страниц или не сработало очистка товаров'


@suite_basket
@allure.title('WS-d-008 Проверка функции "Корзина"')
def test_check_cart(man):
    check_item = man.check_cart.check_goods_cart(product)
    assert check_item[0] == get_h1_c, 'Нет перехода на страницу "В корзине"'
    assert check_item[1] >= numeral, 'Нет счётчика товаров в левом выдвигающем окне'
    assert check_item[2] >= numeral, 'Нет счётчика товаров в header'
    assert check_item[3] >= numeral, 'Не открылась страниц или нет товаров'


@suite_basket
@allure.title('WS-d-008-1  Проверка функции "Корзина" снять товары')
def test_check_cart_disable(man):
    disable_item = man.check_cart.check_cart_disable_item(product)
    assert disable_item == empty_table, 'Не открылась страниц или не сработала очистка товаров'


@allure.severity(allure.severity_level.CRITICAL)
@suite_basket
@allure.title('WS-d-008-2  Проверка функции оформления заказа в Корзине')
def test_order_from_basket(man, db):
    order = man.check_cart.check_send_order_from_cart('Массаж-077', data_form_posiitive)
    assert order.split('.')[0] == 'Ваш заказ отправлен'
    order_name = data_form_posiitive.order_name
    db.delete_test_order(order_name)


@allure.severity(allure.severity_level.CRITICAL)
@suite_order
@allure.title('WS-d-009 Проверка функции "Заказать или Купить в 1 клик"  в модальном окне')
def test_send_order(man, db):
    check_send_order = man.check_cart.check_send_order(service, data_form_posiitive)
    assert check_send_order.split('.')[0] == 'Ваш заказ отправлен'
    order_name = data_form_posiitive.order_name
    check_order_in_db = db.get_test_order(order_name)
    assert check_order_in_db[0] == order_name
    db.delete_test_order(order_name)


@allure.severity(allure.severity_level.CRITICAL)
@suite_order
@allure.title('WS-d-009-1 Проверка функции "Заказать или Купить в 1 клик"  в модальном окне, негативный сценарий')
def test_send_order_negative(man):
    send_order_negative = man.check_cart.check_send_order_negative(service, data_form_negative)
    assert send_order_negative == 'Некорректный формат'
