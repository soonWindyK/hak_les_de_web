from databaseModules.helpModules import get_db_connection


class SmallFuncsDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.categories = 'categories'


    def select_all_categories(self):
        try:
            self.cursor.execute(
                f"SELECT * FROM {self.categories}"
            )
            cats_list = []
            cats = self.cursor.fetchall()

            for row in cats:
                cats_list.append((row['id'], row['category_name']))

            return cats_list
        finally:
            self.conn.close()
