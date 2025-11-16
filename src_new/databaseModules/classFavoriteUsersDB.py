from databaseModules.helpModules import get_db_connection


class FavoriteUsersDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.table_name = 'favorites_user'
        # enum - type_post: nko, news, events

    def presence_in_favorite(self, user_id, post_id, type_post):
        try:
            self.cursor.execute(
                f'SELECT * FROM {self.table_name} '
                f'WHERE user_id = {user_id} '
                f'and post_id = {post_id} '
                f'and post_type = "{type_post}"'
            )
            x = self.cursor.fetchall()[0]
            print(x)
            return x
        except Exception as e:
            print(e)
            return 'error'
        finally:
            self.conn.close()

    def add_favorite(self, user_id, post_id, type_post):
        try:
            self.cursor.execute(
                f'INSERT INTO {self.table_name}(user_id, post_id, post_type) '
                f'VALUES({user_id}, {post_id}, "{type_post}")'
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

    def update_favorite(self, user_id, post_id, type_post, view_status):
        try:
            status = 1 if view_status == 0 else 0
            self.cursor.execute(
                f'UPDATE {self.table_name} SET view_status = {status} '
                f'WHERE user_id = {user_id} '
                f'and post_id = {post_id} '
                f'and post_type = "{type_post}"'
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()