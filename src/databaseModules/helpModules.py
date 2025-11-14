


def wither(data):
    print(data)

def db_returner(data, coloumn=False):
    if not coloumn:
        return [dict(row) for row in data]
    else:
        return [dict(row)[coloumn] for row in data]

from data_from_env import db_table, db_host, db_pass, db_user, db_port
import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            port=db_port,
            password=db_pass,
            database=db_table
    )
    return conn