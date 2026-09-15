from app.database import get_connection

class DBClient:
    def fetch_one(self, sql, params=()):
        connection=get_connection(); cursor=connection.cursor(dictionary=True)
        try:
            cursor.execute(sql, params); return cursor.fetchone()
        finally:
            cursor.close(); connection.close()
