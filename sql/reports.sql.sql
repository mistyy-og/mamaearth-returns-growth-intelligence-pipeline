
SELECT 
    COUNT(*) AS total_orders,
    ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_revenue,
    ROUND(AVG(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS avg_order_value
FROM orders o
JOIN products p ON o.product_id = p.product_id;

output-- total_orders, total_revenue, avg_order_value
          153,	558.68	, 85477.90
SELECT 
    COUNT(*) AS total_rows,
    COUNT(rating) AS rated_rows,
    (COUNT(*) - COUNT(rating)) AS unrated_diff
FROM orders;

	total_rows	rated_rows	unrated_diff
	153	153	0


SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
Having COUNT(o.order_id) = 0;

output--	customer_id	name
	C045	Vihaan


SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM orders);

	customer_id	name
	C045	Vihaan
		
SELECT 
    c.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.returned) AS returned_orders,
    ROUND(SUM(o.returned) * 100.0 / COUNT(o.order_id), 1) AS return_rate_pct
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
HAVING return_rate_pct > 20
ORDER BY return_rate_pct DESC;

	city	total_orders	returned_orders	return_rate_pct
	Jaipur	19	8	42.1
	Lucknow	45	14	31.1


SELECT 
    c.customer_id,
    c.name,
    ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_spend
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;


SELECT 
    p.category,
    COUNT(o.order_id) AS order_count,
    ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS category_revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;

	category	order_count	category_revenue
	Haircare	46	37882.50
	Skincare	52	22657.40
	Babycare	26	15489.40
	PersonalCare	29	9448.60


SELECT * 
FROM customers 
WHERE name LIKE 'A%';

	customer_id	name	city	city_tier	signup_date	acquisition_source	loyalty_tier
	C001	Aarav	Mumbai	1	2026-01-07	Organic	
	C003	Aditi	Mumbai	1	2026-06-23	Organic	
	C004	Ananya	Lucknow	2	2026-01-23	Organic	
	C011	Arjun	Bangalore	1	2026-03-13	Referral	
	C021	Aryan	Bangalore	1	2026-02-11	Ad	
	C030	Anika	Bangalore	1	2026-02-24	Organic	
	C031	Aditya	Jaipur	2	2026-06-14	Ad	
	C036	Aisha	Delhi	1	2026-05-11	Ad	
	C041	Ayaan	Lucknow	2	2026-01-03	Organic	
	C044	Aria	Bangalore	1	2026-04-22	Referral	
							

SELECT DISTINCT acquisition_source 
FROM customers;

	acquisition_source
	Organic
	Referral
	Ad
	Social

ALTER TABLE customers ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers 
SET loyalty_tier = CASE WHEN city_tier = 1 THEN 'Gold' ELSE 'Silver' END;

SELECT loyalty_tier, COUNT(*) AS count 
FROM customers 
GROUP BY loyalty_tier;