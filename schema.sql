DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT, 
    gender TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    postal_code TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    product TEXT,
    quantity INT,
    price NUMERIC,
    status TEXT,
    order_date DATE
);
