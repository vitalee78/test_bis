import os
import time

import xml.etree.ElementTree as ET
import requests
import zeep

index_q = "/index/q/"
company_id = "/company/id/"
goods_id = "/goods/id/"
price_id = "/price/id/"
order_id = "/order/id/"
autocomplite = "/autocomplete/q/"
companiesgoods = "/companygoods/q/"


class APIClient:
    '''
        Класс для REST BisAPI
    '''

    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path, params=None):
        response = requests.get(url=self.base_address + path, params=params)
        if response.status_code == 200:
            return response
        return response.status_code

    def search_goods(self, query, tag):
        res = self.get(index_q + query).json()
        try:
            return res["tovars"][0][tag]
        except:
            return res["count"][tag]

    def get_company(self, query):
        res = self.get(company_id + query).json()
        return res['type']

    def get_card_goods(self, query):
        res = self.get(goods_id + query).json()
        return res

    def send_order(self, id_goods, username, phone, email, comment):
        res = self.get(order_id + str(id_goods) + '?id=123&username=' + username + '&phone=' + phone +
                       '&email=' + email + '&comment=' + comment).json()
        return res['status']


TovarSearchWithPriceAll = '/Spravka/univers.php?procedure=dbo.usp_TovarSearchWithPriceAllWebForXML&s='
City_ID = '&City_ID='
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../media/file.xml')


class APIVapteke:
    '''
        Класс для REST API сервиса Вaптеке - vapteke.ru
    '''
    def __init__(self, api_vapteke):
        self.api_vapteke = api_vapteke

    def write_xml(self, drug, city):
        response = requests.get(
            self.api_vapteke + TovarSearchWithPriceAll + drug + City_ID + city)
        if response.status_code == 200:
            with open(file, 'wb') as f:
                f.write(response.content)
        return response.status_code

    def get_xml(self):
        time.sleep(1)
        root = ET.parse(file)
        drugs = root.findall('U')
        tovar = [t.get('TovarNameFull') for t in drugs]
        return tovar


class WSAPI:
    '''
        Класс SOAP API
        Для проверки статуса и даты обновления морфов и синонимов в БД bis_core_seven
    '''
    def __init__(self, ws_api):
        self.ws_api = ws_api
        self.soap = zeep.Client(wsdl=ws_api)

    def get_update_info(self):
        soap_result = self.soap.service.getUpdaterInfo()
        return soap_result

    def get_prepare_info(self):
        soap_result = self.soap.service.getPrepareInfo()
        return soap_result

