CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name TEXT,
    city TEXT,
    age INT,
    source TEXT,
    registered_at TIMESTAMP
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    order_date TIMESTAMP NOT NULL,
    category TEXT,
    amount NUMERIC(10,2) CHECK (amount >= 0),
    status TEXT
);