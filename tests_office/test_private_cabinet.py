import datetime

import allure
import pytest


@allure.title('Тест-кейс WS - 016 Проврека функции обновления - "без изменений"')
def test_confirm_company(po, db):
    check_message = po.private_office.confirm_active_company()
    assert check_message == 'Спасибо за проверку ваших данных.'
    execute_db = db.check_without_refresh()
    date_changed = po.private_office.check_date()
    assert execute_db == date_changed


@allure.title('Тест-кейс WS - 017 Проверка функции редактирования сущействующей фирмы')
def test_edit_company(po, db):
    check_message = po.private_office.edit_active_company()
    assert check_message == 'Данные обновлены'
    db.return_date()


@allure.title('Тест-кейс WS - 015 Проверка функции сравнения существующей фирмы')
def test_check_company(po):
    check_message = po.private_office.check_company()
    assert check_message == 'Данная компания уже зарегистрирована'


@allure.title('Тест-кейс WS - 014 Проверка добавления новой компании')
def test_add_company(po, db):
    check = po.private_office.add_company()
    assert check == 'Спасибо'
    with allure.step("Удалил тестовую фирму в таблице bis_core_seven.company_register"):
        db.delete_test_company()


date_stat = datetime.datetime.today().strftime("%Y-%m-%d")


@pytest.mark.env("not_run")
@allure.title('Тест-кейс WS - 018 Проверка отправки статистики у недоговорной фирмы')
def test_send_stat_no_contract(po, db):
    '''
        На devtest в ЛК не работает отправка статистики
        Тест пропускается
    '''
    check_massege = po.private_office.send_stat_no_contract()
    assert check_massege == 'Спасибо'
    check_date = po.private_office.check_stat()
    assert check_date == date_stat
    check_message_delete = po.private_office.delete_order_document()
    assert check_message_delete == 'Документ успешно удален'
    check_in_db = db.check_stat_document()
    if check_in_db is not None:
        db.delete_stat_documents()
