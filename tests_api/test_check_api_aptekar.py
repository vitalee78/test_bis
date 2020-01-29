drug = 'анальгин'


def test_check_api(api_aptekar):
    api_aptekar.write_xml(drug, str(2))
    check = api_aptekar.get_xml()
    assert check != [], 'API у аптекаря не работает, нужно проверить' \
                        'https://api.vapteke.ru/Spravka/univers.php?procedure=dbo.usp_TovarSearchWithPriceAllWebForXML&s=анальгин&City_ID=2'
