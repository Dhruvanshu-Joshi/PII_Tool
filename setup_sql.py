import psycopg2
from psycopg2 import sql

# PostgreSQL Admin Configuration
ADMIN_DB_HOST = 'localhost'
ADMIN_DB_NAME = 'postgres'
ADMIN_DB_USER = 'postgres'  # Default superuser
ADMIN_DB_PASS = 'root123'  # Your postgres user password 

# App Database Configuration
DB_NAME = 'pii_database'

# Establish connection to the default 'postgres' database
def get_admin_connection():
    conn = psycopg2.connect(
        host=ADMIN_DB_HOST,
        database=ADMIN_DB_NAME,
        user=ADMIN_DB_USER,
        password=ADMIN_DB_PASS
    )
    return conn

# Grant required privileges to the existing user
def grant_permissions():
    try:
        # Connect to the default database as a superuser
        conn = get_admin_connection()
        conn.autocommit = True
        cur = conn.cursor()

        # Grant privileges on the existing database and public schema
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO postgres").format(sql.Identifier(DB_NAME)))
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON SCHEMA public TO postgres"))

        # Explicitly grant CREATE privilege on the schema
        cur.execute(sql.SQL("GRANT CREATE ON SCHEMA public TO postgres"))

        print(f"Granted privileges on {DB_NAME} and schema public to postgres.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error granting privileges: {e}")

# Connect to the new database as superuser
def get_app_connection():
    conn = psycopg2.connect(
        host=ADMIN_DB_HOST,
        database=DB_NAME,
        user=ADMIN_DB_USER,  # Connect as superuser
        password=ADMIN_DB_PASS
    )
    return conn

# Create the required table and insert data
def setup_table_and_insert_data():
    try:
        conn = get_app_connection()
        cur = conn.cursor()

        # Create pii_data table as superuser
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pii_data (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL
            );
        ''')
        print("Table pii_data created successfully.")

        # Insert data into the table as superuser
        cur.execute('''
            INSERT INTO pii_data (text) VALUES
            ('How can I reach you, Jim?'),
            ('As a democrat, I promise to uphold....'),
            ('As a Catholic, I can tell you that....'),
            ('Here is my contact information: Phone number 555-555-5555 and my email is example123@email.com'),
            ('Perfect, my number if you need me is 777-777-7777. Where is the residence and what is the earliest the crew can arrive?'),
            ('I''ll be at my home at 123 Dark Data Lane, OH, 11111 after 7PM'),
            ('Cool, I''ll be there!');
        ''')
        print("Data inserted successfully.")

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error creating table or inserting data: {e}")

# Main function to orchestrate the setup
def main():
    # Step 1: Grant privileges to the superuser (postgres)
    grant_permissions()

    # Step 2: Set up the table and insert data as superuser
    setup_table_and_insert_data()

if __name__ == '__main__':
    main()
