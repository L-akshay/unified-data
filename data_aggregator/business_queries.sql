-- 1. Monthly Sales Performance Report
-- Run on remote database
SELECT 
    DATE_FORMAT(s.sale_date, '%Y-%m') as month,
    p.category,
    COUNT(*) as total_sales,
    SUM(s.quantity) as units_sold,
    SUM(s.total_amount) as revenue,
    c.country
FROM sales s
JOIN products p ON s.product_id = p.product_id
JOIN customers c ON s.customer_id = c.customer_id
GROUP BY DATE_FORMAT(s.sale_date, '%Y-%m'), p.category, c.country
ORDER BY month;

-- 2. Inventory Status Report
-- Run on remote database
SELECT 
    p.category,
    COUNT(*) as product_count,
    SUM(p.stock_quantity) as total_stock,
    SUM(p.stock_quantity * p.unit_price) as inventory_value
FROM products p
GROUP BY p.category;

-- 3. Department Performance Analysis
-- Run on central database
SELECT 
    d.dept_name,
    COUNT(e.emp_id) as employee_count,
    d.budget,
    d.location,
    AVG(e.salary) as avg_salary
FROM departments d
LEFT JOIN employees e ON d.dept_name = e.department
GROUP BY d.dept_name, d.budget, d.location;

-- 4. Customer Geographic Distribution
-- Run on remote database
SELECT 
    c.country,
    COUNT(DISTINCT c.customer_id) as customer_count,
    COUNT(s.sale_id) as total_orders,
    SUM(s.total_amount) as total_revenue
FROM customers c
LEFT JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.country;

-- 5. Product Performance by Department
-- Requires joining data from both databases using application logic
-- First, get sales data (remote):
SELECT 
    p.category,
    p.product_name,
    SUM(s.quantity) as units_sold,
    SUM(s.total_amount) as revenue
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category, p.product_name;

-- Then, get department data (central):
SELECT 
    d.dept_name,
    d.budget,
    COUNT(e.emp_id) as team_size
FROM departments d
LEFT JOIN employees e ON d.dept_name = e.department
GROUP BY d.dept_name, d.budget;
