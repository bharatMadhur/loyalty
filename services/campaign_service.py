from data_end.sql_queries import INSERT_CAMPAIGN_QUERY, GET_CAMPAIGN_QUERY, UPDATE_CAMPAIGN_QUERY, DELETE_CAMPAIGN_QUERY
from database import get_db_connection

class CampaignService:
    @staticmethod
    def create_campaign(campaign_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_CAMPAIGN_QUERY, campaign_data)
                conn.commit()

    @staticmethod
    def get_campaign(campaign_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_CAMPAIGN_QUERY, (campaign_id, store_id))
                return cursor.fetchone()

    @staticmethod
    def update_campaign(campaign_data, campaign_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_CAMPAIGN_QUERY, campaign_data + (campaign_id, store_id))
                conn.commit()

    @staticmethod
    def delete_campaign(campaign_id, store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_CAMPAIGN_QUERY, (campaign_id, store_id))
                conn.commit()