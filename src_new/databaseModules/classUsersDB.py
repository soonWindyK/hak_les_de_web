from databaseModules.helpModules import db_returner, get_db_connection


class UsersDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.table_name = 'users'

    def new_user(self, data):
        try:
            print(data)

            self.cursor.execute(
                f'INSERT INTO {self.table_name}('
                f'first_name, last_name, '
                f'father_name, user_role, '
                f'user_birthday, user_mail, '
                f'user_pass, city_id) '
                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', data)
            self.conn.commit()
        finally:
            self.conn.close()

    def update_user(self, data, mail):
        try:
            print(mail, data)

            self.cursor.execute(
                f'UPDATE {self.table_name} SET '
                f'first_name = %s, '
                f'last_name = %s, '
                f'father_name = %s, '
                f'user_birthday = %s '
                f'WHERE user_mail = "{mail}"', data)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def select_with_mail(self, mail):
        try:
            self.cursor.execute(
                f'SELECT * FROM {self.table_name}, roles '
                f'WHERE user_mail = %s '
                f'AND roles.role_id = {self.table_name}.user_role',
                (mail,)
            )
            return db_returner(data=self.cursor.fetchall())[0]
        except Exception as e:
            print(e)
            return {'role_id': 1}
        finally:
            self.conn.close()

    def update_password(self, mail, password):
        try:
            self.cursor.execute(
                f'UPDATE {self.table_name} SET user_pass = %s WHERE user_mail = %s',
                (password, mail)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def check_presence_mail(self, mail):
        try:
            self.cursor.execute(
                f"SELECT user_mail FROM {self.table_name} WHERE user_mail = %s",
                (mail,)
            )
            db_returner(self.cursor.fetchall())[0]['user_mail']
            return True
        except Exception as e:
            return False
        finally:
            self.conn.close()
