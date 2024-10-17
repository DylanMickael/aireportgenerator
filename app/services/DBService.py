# app/services/db_service.py
from app import get_db_connection, get_db_schema

class DBService:
    @staticmethod
    def get_schema():
        return get_db_schema()
    
    @staticmethod
    def execute_query(query):
        if not query:
            raise ValueError("No query provided")

        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return results
