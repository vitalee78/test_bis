import allure

from src.LocatorsHelper import CommonFunctions
from src.generate_data import queries_positive

query_goods = queries_positive[0]


@allure.title(f'WS-d-016 Проверка телефона на сайте и в БД в карточке товара {query_goods}')
def test_check_show_phones(man, db, n=None):
    phone_on_site = man.check_data.check_phone_in_goods(query_goods)
    get_phone = db.get_id_goods(phone_on_site[1]).split(',')[0]
    phone_in_db = CommonFunctions.req_phone(n, get_phone)
    assert phone_on_site[0] == phone_in_db
