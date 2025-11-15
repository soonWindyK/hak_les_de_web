from databaseModules.helpModules import get_db_connection


class NewssDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.news = 'news'


    def create_new(self, data):
        try:
            print(data)
            self.cursor.execute(
                f'INSERT INTO {self.news}(title, description, created_by_id, attached_file, citi_code)'
                f'VALUES (%s, %s, %s, %s, %s)', data)

            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_all_news(self):
        try:
            self.cursor.execute(f'select * from {self.news}, cities, regions '
                                f'WHERE cities.city_id = {self.news}.citi_code '
                                f'and regions.region_code = cities.region_code ')
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

