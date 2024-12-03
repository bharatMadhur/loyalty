import psycopg
from datetime import datetime, timezone

# Replace these with your actual database credentials
DATABASE_URL = "dbname=dreamseller user=postgres password=Madhur1997"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Create users table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id SERIAL PRIMARY KEY,
            details TEXT,
            frequency VARCHAR(20),
            audience TEXT,
            channel VARCHAR(20),
            type VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            shop_id INTEGER REFERENCES users(id) ON DELETE CASCADE  -- Associate with a specific shop
        );
        """)
        conn.commit()


