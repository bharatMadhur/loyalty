# Service Layer for CRUD Operations

# Importing necessary queries and database connection
from data_end.sql_queries import (
    INSERT_USER_QUERY, GET_USER_QUERY, UPDATE_USER_QUERY, SOFT_DELETE_USER_QUERY,
    INSERT_STORE_QUERY, GET_STORE_QUERY,
    INSERT_OFFER_QUERY, GET_OFFERS_QUERY, UPDATE_OFFER_QUERY, DELETE_OFFER_QUERY,
    INSERT_CAMPAIGN_QUERY, GET_CAMPAIGN_QUERY, UPDATE_CAMPAIGN_QUERY, DELETE_CAMPAIGN_QUERY,
    INSERT_TRANSACTION_QUERY, GET_TRANSACTION_HISTORY_QUERY,
    INSERT_FEEDBACK_QUERY, GET_FEEDBACK_QUERY,
    INSERT_STORE_MEMBERSHIP_QUERY, GET_STORE_MEMBERSHIP_QUERY,
    INSERT_LOYALTY_CARD_QUERY, GET_LOYALTY_CARD_QUERY, UPDATE_LOYALTY_CARD_QUERY,
    VERIFY_SHOP_NAME_QUERY
)
from data_end.database import get_db_connection

# Users Service
class UserService:
    @staticmethod
    def create_user(user_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_USER_QUERY, user_data)
                conn.commit()

    @staticmethod
    def get_user(user_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_USER_QUERY, (user_id,))
                return cursor.fetchone()

    @staticmethod
    def update_user(user_data, user_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_USER_QUERY, user_data + (user_id,))
                conn.commit()

    @staticmethod
    def soft_delete_user(user_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(SOFT_DELETE_USER_QUERY, (user_id,))
                conn.commit()

# Stores Service
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

# Offers Service
class OfferService:
    @staticmethod
    def create_offer(offer_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_OFFER_QUERY, offer_data)
                conn.commit()

    @staticmethod
    def get_offers(store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_OFFERS_QUERY, (store_id,))
                return cursor.fetchall()

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

# Campaigns Service
class CampaignService:
    @staticmethod
    def create_campaign(campaign_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_CAMPAIGN_QUERY, campaign_data)
                conn.commit()

    @staticmethod
    def get_campaign(campaign_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_CAMPAIGN_QUERY, (campaign_id,))
                return cursor.fetchone()

    @staticmethod
    def update_campaign(campaign_data, campaign_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_CAMPAIGN_QUERY, campaign_data + (campaign_id,))
                conn.commit()

    @staticmethod
    def delete_campaign(campaign_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(DELETE_CAMPAIGN_QUERY, (campaign_id,))
                conn.commit()

# Transactions Service
class TransactionService:
    @staticmethod
    def create_transaction(transaction_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_TRANSACTION_QUERY, transaction_data)
                conn.commit()

    @staticmethod
    def get_transaction_history(store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_TRANSACTION_HISTORY_QUERY, (store_id,))
                return cursor.fetchall()

# Feedback Service
class FeedbackService:
    @staticmethod
    def submit_feedback(feedback_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_FEEDBACK_QUERY, feedback_data)
                conn.commit()

    @staticmethod
    def get_feedback(store_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_FEEDBACK_QUERY, (store_id,))
                return cursor.fetchall()

# Store Memberships Service
class StoreMembershipService:
    @staticmethod
    def create_store_membership(membership_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_STORE_MEMBERSHIP_QUERY, membership_data)
                conn.commit()

    @staticmethod
    def get_store_membership(store_id, customer_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_STORE_MEMBERSHIP_QUERY, (store_id, customer_id))
                return cursor.fetchone()

# Loyalty Cards Service
class LoyaltyCardService:
    @staticmethod
    def create_loyalty_card(card_data):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(INSERT_LOYALTY_CARD_QUERY, card_data)
                conn.commit()

    @staticmethod
    def get_loyalty_card(card_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(GET_LOYALTY_CARD_QUERY, (card_id,))
                return cursor.fetchone()

    @staticmethod
    def update_loyalty_card(card_data, card_id):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(UPDATE_LOYALTY_CARD_QUERY, card_data + (card_id,))
                conn.commit()

# Utility Service
class UtilityService:
    @staticmethod
    def verify_shop_name(store_id, shop_name):
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(VERIFY_SHOP_NAME_QUERY, (store_id, shop_name))
                return cursor.fetchone()
