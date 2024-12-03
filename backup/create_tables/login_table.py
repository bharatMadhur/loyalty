import psycopg
from datetime import datetime, timezone

# Replace these with your actual database credentials
DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            shop_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            login_count INTEGER DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        """)
        conn.commit()


