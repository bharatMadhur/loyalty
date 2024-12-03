import psycopg

# Replace with your actual database connection URL
DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

def get_db():
    conn = psycopg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()
