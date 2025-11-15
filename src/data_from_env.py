from dotenv import load_dotenv
import os

load_dotenv()

db_table = os.getenv('db_table')
db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_port = os.getenv('db_port')

print(db_table)
