from data_end.sql_queries import INSERT_FEEDBACK_QUERY, GET_FEEDBACK_QUERY, UPDATE_FEEDBACK_QUERY, DELETE_FEEDBACK_QUERY
from database import get_db_connection

class FeedbackService:
    @staticmethod
    def submit_feedback(feedback_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_FEEDBACK_QUERY, feedback_data)
                conn.commit()

    @staticmethod
    def get_feedback(feedback_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_FEEDBACK_QUERY, (feedback_id, store_id))
                return cursor.fetchone()

    @staticmethod
    def update_feedback(feedback_data, feedback_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_FEEDBACK_QUERY, feedback_data + (feedback_id, store_id))
                conn.commit()

    @staticmethod
    def delete_feedback(feedback_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_FEEDBACK_QUERY, (feedback_id, store_id))
                conn.commit()