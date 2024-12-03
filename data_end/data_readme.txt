users:
Purpose: Stores global user information for customers, store owners, and admins.
Data: User type (customer/store owner), contact info, registration date, joined_at, last_activity_at, subscription_status, birthday, city, referral_code, sign_up_channel.

#################################################################################

stores:
Purpose: Holds details about participating stores.
Data: Store name, branding, location, created_at, POS, status, contact_person.
Logic: To handle brands with multiple stores, a `parent_store_id` field links sub-stores to a master store.

#################################################################################

store_memberships:
Purpose: Tracks customers’ association with stores.
Data: Store ID, customer ID, membership status.

#################################################################################

loyalty_cards:
Purpose: Tracks V1 (unverified) and V2 (verified) loyalty cards.
Data: Card ID, store ID, customer ID (nullable for V1), verification status, source of verification.

#################################################################################

offers:
Purpose: Stores active and upcoming store-specific offers.
Data: Offer title, description, conditions, expiration date, redemptions (total and used).

#################################################################################

loyalty_performance:
Purpose: Tracks loyalty card activity and effectiveness.
Data: Points earned/redeemed, offers used, transactions count.

#################################################################################

campaigns:
Purpose: Manages marketing campaigns created by store owners.
Data: Campaign name, type (email/card notification), start and end dates, campaign stats (e.g., total redemptions, views, etc.).

#################################################################################

transactions:
Purpose: Logs purchases and links them to loyalty activities.
Data: Store ID (location-specific), menu_detail (from POS), transaction_no, transaction_amount, transaction_id, timestamp.

#################################################################################

feedback:
Purpose: Collects feedback from customers about stores and services.
Data: Store ID, message, rating.

#################################################################################

redeemable/redemptions:
Purpose: Tracks items or offers that can be redeemed and their statuses.
Data: Redemption ID, offer/campaign ID, customer ID, redeemed_at.

#################################################################################

campaign_stats:
Purpose: Tracks detailed statistics for campaigns.
Data: Campaign ID, total views, total redemptions, conversion rate.

#################################################################################

store_owner_logins:
Purpose: Manages credentials for store owners.
Data: Username, hashed password, last login.

#################################################################################

customer_logins:
Purpose: Tracks Google-based or id_password logins for customers.
Data: Login type, authentication token, registration date.

#################################################################################

notifications:
Purpose: Tracks email or card notifications sent to customers.
Data: Notification type, content, status, sent timestamp.

#################################################################################

email_templates:
Purpose: Stores reusable email designs for campaigns.
Data: Template content, linked store ID, created date.

#################################################################################

card_notifications:
Purpose: Logs push notifications sent to digital wallet cards.
Data: Notification content, delivery status, timestamp.

#################################################################################

customer_activity:
Purpose: Tracks customer interactions like logging in or redeeming rewards.
Data: Activity type, customer ID, store ID, timestamp.

#################################################################################

store_analytics:
Purpose: Aggregates store-level metrics such as campaign success and loyalty usage.
Data: Store ID, metric name, value, timestamp.

#################################################################################

form_responses:
Purpose: Stores form data submitted by shops or customers, structured as JSON.
Data: Form response data (JSONB), shop reference (shop_id), timestamp.

#################################################################################

contact_submissions:
Purpose: Stores customer inquiries or feedback submitted via forms.
Data: Name, email, message, and timestamp.
