from databaseModules.helpModules import get_db_connection


class EventsDB_module:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        self.events = 'events'


    def create_event(self, data):
        try:
            print(data)
            self.cursor.execute(
                f'INSERT INTO {self.events}(title, description, organizer, location, date, city_id, category_id, start_time, end_time, crated_by_id)'
                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)

            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def get_all_events(self):
        try:
            self.cursor.execute(f'select * from {self.events}, cities, regions '
                                f'WHERE cities.city_id = {self.events}.city_id '
                                f'and regions.region_code = cities.region_code ')
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            self.conn.close()

