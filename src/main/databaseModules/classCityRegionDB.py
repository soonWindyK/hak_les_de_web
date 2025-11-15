from src.main.databaseModules.helpModules import get_db_connection


class CityRegionDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.table_cities = 'cities'
        self.table_regions = 'regions'

    def get_cities_list_with_region(self):
        self.cursor.execute(
            f'SELECT city_id, city_name, region_name FROM {self.table_cities}, {self.table_regions} WHERE {self.table_cities}.region_code = {self.table_regions}.region_code'
        )
        l = []
        for row in self.cursor.fetchall():
            l.append((row['city_id'], row['city_name'], row['region_name']))
        return l