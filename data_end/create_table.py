import psycopg

DATABASE_URL = "postgresql://postgres:Madhur1997@localhost:5432/dreamseller"

# List of table creation queries, ordered to respect dependencies
table_queries = [
    {
        "name": "users",
        "query": """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            user_type VARCHAR(50) NOT NULL,
            name VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(15),
            joined_at TIMESTAMPTZ,
            last_activity_at TIMESTAMPTZ,
            subscription_status VARCHAR(50),
            birthday DATE,
            city VARCHAR(255),
            referral_code VARCHAR(50),
            sign_up_channel VARCHAR(50),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "stores",
        "query": """
        CREATE TABLE IF NOT EXISTS stores (
            store_id SERIAL PRIMARY KEY,
            store_name VARCHAR(255) NOT NULL,
            branding JSONB,
            location VARCHAR(255),
            created_at TIMESTAMPTZ DEFAULT NOW(),
            POS VARCHAR(50),
            status VARCHAR(50),
            contact_person VARCHAR(255),
            parent_store_id INT REFERENCES stores(store_id)
        );
        """
    },
    {
        "name": "store_owner_logins",
        "query": """
        CREATE TABLE IF NOT EXISTS store_owner_logins (
            login_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            username VARCHAR(255) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            last_login TIMESTAMPTZ,
            login_count INT DEFAULT 0
        );
        """
    },
    {
        "name": "store_memberships",
        "query": """
        CREATE TABLE IF NOT EXISTS store_memberships (
            membership_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            customer_id INT REFERENCES users(user_id),
            membership_status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "loyalty_cards",
        "query": """
        CREATE TABLE IF NOT EXISTS loyalty_cards (
            card_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            customer_id INT REFERENCES users(user_id),
            verified BOOLEAN DEFAULT FALSE,
            source_verification VARCHAR(50),
            metadata JSONB,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "offers",
        "query": """
        CREATE TABLE IF NOT EXISTS offers (
            offer_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            conditions JSONB,
            expiry_date TIMESTAMPTZ,
            redemptions_total INT DEFAULT 0,
            redemptions_used INT DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "loyalty_performance",
        "query": """
        CREATE TABLE IF NOT EXISTS loyalty_performance (
            performance_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            card_id INT REFERENCES loyalty_cards(card_id),
            points_earned INT DEFAULT 0,
            points_redeemed INT DEFAULT 0,
            offers_used INT DEFAULT 0,
            transactions_count INT DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "campaigns",
        "query": """
        CREATE TABLE IF NOT EXISTS campaigns (
            campaign_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            name VARCHAR(255) NOT NULL,
            type VARCHAR(50),
            start_date TIMESTAMPTZ,
            end_date TIMESTAMPTZ,
            redemptions INT DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "transactions",
        "query": """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            location VARCHAR(255),
            menu_detail JSONB,
            transaction_no VARCHAR(50),
            transaction_amount DECIMAL(10, 2),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "feedback",
        "query": """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            message TEXT,
            rating INT CHECK (rating >= 1 AND rating <= 5),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "redeemable",
        "query": """
        CREATE TABLE IF NOT EXISTS redeemable (
            redemption_id SERIAL PRIMARY KEY,
            offer_id INT REFERENCES offers(offer_id),
            customer_id INT REFERENCES users(user_id),
            redeemed_at TIMESTAMPTZ
        );
        """
    },
    {
        "name": "campaign_stats",
        "query": """
        CREATE TABLE IF NOT EXISTS campaign_stats (
            stat_id SERIAL PRIMARY KEY,
            campaign_id INT REFERENCES campaigns(campaign_id),
            total_views INT DEFAULT 0,
            total_redemptions INT DEFAULT 0,
            conversion_rate DECIMAL(5, 2)
        );
        """
    },
    {
        "name": "notifications",
        "query": """
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES users(user_id),
            store_id INT REFERENCES stores(store_id),
            type VARCHAR(50),
            content TEXT,
            status VARCHAR(50),
            sent_at TIMESTAMPTZ
        );
        """
    },
    {
        "name": "email_templates",
        "query": """
        CREATE TABLE IF NOT EXISTS email_templates (
            template_id SERIAL PRIMARY KEY,
            store_id INT REFERENCES stores(store_id),
            name VARCHAR(255),
            content TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "card_notifications",
        "query": """
        CREATE TABLE IF NOT EXISTS card_notifications (
            notification_id SERIAL PRIMARY KEY,
            card_id INT REFERENCES loyalty_cards(card_id),
            content TEXT,
            status VARCHAR(50),
            sent_at TIMESTAMPTZ
        );
        """
    },
    {
        "name": "customer_activity",
        "query": """
        CREATE TABLE IF NOT EXISTS customer_activity (
            activity_id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES users(user_id),
            store_id INT REFERENCES stores(store_id),
            action VARCHAR(50),
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "store_analytics",
        "query": """
        CREATE TABLE IF NOT EXISTS store_analytics (
            store_id INT REFERENCES stores(store_id),
            metric VARCHAR(255),
            value DECIMAL(10, 2),
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "form_responses",
        "query": """
        CREATE TABLE IF NOT EXISTS form_responses (
            id SERIAL PRIMARY KEY,
            shop_id INT REFERENCES stores(store_id),
            response_data JSONB,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
    },
    {
        "name": "contact_submissions",
        "query": """
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            message TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
    }
]

# Function to create tables one by one
def create_tables():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            for table in table_queries:
                try:
                    print(f"Creating/Recreating table: {table['name']}")
                    cur.execute(f"DROP TABLE IF EXISTS {table['name']} CASCADE;")  # Drop the table to ensure clean slate
                    cur.execute(table['query'])  # Create the table
                    conn.commit()
                    print(f"Table {table['name']} created successfully!")
                except Exception as e:
                    conn.rollback()
                    print(f"Error creating table {table['name']}: {e}")

# Run the function
create_tables()
