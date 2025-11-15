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

    def get_all_nko(self):
        try:
            self.cursor.execute(
                f"SELECT * FROM {self.nko_list}, cities, categories, regions WHERE "
                # f"status_id = 2 and "
                f"cities.city_id = {self.nko_list}.citi_code "
                f"and categories.id = {self.nko_list}.category_id "
                f"and regions.region_code = cities.region_code "
                f"and {self.nko_list}.deleted_at is null "
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