import psycopg2
import csv
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Database connection
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

# Step 1: Create tables
with open('schema.sql', 'r') as f:
    cur.execute(f.read())
print("✅ Tables created.")

# Step 2: Load users.csv
with open('users.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO users (user_id, first_name, last_name, email, gender, address, city, state, country, postal_code)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """, (
                row['user_id'], row['first_name'], row['last_name'], row['email'],
                row['gender'], row['address'], row['city'],
                row['state'], row['country'], row['postal_code']
            ))
        except Exception as e:
            print(f"[USER ERROR] {e} on row: {row}")

print("✅ Users loaded.")

# Step 3: Load orders.csv
with open('orders.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO orders (order_id, user_id, product, quantity, price, status, order_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
            """, (
                row['order_id'], row['user_id'], row['product'], row['quantity'],
                row['price'], row['status'], row['order_date']
            ))
        except Exception as e:
            print(f"[ORDER ERROR] {e} on row: {row}")

print("✅ Orders loaded.")

# Finalize
conn.commit()
cur.close()
conn.close()
print("✅ Data loading complete.")