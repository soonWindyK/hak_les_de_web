from databaseModules.helpModules import get_db_connection


class CoursesDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.courses_table = 'courses'
        self.themes_table = 'themes'

    def get_all_courses(self):
        """Получить все курсы"""
        try:
            self.cursor.execute(f"SELECT * FROM {self.courses_table} ORDER BY name")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting courses: {e}")
            return []
        finally:
            self.conn.close()

    def get_course_by_id(self, course_id):
        """Получить курс по ID"""
        try:
            self.cursor.execute(f"SELECT * FROM {self.courses_table} WHERE id = %s", (course_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting course: {e}")
            return None
        finally:
            self.conn.close()

    def create_course(self, name):
        """Создать новый курс"""
        try:
            self.cursor.execute(f"INSERT INTO {self.courses_table}(name) VALUES(%s)", (name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating course: {e}")
            return None
        finally:
            self.conn.close()

    def get_themes_by_course(self, course_id):
        """Получить все темы курса"""
        try:
            self.cursor.execute(
                f"SELECT * FROM {self.themes_table} WHERE courses_id = %s ORDER BY id",
                (course_id,)
            )
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error getting themes: {e}")
            return []
        finally:
            self.conn.close()

    def get_theme_by_id(self, theme_id):
        """Получить тему по ID"""
        try:
            self.cursor.execute(f"SELECT * FROM {self.themes_table} WHERE id = %s", (theme_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error getting theme: {e}")
            return None
        finally:
            self.conn.close()

    def create_theme(self, title, description, courses_id, speaker, file_path=None, url=None):
        """Создать новую тему"""
        try:
            self.cursor.execute(
                f"INSERT INTO {self.themes_table}(title, description, courses_id, speaker, file, url) "
                f"VALUES(%s, %s, %s, %s, %s, %s)",
                (title, description, courses_id, speaker, file_path, url)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating theme: {e}")
            return None
        finally:
            self.conn.close()

    def update_theme(self, theme_id, title, description, speaker, file_path=None, url=None):
        """Обновить тему"""
        try:
            self.cursor.execute(
                f"UPDATE {self.themes_table} SET title=%s, description=%s, speaker=%s, file=%s, url=%s "
                f"WHERE id=%s",
                (title, description, speaker, file_path, url, theme_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating theme: {e}")
            return False
        finally:
            self.conn.close()

    def delete_theme(self, theme_id):
        """Удалить тему"""
        try:
            self.cursor.execute(f"DELETE FROM {self.themes_table} WHERE id = %s", (theme_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting theme: {e}")
            return False
        finally:
            self.conn.close()
