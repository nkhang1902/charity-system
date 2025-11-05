from src.core.config import settings
import mysql.connector

class MySQL:
    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=settings.MySQLHost,
                port=settings.MySQLPort,
                user=settings.MySQLUser,
                password=settings.MySQLPassword,
                database=settings.MySQLDatabase,
                autocommit=True,
                connection_timeout=10
            )
        except Exception as e:
            print(f"[MySQL] Connection error: {str(e)}")
            raise e

    def _ensure_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self._connect()

    def executeQuery(self, query: str, params: tuple = None):
        try:
            self._ensure_connection()
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"[MySQL] Query error: {str(e)}")
            raise e

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
