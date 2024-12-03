import psycopg
from datetime import datetime, timedelta

DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

# Dummy data for tables
dummy_data = {
    "users": [
        ("customer", "John Doe", "john.doe@example.com", "1234567890", datetime.utcnow(), None, "active", None, "New York", "REF123", "online", datetime.utcnow()),
        ("customer", "Jane Smith", "jane.smith@example.com", "0987654321", datetime.utcnow(), None, "active", None, "Los Angeles", "REF456", "offline", datetime.utcnow()),
        ("customer", "Bob Johnson", "bob.johnson@example.com", "5556667777", datetime.utcnow(), None, "inactive", None, "Chicago", "REF789", "offline", datetime.utcnow()),
        ("customer", "Alice Brown", "alice.brown@example.com", "2223334444", datetime.utcnow(), None, "active", None, "Miami", "REF321", "online", datetime.utcnow()),
        ("customer", "Charlie Black", "charlie.black@example.com", "9998887777", datetime.utcnow(), None, "active", None, "San Francisco", "REF654", "online", datetime.utcnow()),
    ],
    "stores": [
        ("DreamStore NYC", '{"color": "blue"}', "New York", datetime.utcnow(), "Square", "active", "John Manager", None),
        ("DreamStore LA", '{"color": "red"}', "Los Angeles", datetime.utcnow(), "Clover", "active", "Jane Manager", None),
        ("DreamStore Chicago", '{"color": "green"}', "Chicago", datetime.utcnow(), "Toast", "active", "Bob Manager", None),
        ("DreamStore Miami", '{"color": "yellow"}', "Miami", datetime.utcnow(), "Square", "inactive", "Alice Manager", None),
        ("DreamStore SF", '{"color": "purple"}', "San Francisco", datetime.utcnow(), "Clover", "active", "Charlie Manager", None),
    ],
    "store_memberships": [
        (1, 1, "active", datetime.utcnow()),
        (2, 2, "active", datetime.utcnow()),
        (3, 3, "active", datetime.utcnow()),
        (4, 4, "inactive", datetime.utcnow()),
        (5, 5, "active", datetime.utcnow()),
    ],
    "loyalty_cards": [
        (1, 1, True, "email", '{"type": "premium"}', datetime.utcnow()),
        (2, 2, False, None, '{"type": "basic"}', datetime.utcnow()),
        (3, 3, True, "google", '{"type": "premium"}', datetime.utcnow()),
        (4, None, False, None, '{"type": "basic"}', datetime.utcnow()),
        (5, 5, True, "email", '{"type": "premium"}', datetime.utcnow()),
    ],
    "offers": [
        (1, "20% Discount", "20% discount for all members", '{"minimum_purchase": 50}', datetime.utcnow() + timedelta(days=30), 100, 20, datetime.utcnow()),
        (2, "Buy 1 Get 1 Free", "Buy one get one free on select items", '{"days": ["Monday", "Friday"]}', datetime.utcnow() + timedelta(days=60), 50, 10, datetime.utcnow()),
        (3, "Free Coffee", "Free coffee for loyalty card holders", '{"stores": [1, 3]}', datetime.utcnow() + timedelta(days=15), 200, 50, datetime.utcnow()),
        (4, "$10 Off", "$10 off on purchase over $100", '{"categories": ["electronics"]}', datetime.utcnow() + timedelta(days=45), 150, 60, datetime.utcnow()),
        (5, "15% Discount", "15% discount on clothing", '{"minimum_purchase": 30}', datetime.utcnow() + timedelta(days=20), 80, 25, datetime.utcnow()),
    ],
    "campaigns": [
        (1, "Summer Sale", "discount", datetime.utcnow(), datetime.utcnow() + timedelta(days=10), 0, datetime.utcnow()),
        (1, "Holiday Special", "email", datetime.utcnow(), datetime.utcnow() + timedelta(days=5), 0, datetime.utcnow()),
        (2, "Weekend Flash Sale", "sms", datetime.utcnow(), datetime.utcnow() + timedelta(days=7), 0, datetime.utcnow()),
        (3, "Black Friday", "email", datetime.utcnow(), datetime.utcnow() + timedelta(days=30), 0, datetime.utcnow()),
        (4, "Spring Collection", "discount", datetime.utcnow(), datetime.utcnow() + timedelta(days=20), 0, datetime.utcnow()),
    ],
    "transactions": [
        (1, "New York", '{"item": "Laptop"}', "TXN123", 1000.50, datetime.utcnow()),
        (2, "Los Angeles", '{"item": "Coffee"}', "TXN456", 5.00, datetime.utcnow()),
        (3, "Chicago", '{"item": "Phone"}', "TXN789", 300.00, datetime.utcnow()),
        (4, "Miami", '{"item": "Shoes"}', "TXN321", 50.75, datetime.utcnow()),
        (5, "San Francisco", '{"item": "Watch"}', "TXN654", 150.00, datetime.utcnow()),
    ],
    "feedback": [
        (1, "Great service!", 5, datetime.utcnow()),
        (2, "Good offers", 4, datetime.utcnow()),
        (3, "Average experience", 3, datetime.utcnow()),
        (4, "Poor quality", 2, datetime.utcnow()),
        (5, "Excellent products", 5, datetime.utcnow()),
    ],
}

# SQL Insert queries for tables
insert_queries = {
    "users": "INSERT INTO users (user_type, name, email, phone, joined_at, last_activity_at, subscription_status, birthday, city, referral_code, sign_up_channel, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "stores": "INSERT INTO stores (store_name, branding, location, created_at, POS, status, contact_person, parent_store_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
    "store_memberships": "INSERT INTO store_memberships (store_id, customer_id, membership_status, created_at) VALUES (%s, %s, %s, %s)",
    "loyalty_cards": "INSERT INTO loyalty_cards (store_id, customer_id, verified, source_verification, metadata, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
    "offers": "INSERT INTO offers (store_id, title, description, conditions, expiry_date, redemptions_total, redemptions_used, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
    "campaigns": "INSERT INTO campaigns (store_id, name, type, start_date, end_date, redemptions, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    "transactions": "INSERT INTO transactions (store_id, location, menu_detail, transaction_no, transaction_amount, created_at) VALUES (%s, %s, %s, %s, %s, %s)",
    "feedback": "INSERT INTO feedback (store_id, message, rating, created_at) VALUES (%s, %s, %s, %s)",
}

# Function to insert dummy data
def insert_dummy_data():
    try:
        connection = psycopg.connect(DATABASE_URL)
        cursor = connection.cursor()
        for table, records in dummy_data.items():
            for record in records:
                cursor.execute(insert_queries[table], record)
        connection.commit()
        print("Dummy data inserted successfully!")
    except Exception as e:
        print(f"Error inserting dummy data: {e}")
    finally:
        cursor.close()
        connection.close()

# Run the function to insert dummy data
insert_dummy_data()

# Function to verify all tables have data
def verify_data():
    try:
        connection = psycopg.connect(DATABASE_URL)
        cursor = connection.cursor()
        for table in dummy_data.keys():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table {table} has {count} records.")
    except Exception as e:
        print(f"Error verifying data: {e}")
    finally:
        cursor.close()
        connection.close()

# Run the function to verify data
verify_data()
