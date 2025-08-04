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

with open('users.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            cur.execute("""
                INSERT INTO users (
                    user_id, first_name, last_name, email, gender, address, city, state, country, postal_code
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """, (
                int(row['id']),
                row['first_name'],
                row['last_name'],
                row['email'],
                row['gender'],
                row['street_address'],
                row['city'],
                row['state'],
                row['country'],
                row['postal_code']
            ))
        except Exception as e:
            print(f"⚠️ Skipped user {row.get('id', 'unknown')}: {e}")


# Load orders.csv
try:
    with open('orders.csv', newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        print("🔍 CSV Headers (orders.csv):", reader.fieldnames)

        for row in reader:
            try:
                cur.execute("""
                    INSERT INTO orders (order_id, user_id, product, quantity, price, status, order_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING
                """, (
                    row['order_id'], row['user_id'], "Unknown Product", row['num_of_item'],
                    0.0, row['status'], row['created_at']
                ))
            except psycopg2.Error as e:
                print(f"⚠️ Skipped order {row['order_id']}: {e.pgerror.strip()}")
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
