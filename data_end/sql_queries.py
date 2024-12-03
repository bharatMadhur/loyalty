# Users Table Queries
INSERT_USER_QUERY = """
INSERT INTO users (user_type, name, email, phone, joined_at, last_activity_at, subscription_status, birthday, city, referral_code, sign_up_channel, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_USER_QUERY = """
SELECT * FROM users WHERE user_id = %s
"""

UPDATE_USER_QUERY = """
UPDATE users SET name = %s, email = %s, phone = %s, subscription_status = %s, city = %s, referral_code = %s, sign_up_channel = %s, last_activity_at = %s
WHERE user_id = %s
"""

SOFT_DELETE_USER_QUERY = """
UPDATE users SET subscription_status = 'deleted' WHERE user_id = %s
"""

#### **Store Table Queries**
#
# Stores Table Queries
INSERT_STORE_QUERY = """
INSERT INTO stores (store_name, branding, location, created_at, POS, status, contact_person, parent_store_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_STORE_QUERY = """
SELECT * FROM stores WHERE store_id = %s
"""

UPDATE_STORE_QUERY = """
UPDATE stores SET store_name = %s, branding = %s, location = %s, POS = %s, status = %s, contact_person = %s
WHERE store_id = %s
"""

DELETE_STORE_QUERY = """
DELETE FROM stores WHERE store_id = %s
"""

#### **Offers Table Queries**
#
# Offers Table Queries
INSERT_OFFER_QUERY = """
INSERT INTO offers (store_id, title, description, conditions, expiry_date, redemptions_total, redemptions_used, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

GET_OFFERS_QUERY = """
SELECT * FROM offers WHERE store_id = %s
"""

UPDATE_OFFER_QUERY = """
UPDATE offers SET title = %s, description = %s, conditions = %s, expiry_date = %s, redemptions_total = %s, redemptions_used = %s
WHERE offer_id = %s AND store_id = %s
"""

DELETE_OFFER_QUERY = """
DELETE FROM offers WHERE offer_id = %s AND store_id = %s
"""

#### **Campaigns Table Queries**
#
# Campaigns Table Queries
INSERT_CAMPAIGN_QUERY = """
INSERT INTO campaigns (store_id, name, type, start_date, end_date, redemptions, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

GET_CAMPAIGN_QUERY = """
SELECT * FROM campaigns WHERE campaign_id = %s
"""

UPDATE_CAMPAIGN_QUERY = """
UPDATE campaigns SET name = %s, type = %s, start_date = %s, end_date = %s, redemptions = %s
WHERE campaign_id = %s
"""

DELETE_CAMPAIGN_QUERY = """
DELETE FROM campaigns WHERE campaign_id = %s
"""

#### **Transactions Table Queries**
#
# Transactions Table Queries
INSERT_TRANSACTION_QUERY = """
INSERT INTO transactions (store_id, location, menu_detail, transaction_no, transaction_amount, created_at)
VALUES (%s, %s, %s, %s, %s, %s)
"""

GET_TRANSACTION_HISTORY_QUERY = """
SELECT * FROM transactions WHERE store_id = %s
"""

#### **Feedback Table Queries**
#
# Feedback Table Queries
INSERT_FEEDBACK_QUERY = """
INSERT INTO feedback (store_id, message, rating, created_at)
VALUES (%s, %s, %s, %s)
"""

GET_FEEDBACK_QUERY = """
SELECT * FROM feedback WHERE store_id = %s
"""

#### **Store Memberships Table Queries**
#
# Store Memberships Table Queries
INSERT_STORE_MEMBERSHIP_QUERY = """
INSERT INTO store_memberships (store_id, customer_id, membership_status, created_at)
VALUES (%s, %s, %s, %s)
"""

GET_STORE_MEMBERSHIP_QUERY = """
SELECT * FROM store_memberships WHERE store_id = %s AND customer_id = %s
"""

#### **Loyalty Cards Table Queries**
#
# Loyalty Cards Table Queries
INSERT_LOYALTY_CARD_QUERY = """
INSERT INTO loyalty_cards (store_id, customer_id, verified, source_verification, metadata, created_at)
VALUES (%s, %s, %s, %s, %s, %s)
"""

GET_LOYALTY_CARD_QUERY = """
SELECT * FROM loyalty_cards WHERE card_id = %s
"""

UPDATE_LOYALTY_CARD_QUERY = """
UPDATE loyalty_cards SET verified = %s, source_verification = %s, metadata = %s
WHERE card_id = %s
"""

DELETE_LOYALTY_CARD_QUERY = """
DELETE FROM loyalty_cards WHERE card_id = %s
"""

#### **General Utility Queries**
#
# General Utility Queries
VERIFY_SHOP_NAME_QUERY = """
SELECT * FROM stores WHERE store_id = %s AND store_name = %s
"""

GET_OFFER_QUERY = """
SELECT * FROM offers WHERE offer_id = %s
"""

# Get a specific transaction by transaction ID
GET_TRANSACTION_QUERY = """
SELECT * FROM transactions WHERE transaction_id = %s
"""
# Update a transaction record by transaction ID
UPDATE_TRANSACTION_QUERY = """
UPDATE transactions SET location = %s, menu_detail = %s, transaction_no = %s, transaction_amount = %s
WHERE transaction_id = %s
"""

# Delete a specific transaction by transaction ID
DELETE_TRANSACTION_QUERY = """
DELETE FROM transactions WHERE transaction_id = %s
"""

# Update a feedback record by feedback ID
UPDATE_FEEDBACK_QUERY = """
UPDATE feedback SET message = %s, rating = %s
WHERE feedback_id = %s
"""

# Delete a specific feedback by feedback ID
DELETE_FEEDBACK_QUERY = """
DELETE FROM feedback WHERE feedback_id = %s
"""




