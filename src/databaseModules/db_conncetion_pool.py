import time
import mysql.connector
from queue import Queue
from threading import Lock
from data_from_env import db_table, db_user, db_host, db_pass, db_port


class ConnectionPool:
    def __init__(self, size):
        self.db_conf = dict(
            host=db_host,
            user=db_user,
            password=db_pass,
            port=db_port,
            database=db_table
        )
        self.timeout = 3
        self.size = size  # Размер пула
        self.lock = Lock()  # Блокировка для синхронизации доступа
        self.queue = Queue(maxsize=size)  # Очередь для хранения соединений

        for _ in range(size):
            conn = mysql.connector.connect(**self.db_conf)
            self.queue.put(conn)

    def get_connection(self):
        """Получает свободное соединение из пула или ожидает освобождения."""
        while True:
            try:
                # Ждем появления свободного соединения в течение указанного времени
                conn = self.queue.get(timeout=self.timeout)
                return conn
            except Exception:
                # Если очередь пуста и ждать нечего, пытаемся создать новое соединение
                if self.queue.qsize() >= self.size:
                    raise Exception("No available connections!")
                else:
                    conn = mysql.connector.connect(**self.db_conf)
                    return conn

    def release_connection(self, conn):
        with self.lock: self.queue.put(conn)


# Глобальные переменные для примера
connection_pool = None


def init_pool(size=1):
    print('Пуск', size)
    global connection_pool
    connection_pool = ConnectionPool(size=size)


def get_conn_from_pool():
    """
    Получает соединение из пула
    """
    global connection_pool
    if connection_pool is None:
        raise ValueError("Connection pool has not been initialized.")
    print('connect')
    return connection_pool.get_connection()

def close_conn_in_pool(conn):
    """
    Возвращает соединение обратно в пул
    """
    global connection_pool
    if connection_pool is None:
        raise ValueError("Connection pool has not been initialized.")
    print('disconnect')
    connection_pool.release_connection(conn)
