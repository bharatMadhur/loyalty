from data_end.sql_queries import INSERT_USER_QUERY, GET_USER_QUERY, UPDATE_USER_QUERY, SOFT_DELETE_USER_QUERY
from database import get_db_connection

class UserService:
    @staticmethod
    def create_user(user_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_USER_QUERY, user_data)
                conn.commit()

    @staticmethod
    def get_user(user_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_USER_QUERY, (user_id, store_id))
                return cursor.fetchone()

    @staticmethod
    def update_user(user_data, user_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_USER_QUERY, user_data + (user_id, store_id))
                conn.commit()

    @staticmethod
    def soft_delete_user(user_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SOFT_DELETE_USER_QUERY, (user_id, store_id))
                conn.commit()