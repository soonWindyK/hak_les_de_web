from databaseModules.helpModules import get_db_connection


class KnowelegesDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.courses_table = 'courses'
        self.themes_table = 'themes'

    def get_all_courses(self):
        try:
            self.cursor.execute(
                f'SElECT * FROM {self.courses_table}'
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()


    def get_course_info(self, id):
        try:
            self.cursor.execute(
                f'SElECT * FROM {self.courses_table} where id = {id}'
            )
            return self.cursor.fetchall()[0]
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()


    def get_theme_info(self, id):
        try:
            self.cursor.execute(
                f'SElECT * FROM {self.themes_table} where id = {id}'
            )
            return self.cursor.fetchall()[0]
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()


    def get_themses_by_course_id(self, id):
        try:
            self.cursor.execute(
                f'SElECT * FROM {self.themes_table} where id = {id}'
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def add_course(self, name):
        try:
            self.cursor.execute(
                f'INSERT INTO {self.courses_table}(name) '
                f'VALUES("{name}")'
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()


