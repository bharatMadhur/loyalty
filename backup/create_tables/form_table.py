import psycopg

DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        # Create the form_responses table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS form_responses (
            id SERIAL PRIMARY KEY,
            shop_id INTEGER NOT NULL REFERENCES users(id),  -- Foreign key to associate with the logged-in user
            response_data JSONB NOT NULL,                   -- Store form responses as JSON
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """)
        conn.commit()
