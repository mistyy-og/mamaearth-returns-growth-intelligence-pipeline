
USE mamaearth_analytics;

-- Load customers from customers.csv
LOAD DATA LOCAL INFILE 'data/customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(customer_id, name, city, city_tier, signup_date, acquisition_source);

-- Load products from products.csv
LOAD DATA LOCAL INFILE 'data/products.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(product_id, product_name, category, price);

-- Load orders from orders.csv
LOAD DATA LOCAL INFILE 'data/orders.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, customer_id, product_id, order_date, quantity,
 discount_pct, payment_method, rating, returned);
