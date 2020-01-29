import pymysql.cursors

from models.Data import DateApp


class DbHelper:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host=host, database=name, user=user, password=password, charset="utf8")
        self.connection.autocommit(True)

    def get_id_goods(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT phone
                FROM bis_core_seven.goods_phones 
                WHERE id_goods = %s""", (id))
            for phone in cursor.fetchall():
                return phone[0]
        finally:
            cursor.close()

    def get_companies_ids(self, type, limit):
        '''
            Selection of contractual firms until 10
        :return:
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT id_company
                      FROM bis_core_seven.companies
                      WHERE id_refresh!=666 AND type IN (%s)
                      LIMIT %s
                      """, (type, limit))
            row = cursor.fetchall()
            ids = [r[0] for r in row]
            return ids
        finally:
            cursor.close()

    # получить список данных заявки из таблицы goods_order
    def get_test_order(self, order_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                """SELECT user_name, user_phone, email_user, message
                    FROM bis_core_seven.goods_order
                    WHERE user_name=%s""", order_name)
            row = cursor.fetchall()
            try:
                return row[0]
            except IndexError as e:
                print("Отсутствует заказ в таблице -", e)
        finally:
            cursor.close()

    # очистить от тестовых заказов в таблице goods_order
    def delete_test_order(self, order_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                      DELETE FROM bis_core_seven.goods_order
                      WHERE user_name=%s""", order_name)
        finally:
            cursor.close()

    ########################################### SQL queries for private office #####################################

    # получить список данных заявки из таблицы goods_order
    def get_form_new(self):
        l = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, user_name, user_phone, email_user, message FROM goods_order WHERE id_goods=71845")
            for row in cursor:
                (id, user_name, user_phone, email_user, message) = row
                l.append(DateApp(id=id, user_name=user_name, user_phone=user_phone,
                                 email_user=email_user, message=message))
        finally:
            cursor.close()
        return l

    # получить новую фирму в company_register
    def get_new_company(self):
        l = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, user_name, user_phone, email_user, message FROM company_register WHERE id_goods=71845")
            for row in cursor:
                (id, user_name, user_phone, email_user, message) = row
                l.append(DateApp(id=id, user_name=user_name, user_phone=user_phone,
                                 email_user=email_user, message=message))
        finally:
            cursor.close()
        return l

    def destroy(self):
        self.connection.close()

    # вернуть данные в таблице bis_core_seven.company_register
    # чтобы не было видно в админке у оператора
    def return_date(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE bis_core_seven.company_register SET new = 0 WHERE id_company = 38318")
        finally:
            cursor.close()

    # удалить тестовую компанию в таблице bis_core_seven.company_register
    # чтобы не было видно в админке у оператора
    def delete_test_company(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""DELETE cr 
                        FROM bis_core_seven.company_register cr 
                        WHERE cr.id_company = 0
                        AND cr.name LIKE 'Тест фирма фактическая' AND cr.name_urid LIKE 'Тест фирма юридическая'""")
        finally:
            cursor.close()

    # чтобы не копились записи в таблицах
    def delete_test_users_auth(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""DELETE ua
                           FROM  bis_core_seven_users.users_auth ua
                            WHERE  ua.password='40c3634c0347ed3d0b2c0d84b55d5f64'""")
        finally:
            cursor.close()

    def check_without_refresh(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT DATE_FORMAT(date_changed, '%d.%m.%Y')"
                           "FROM bis_core_seven.companies WHERE id_company=38318")
            rows = cursor.fetchall()
            return rows[0][0]
        finally:
            cursor.close()

    def check_stat_document(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                    SELECT id_company
                      FROM bis_core_seven.company_ordered_documents
                        WHERE id_company=38318""")
            try:
                rows = cursor.fetchall()
                return rows[0][0]
            except IndexError:
                return None
        finally:
            cursor.close()

    # чистит тестовые заказы статистики в таблице company_ordered_documents
    def delete_stat_documents(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                              DELETE FROM bis_core_seven.company_ordered_documents
                                WHERE id_company=38318""")
        finally:
            cursor.close()

    ################################################# queries for sort ###############################################

    def sort_ascending(self, company_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                   SELECT REPLACE(gp.min_price, '.0', '')
                      FROM bis_core_seven.goods g
                      JOIN bis_core_seven.goods_prices gp ON gp.id_goods=g.id_goods
                      JOIN bis_core_seven.companies c ON c.id_company=g.id_company                  
                      WHERE c.name=%s AND gp.min_price!=0
                      ORDER BY gp.min_price
                       """, company_name)
            rows = cursor.fetchall()
            return [list(p)[0] for p in rows]
        finally:
            cursor.close()

    def sort_descending(self, company_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                   SELECT REPLACE(gp.min_price, '.0', '')
                      FROM bis_core_seven.goods g
                      JOIN bis_core_seven.goods_prices gp ON gp.id_goods=g.id_goods
                      JOIN bis_core_seven.companies c ON c.id_company=g.id_company                  
                      WHERE c.name=%s
                      ORDER BY gp.min_price DESC 
                       """, company_name)
            rows = cursor.fetchall()
            return [list(p)[0] for p in rows]
        finally:
            cursor.close()
