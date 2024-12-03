from data_end.sql_queries import INSERT_OFFER_QUERY, GET_OFFER_QUERY, UPDATE_OFFER_QUERY, DELETE_OFFER_QUERY
from database import get_db_connection

class OfferService:
    @staticmethod
    def create_offer(offer_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_OFFER_QUERY, offer_data)
                conn.commit()

    @staticmethod
    def get_offer(offer_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_OFFER_QUERY, (offer_id, store_id))
                return cursor.fetchone()

    @staticmethod
    def update_offer(offer_data, offer_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_OFFER_QUERY, offer_data + (offer_id, store_id))
                conn.commit()

    @staticmethod
    def delete_offer(offer_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_OFFER_QUERY, (offer_id, store_id))
                conn.commit()