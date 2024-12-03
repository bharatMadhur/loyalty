from data_end.sql_queries import INSERT_STORE_QUERY, GET_STORE_QUERY, UPDATE_STORE_QUERY, DELETE_STORE_QUERY
from database import get_db_connection

class StoreService:
    @staticmethod
    def create_store(store_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_STORE_QUERY, store_data)
                conn.commit()

    @staticmethod
    def get_store(store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_STORE_QUERY, (store_id,))
                return cursor.fetchone()

    @staticmethod
    def update_store(store_data, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_STORE_QUERY, store_data + (store_id,))
                conn.commit()

    @staticmethod
    def delete_store(store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_STORE_QUERY, (store_id,))
                conn.commit()