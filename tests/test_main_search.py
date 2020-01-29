import allure
import pytest

from src.generate_data import queries_positive, queries_negative, name_companies

suite_serach = allure.feature('Проверка основного поиска')


# @pytest.mark.env("not_run")
@suite_serach
@allure.title('WS-d-001  Поиск товаров/услуг и автокомплит')
@pytest.mark.parametrize('words', queries_positive)
def test_search_autocomplit_rubrics(man, words):
    check_query = man.search_goods.search_goods_autocomplit_to_rubrics(words)
    assert check_query >= 1, 'Не работает автокоплит или нет товаров согласно запроса'


@suite_serach
@allure.title('WS-d-003  Поиск товаров/услуг по кнопке "лупа" с негативными запросами')
@pytest.mark.parametrize('words', queries_negative)
def test_search_click_to_button(man, words):
    check_query = man.search_goods.search_goods_click_to_button(words)
    assert check_query >= 1


@suite_serach
@allure.title('WS-d-003  Поиск компаний по кнопке "лупа"')
@pytest.mark.parametrize('names', name_companies)
def test_search_companies(man, names):
    check = man.search_goods.search_goods_click_to_button(names)
    assert check >= 1
