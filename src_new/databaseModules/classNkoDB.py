from databaseModules.helpModules import get_db_connection


class NkoDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.nko_list = 'list_nko'


    def create_nko(self, data):
        try:
            print(data)
            self.cursor.execute(
                f"INSERT INTO {self.nko_list}(name, category_id, description, about, volounteer_help, "
                f"address, email, phone, link_social_net, link_website, citi_code, creator_id) "
                f"VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)", data
            )
            self.conn.commit()
            return False
        except Exception as e:
            print(e)
            return e
        finally:
            self.conn.close()

    def get_all_nko(self, status=2):
        try:
            self.cursor.execute(
                f"SELECT * FROM {self.nko_list}, cities, categories, regions "
                f"WHERE "
                f"status_id = {status} "
                f"and cities.city_id = {self.nko_list}.citi_code "
                f"and categories.id = {self.nko_list}.category_id "
                f"and regions.region_code = cities.region_code "
                f"and {self.nko_list}.deleted_at is null"
            )
            data = self.cursor.fetchall()
            print(data)
            return data
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def get_nko_by_city_id(self, city_id):
        try:
            status = 2
            self.cursor.execute(
                f"SELECT * FROM {self.nko_list}, cities, categories, regions WHERE "
                f"status_id = {status} "
                f"and cities.city_id = {self.nko_list}.citi_code "
                f"and categories.id = {self.nko_list}.category_id "
                f"and regions.region_code = cities.region_code "
                f"and {self.nko_list}.deleted_at is null "
                f"and citi_code = {city_id}"
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def delete_nko(self, nko_id):
        try:
            self.cursor.execute(
                f'UPDATE {self.nko_list} SET deleted_at = CURRENT_TIMESTAMP '
                f'WHERE nko_id = {nko_id}')
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def update_status_nko(self, nko_id: int, status: int):
        try:
            self.cursor.execute(
                f'UPDATE {self.nko_list} '
                f'SET status_id = {status} '
                f'WHERE nko_id = {nko_id}'
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()
            pass