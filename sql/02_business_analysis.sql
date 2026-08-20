-- 1. Выручка и количество заказов по категориям

SELECT
	category,
	SUM(amount) AS total,
	COUNT(order_id) AS count
FROM orders
GROUP BY category 
ORDER BY total DESC, count DESC;

-- 2. Какие пользователи принесли больше всего выручки (топ 10)

SELECT
	user_id,
	COALESCE(SUM(amount), 0) AS total
FROM users u
LEFT JOIN orders o USING(user_id)
GROUP BY user_id
ORDER BY total DESC
LIMIT 10;

-- 3.Какие города наиболее прибыльные

SELECT
	city,
	COALESCE(SUM(amount), 0) AS total
FROM users u
LEFT JOIN orders o USING(user_id)
GROUP BY city
ORDER BY total DESC;

-- 4. Выручка по месяцам

SELECT
	DATE_TRUNC('month', order_date) AS order_month,
	COUNT(order_id) AS orders_count, 
	SUM(amount) AS revenue,
	AVG(amount) AS avg_order
FROM orders 
GROUP BY order_month
ORDER BY order_month

--5. Пользователи, которые совершили больше одного заказа

SELECT
	user_id,
	name,
	COUNT(order_id) AS orders_count,
	SUM(amount) AS total_revenue
FROM users 
JOIN orders USING(user_id)
GROUP BY user_id
HAVING COUNT(order_id) > 1;

--6. Самый дорогой заказ, который совершил каждый клиент

WITH RankAmount AS (
SELECT
	user_id,
	name,
	order_id, 
	amount, 
	DENSE_RANK() OVER(PARTITION BY user_id ORDER BY amount DESC) AS rank
FROM users 
JOIN orders USING(user_id)
)

SELECT 
	user_id,
	name,
	order_id, 
	amount
FROM RankAmount 
WHERE rank = 1;

--7. Какие источники привлечения клиентов наиболее эффективны

SELECT 
	source,
	COUNT(DISTINCT user_id) AS users_count,
	COUNT(order_id) AS orders_count,
	SUM(amount) AS revenue,
	ROUND(SUM(amount) / COUNT(DISTINCT user_id), 2) AS avg_revenue_per_user
FROM users
JOIN orders USING(user_id)
GROUP BY SOURCE
ORDER BY revenue DESC;








