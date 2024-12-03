import psycopg
from datetime import datetime

DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

# Function to add login_count column if it doesn't exist
def add_login_count_column():
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE store_owner_logins
                    ADD COLUMN IF NOT EXISTS login_count INT DEFAULT 0;
                """)
                connection.commit()
                print("login_count column added successfully!")
    except Exception as e:
        print(f"Error adding login_count column: {e}")

# Function to insert dummy data into store_owner_logins table
def insert_dummy_data_store_owner_logins():
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                dummy_data = [
                    (1, 'storeowner1', 'hashedpassword1', datetime.utcnow(), 5),
                    (2, 'storeowner2', 'hashedpassword2', datetime.utcnow(), 3),
                    (3, 'storeowner3', 'hashedpassword3', datetime.utcnow(), 10),
                    (4, 'storeowner4', 'hashedpassword4', datetime.utcnow(), 1),
                    (5, 'storeowner5', 'hashedpassword5', datetime.utcnow(), 0),
                ]
                insert_query = """
                    INSERT INTO store_owner_logins (store_id, username, hashed_password, last_login, login_count)
                    VALUES (%s, %s, %s, %s, %s)
                """
                for record in dummy_data:
                    cursor.execute(insert_query, record)
                connection.commit()
                print("Dummy data inserted into store_owner_logins successfully!")
    except Exception as e:
        print(f"Error inserting dummy data: {e}")

# Function to verify data in store_owner_logins table
def verify_store_owner_logins_data():
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM store_owner_logins;")
                records = cursor.fetchall()
                for record in records:
                    print(record)
    except Exception as e:
        print(f"Error verifying data: {e}")

# Run the functions
add_login_count_column()
insert_dummy_data_store_owner_logins()
verify_store_owner_logins_data()
