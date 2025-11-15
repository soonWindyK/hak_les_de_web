from src.databaseModules.helpModules import get_db_connection


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
                                'user_pass VARCHAR(64) NOT NULL,'
                                'city_id INTEGER NOT NULL,'
                                'user_created_time DATETIME DEFAULT CURRENT_TIMESTAMP,'
                                f'FOREIGN KEY(user_role) REFERENCES {self.role}(role_id),'
                                f'FOREIGN KEY(city_id) REFERENCES {self.city}(city_id)'
                                f')')
            self.conn.commit()
        finally:
            self.conn.close()

#vv 

def create_nko_categories(self): 
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.organization} ('
            'category_id SERIAL PRIMARY KEY,'
            'category VARCHAR(100) NOT NULL,'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()


def create_organizations(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.organization} ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR(255) NOT NULL,'
            'description TEXT,'
            'full_description TEXT,'
            'address TEXT,'
            'category_id INTEGER'
            'logo_url VARCHAR(500),'
            'website_url VARCHAR(500),'
            'social_links JSONB,'
            'contact_email VARCHAR(255),'
            'contact_phone VARCHAR(20),'
            'city_id INTEGER NOT NULL,'
            'user_id INTEGER NOT NULL,'
            'is_approved BOOLEAN DEFAULT FALSE,'
            'views_count INTEGER DEFAULT 0,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            f'FOREIGN KEY(city_id) REFERENCES {self.city}(id),'
            f'FOREIGN KEY(user_id) REFERENCES {self.user}(user_id)'
            f'FOREIGN KEY(category_id) REFERENCES {self.category}(category_id)'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_news(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.news} ('
            'id SERIAL PRIMARY KEY,'
            'title VARCHAR(500) NOT NULL,'
            'content TEXT NOT NULL,'
            'excerpt TEXT,'
            'image_url VARCHAR(500),'
            'attachments JSONB,'
            'city_id INTEGER REFERENCES cities(id),'
            'is_global BOOLEAN DEFAULT FALSE,'
            'author_id INTEGER NOT NULL REFERENCES users(user_id),'
            'is_published BOOLEAN DEFAULT TRUE,'
            'views_count INTEGER DEFAULT 0,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_events(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.events} ('
            'id SERIAL PRIMARY KEY,'
            'title VARCHAR(500) NOT NULL,'
            'description TEXT NOT NULL,'
            'short_description TEXT,'
            'event_date TIMESTAMP NOT NULL,'
            'event_end_date TIMESTAMP,'
            'location VARCHAR(500),'
            'image_url VARCHAR(500),'
            'organization_id INTEGER REFERENCES organizations(id),'
            'city_id INTEGER NOT NULL REFERENCES cities(id),'
            'user_id INTEGER NOT NULL REFERENCES users(user_id),'
            'event_type VARCHAR(50),'
            'max_participants INTEGER,'
            'is_approved BOOLEAN DEFAULT FALSE,'
            'registration_required BOOLEAN DEFAULT FALSE,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_knowledge_base(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.knowledge_base} ('
            'id SERIAL PRIMARY KEY,'
            'title VARCHAR(500) NOT NULL,'
            'type VARCHAR(50) NOT NULL,'
            'file_url VARCHAR(500),'
            'video_url VARCHAR(500),'
            'external_url VARCHAR(500),'
            'content TEXT,'
            'description TEXT,'
            'category VARCHAR(100) NOT NULL,'
            'file_size INTEGER,'
            'author_id INTEGER NOT NULL REFERENCES users(user_id),'
            'is_published BOOLEAN DEFAULT TRUE,'
            'download_count INTEGER DEFAULT 0,'
            'view_count INTEGER DEFAULT 0,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_favorite_news(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.favorite_news} ('
            'id SERIAL PRIMARY KEY,'
            'user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,'
            'news_id INTEGER NOT NULL REFERENCES news(id) ON DELETE CASCADE,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'UNIQUE(user_id, news_id)'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_favorite_events(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.favorite_events} ('
            'id SERIAL PRIMARY KEY,'
            'user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,'
            'event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'UNIQUE(user_id, event_id)'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()

def create_favorite_knowledge(self):
    try:
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {self.favorite_knowledge} ('
            'id SERIAL PRIMARY KEY,'
            'user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,'
            'knowledge_id INTEGER NOT NULL REFERENCES knowledge_base(id) ON DELETE CASCADE,'
            'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
            'UNIQUE(user_id, knowledge_id)'
            ')'
        )
        self.conn.commit()
    finally:
        self.conn.close()






