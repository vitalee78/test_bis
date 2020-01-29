import allure

from src.generate_data import query_filtr, limit_filtr


@allure.title(f'Проверка функции выбрать параметры у товара/услуги {query_filtr}')
def test_checking_params(man):
    filtrs = man.select_params.check_filters(query_filtr, limit_filtr)
    for filtr in filtrs:
        assert filtr != '', 'Отсутствует название производителя'
    assert len(filtrs) == limit_filtr, 'Не соответствует кол-во "плашек"'
