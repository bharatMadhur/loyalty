import psycopg
from datetime import datetime, timezone

# Replace these with your actual database credentials
DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Create users table
        cur.execute("""
        CREATE TABLE contact_submissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

        """)
        conn.commit()


