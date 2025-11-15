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
                f"address, email, phone, link_social_net, link_website, citi_code, status_id) "
                f"VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 1)", data
            )
            self.conn.commit()
            return False
        except Exception as e:
            print(e)
            return e
        finally:
            self.conn.close()