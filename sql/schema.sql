
CREATE DATABASE IF NOT EXISTS mamaearth_analytics;

USE mamaearth_analytics;

-- 1. Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    city VARCHAR(100),
    city_tier VARCHAR(30),
    signup_date DATE,
    acquisition_source VARCHAR(50)
);

-- 2. Products table
CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150),
    category VARCHAR(100),
    price DECIMAL(10, 2)
);

-- 3. Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20),
    product_id VARCHAR(20),
    order_date DATE,
    quantity INT,
    discount_pct DECIMAL(5, 2),
    payment_method VARCHAR(30),
    rating DECIMAL(3, 1),
    returned TINYINT(1),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_orders_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
