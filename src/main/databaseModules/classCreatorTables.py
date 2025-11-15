from src.main.databaseModules.helpModules import get_db_connection


class CreatorTables:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

        self.city = 'cities'
        self.region = 'regions'
        self.user = 'users'
        self.role = 'roles'

    def create_cities(self):
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.city}("
                "city_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                "city_name VARCHAR(64) NOT NULL UNIQUE,"
                "region_code INTEGER NOT NULL,"
                f"FOREIGN KEY(region_code) REFERENCES {self.region}(region_code)"
                ")"
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_regions(self):
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.region}("
                "region_code INTEGER PRIMARY KEY,"
                "region_name VARCHAR(64) NOT NULL UNIQUE"
                ")"
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_roles(self):
        try:
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.role}("
                "role_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
                "role_name VARCHAR(64) NOT NULL UNIQUE,"
                "role_discrip TEXT"
                ")"
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_users(self):
        try:
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.user}(' +
                                'user_id INTEGER AUTO_INCREMENT PRIMARY KEY,' +
                                'first_name VARCHAR(64) NOT NULL,' +
                                'last_name VARCHAR(64),'
                                'father_name VARCHAR(64),'
                                'user_role INTEGER NOT NULL,'
                                'user_birthday DATETIME NOT NULL,'
                                'user_mail VARCHAR(256) NOT NULL UNIQUE,'
                                'user_pass VARCHAR(64) NOT NULL,'
                                'city_id INTEGER NOT NULL,'
                                'user_created_time DATETIME DEFAULT CURRENT_TIMESTAMP,'
                                f'FOREIGN KEY(user_role) REFERENCES {self.role}(role_id),'
                                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id)'
                                f')')
            self.conn.commit()
        finally:
            self.conn.close()







