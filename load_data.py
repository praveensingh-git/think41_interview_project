import psycopg2
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to DB
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    print("✅ Successfully connected to the database.")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)

# Run schema.sql
try:
    with open('schema.sql', 'r') as f:
        cur.execute(f.read())
    print("✅ Tables created successfully.")
except Exception as e:
    print(f"❌ Error creating tables: {e}")

# Load users.csv
try:
    with open('users.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO users (user_id, first_name, last_name, email, gender, address, city, state, country, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """, (
                row['User Id'], row['First Name'], row['Last Name'], row['Email'],
                row['Gender'], row['Address'], row['City'], row['State'],
                row['Country'], row['Postal Code']
            ))
    print("✅ Users loaded successfully.")
except Exception as e:
    print(f"❌ Error loading users.csv: {e}")

# Load orders.csv
try:
    with open('orders.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO orders (order_id, user_id, product, quantity, price, status, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
            """, (
                row['Order Id'], row['User Id'], row['Product Name'], row['Quantity'],
                row['Price'], row['Status'], row['Order Date']
            ))
    print("✅ Orders loaded successfully.")
except Exception as e:
    print(f"❌ Error loading orders.csv: {e}")

# Commit
try:
    conn.commit()
    print("✅ Database changes committed.")
except Exception as e:
    print(f"❌ Commit failed: {e}")

cur.close()
conn.close()
print("✅ Database connection closed.")
print("✅ Data loading complete.")
