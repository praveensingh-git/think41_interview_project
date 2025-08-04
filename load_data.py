import psycopg2
import csv
import os
from dotenv import load_dotenv

# Load .env variables from the environment.
# This keeps sensitive database credentials out of the code.
load_dotenv()

def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    The connection details are loaded from environment variables.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Successfully connected to the database.")
        return conn
    except Exception as e:
        print(f"❌ Error connecting to the database: {e}")
        return None

def create_tables(cur):
    """
    Executes the SQL schema from 'schema.sql' to create database tables.
    """
    try:
        with open('schema.sql', 'r') as f:
            cur.execute(f.read())
        print("✅ Tables created or already exist.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

def load_data(cur, file_path, table_name, columns, conflict_column):
    """
    Loads data from a CSV file into a specified database table using bulk insertion.
    This is much more efficient than row-by-row insertion.
    """
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data_to_insert = [
                tuple(row[col] for col in columns) for row in reader
            ]

        # Build the dynamic INSERT statement with ON CONFLICT clause
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)
        insert_sql = f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders})
            ON CONFLICT ({conflict_column}) DO NOTHING
        """
        
        cur.executemany(insert_sql, data_to_insert)
        print(f"✅ Data from '{file_path}' loaded into '{table_name}'.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"❌ Error loading data from '{file_path}': {e}")


def main():
    """
    Main function to orchestrate the data loading process.
    Uses context managers for automatic resource cleanup.
    """
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            # Step 1: Create tables
            create_tables(cur)
            
            # Step 2: Load users.csv using bulk insertion
            user_columns = [
                'user_id', 'first_name', 'last_name', 'email', 'gender',
                'address', 'city', 'state', 'country', 'postal_code'
            ]
            load_data(cur, 'users.csv', 'users', user_columns, 'user_id')
            
            # Step 3: Load orders.csv using bulk insertion
            order_columns = [
                'order_id', 'user_id', 'product', 'quantity',
                'price', 'status', 'order_date'
            ]
            load_data(cur, 'orders.csv', 'orders', order_columns, 'order_id')
            
            # Commit the transaction to save changes to the database
            conn.commit()
            print("✅ Database changes committed.")

    except Exception as e:
        # Rollback the transaction on error
        conn.rollback()
        print(f"❌ An unexpected error occurred. Rolling back transaction: {e}")
    finally:
        # Ensure the connection is always closed
        if conn:
            conn.close()
            print("✅ Database connection closed.")
        
    print("✅ Data loading complete.")

if __name__ == '__main__':
    main()
