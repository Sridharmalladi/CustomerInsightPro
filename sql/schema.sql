
# sql/schema.sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    join_date DATE,
    segment VARCHAR(50),
    lifetime_value DECIMAL(10,2)
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    date TIMESTAMP,
    amount DECIMAL(10,2),
    product_category VARCHAR(50),
    channel VARCHAR(50)
);

CREATE TABLE customer_patterns (
    pattern_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    purchase_frequency INTEGER,
    avg_basket_size DECIMAL(10,2),
    preferred_category VARCHAR(50),
    last_purchase_date DATE
);

# sql/analysis_queries.sql
-- Customer Segmentation
CREATE VIEW customer_segments AS
SELECT 
    c.customer_id,
    COUNT(t.transaction_id) as total_transactions,
    SUM(t.amount) as total_spent,
    AVG(t.amount) as avg_transaction,
    MAX(t.date) as last_purchase
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
GROUP BY c.customer_id;

-- Pattern Analysis
CREATE VIEW consumption_patterns AS
SELECT 
    customer_id,
    product_category,
    COUNT(*) as purchase_count,
    AVG(amount) as avg_amount,
    MAX(date) as last_purchase
FROM transactions
GROUP BY customer_id, product_category;