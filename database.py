import psycopg

DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

def get_db_connection():
    try:
        return psycopg.connect(DATABASE_URL)
    except Exception as e:
        print("Unable to connect to the database", e)
        raise
