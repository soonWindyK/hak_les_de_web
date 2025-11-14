from src.databaseModules.helpModules import get_db_connection

class CreatorTables:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.city = 'cities'
        self.region = 'regions'

    def create_cities(self):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.city}("
            "city_id INTEGER AUTO_INCREMENT PRIMARY KEY,"
            "city_name VARCHAR(64) NOT NULL UNIQUE,"
            "region_code INTEGER NOT NULL,"
            f"FOREIGN KEY(region_code) REFERENCES {self.region}(region_code)"
            ")"
        )

    def create_regions(self):
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.region}("
            "region_code INTEGER PRIMARY KEY,"
            "region_name VARCHAR(64) NOT NULL UNIQUE"
            ")"
        )

