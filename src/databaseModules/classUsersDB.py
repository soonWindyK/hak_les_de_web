from src.databaseModules.helpModules import db_returner, get_db_connection


class UsersDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.table_name = 'users'


    def new_user(self, *kwargs):
        try:
            print(*kwargs)

            self.cursor.execute(
                f'INSERT INTO {self.table_name}(first_name, last_name, father_name, user_role, user_birthaday, user_mail, user_pass, city_id) '
                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', *kwargs)
            self.conn.commit()
        finally:
            self.conn.close()


    def select_with_mail(self, mail):
        try:
            self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE user_mail = "{mail}"')
            return db_returner(data=self.cursor.fetchall())[0]
        finally:
            self.conn.close()

    def check_presence_mail(self, mail):
        try:
            self.cursor.execute(f"SELECT user_mail FROM {self.table_name} WHERE user_mail = '{mail}'")
            db_returner(self.cursor.fetchall())[0]['user_mail']
            return True
        except Exception as e:
            return False
        finally:
            self.conn.close()

    def select_users_msgs(self, us_name):
        resp = self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE admin == 0 and us_name != "{us_name}"').fetchall()
        return json_return(resp)

    def select_users_all(self):
        resp = self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE admin == 0').fetchall()
        return json_return(resp)

    def select_admins(self):
        resp = self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE admin == 1').fetchall()
        return json_return(resp)

    def update_user(self, data: dict, email):
        try:
            print(data, email)
            self.cursor.execute(f'UPDATE {self.table_name} SET us_name = :us_name, ' +
                                f'age = :age, ' +
                                f'info = :info,' +
                                f'profile_picture = :profile_picture' +
                                f' WHERE email = "{email}"', data)
            self.conn.commit()
        except Exception as e:
            return e