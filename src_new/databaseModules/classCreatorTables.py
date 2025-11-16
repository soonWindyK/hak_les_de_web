from databaseModules.helpModules import get_db_connection

# создаются таблицы для удобства (часть руками была сделана) поэтмоу тут неактуально
class CreatorTables:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor(buffered=True, dictionary=True)

        self.city = 'cities'
        self.region = 'regions'
        self.user = 'users'
        self.role = 'roles'
        self.organization = 'organisation'
        self.news = 'news'
        self.events = 'events'
        self.knowledge_base = 'knowledge_base'
        self.favorite_news = 'favorite_news'
        self.favorite_events = 'favorite_events'
        self.favorite_knowledge = 'favorite_knowledge'
        self.favorite_organizations = 'favorite_organizations'

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
                                'user_pass VARCHAR(256) NOT NULL,'
                                'city_id INTEGER NOT NULL,'
                                'user_created_time DATETIME DEFAULT CURRENT_TIMESTAMP,'
                                f'FOREIGN KEY(user_role) REFERENCES {self.role}(role_id),'
                                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id)'
                                f')')
            self.conn.commit()
        finally:
            self.conn.close()

    def create_nko_categories(self):
        try:
            self.cursor.execute(
                'CREATE TABLE IF NOT EXISTS nko_categories ('
                'category_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'category_name VARCHAR(100) NOT NULL UNIQUE,'
                'category_description TEXT'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_organizations(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.organization} ('
                'org_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'org_name VARCHAR(255) NOT NULL,'
                'category_id INTEGER,'
                'short_description TEXT,'
                'full_description TEXT,'
                'volunteer_functions TEXT,'
                'address VARCHAR(500),'
                'logo_url VARCHAR(500),'
                'website_url VARCHAR(500),'
                'vk_url VARCHAR(500),'
                'telegram_url VARCHAR(500),'
                'contact_email VARCHAR(255),'
                'contact_phone VARCHAR(50),'
                'city_id INTEGER NOT NULL,'
                'user_id INTEGER NOT NULL,'
                'is_approved BOOLEAN DEFAULT FALSE,'
                'views_count INTEGER DEFAULT 0,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                'updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id),'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id),'
                'FOREIGN KEY(category_id) REFERENCES nko_categories(category_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_news(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.news} ('
                'news_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'title VARCHAR(500) NOT NULL,'
                'content TEXT NOT NULL,'
                'excerpt TEXT,'
                'image_url VARCHAR(500),'
                'attachments TEXT,'
                'city_id INTEGER,'
                'is_global BOOLEAN DEFAULT FALSE,'
                'author_id INTEGER NOT NULL,'
                'is_published BOOLEAN DEFAULT TRUE,'
                'views_count INTEGER DEFAULT 0,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                'updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id),'
                f'FOREIGN KEY(author_id) REFERENCES {self.user}(user_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_events(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.events} ('
                'event_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'title VARCHAR(500) NOT NULL,'
                'description TEXT NOT NULL,'
                'short_description TEXT,'
                'event_date DATETIME NOT NULL,'
                'event_end_date DATETIME,'
                'location VARCHAR(500),'
                'image_url VARCHAR(500),'
                'organization_id INTEGER,'
                'city_id INTEGER NOT NULL,'
                'user_id INTEGER NOT NULL,'
                'event_type VARCHAR(50),'
                'max_participants INTEGER,'
                'is_approved BOOLEAN DEFAULT FALSE,'
                'registration_required BOOLEAN DEFAULT FALSE,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                'updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(organization_id) REFERENCES {self.organization}(org_id),'
                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id),'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_knowledge_base(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.knowledge_base} ('
                'knowledge_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'title VARCHAR(500) NOT NULL,'
                'type VARCHAR(50) NOT NULL,'
                'file_url VARCHAR(500),'
                'video_url VARCHAR(500),'
                'external_url VARCHAR(500),'
                'content TEXT,'
                'description TEXT,'
                'category VARCHAR(100) NOT NULL,'
                'file_size INTEGER,'
                'author_id INTEGER NOT NULL,'
                'is_published BOOLEAN DEFAULT TRUE,'
                'download_count INTEGER DEFAULT 0,'
                'view_count INTEGER DEFAULT 0,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                'updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(author_id) REFERENCES {self.user}(user_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_favorite_news(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.favorite_news} ('
                'fav_news_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'user_id INTEGER NOT NULL,'
                'news_id INTEGER NOT NULL,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id) ON DELETE CASCADE,'
                f'FOREIGN KEY(news_id) REFERENCES {self.news}(news_id) ON DELETE CASCADE,'
                'UNIQUE KEY unique_user_news (user_id, news_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_favorite_events(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.favorite_events} ('
                'fav_event_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'user_id INTEGER NOT NULL,'
                'event_id INTEGER NOT NULL,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id) ON DELETE CASCADE,'
                f'FOREIGN KEY(event_id) REFERENCES {self.events}(event_id) ON DELETE CASCADE,'
                'UNIQUE KEY unique_user_event (user_id, event_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_favorite_knowledge(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.favorite_knowledge} ('
                'fav_knowledge_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'user_id INTEGER NOT NULL,'
                'knowledge_id INTEGER NOT NULL,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id) ON DELETE CASCADE,'
                f'FOREIGN KEY(knowledge_id) REFERENCES {self.knowledge_base}(knowledge_id) ON DELETE CASCADE,'
                'UNIQUE KEY unique_user_knowledge (user_id, knowledge_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()

    def create_favorite_organizations(self):
        try:
            self.cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {self.favorite_organizations} ('
                'fav_org_id INTEGER AUTO_INCREMENT PRIMARY KEY,'
                'user_id INTEGER NOT NULL,'
                'org_id INTEGER NOT NULL,'
                'created_at DATETIME DEFAULT CURRENT_TIMESTAMP,'
                f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id) ON DELETE CASCADE,'
                f'FOREIGN KEY(org_id) REFERENCES {self.organization}(org_id) ON DELETE CASCADE,'
                'UNIQUE KEY unique_user_org (user_id, org_id)'
                ')'
            )
            self.conn.commit()
        finally:
            self.conn.close()







