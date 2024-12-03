from data_end.sql_queries import INSERT_TRANSACTION_QUERY, GET_TRANSACTION_QUERY, UPDATE_TRANSACTION_QUERY, DELETE_TRANSACTION_QUERY
from database import get_db_connection

class TransactionService:
    @staticmethod
    def create_transaction(transaction_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_TRANSACTION_QUERY, transaction_data)
                conn.commit()

    @staticmethod
    def get_transaction(transaction_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_TRANSACTION_QUERY, (transaction_id, store_id))
                return cursor.fetchone()

    @staticmethod
    def update_transaction(transaction_data, transaction_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_TRANSACTION_QUERY, transaction_data + (transaction_id, store_id))
                conn.commit()

    @staticmethod
    def delete_transaction(transaction_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_TRANSACTION_QUERY, (transaction_id, store_id))
                conn.commit()