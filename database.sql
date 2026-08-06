DROP DATABASE IF EXISTS finsight;
CREATE DATABASE finsight;
USE finsight;

-- Customers
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50)
);

-- Products
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- Orders
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    CONSTRAINT orders_ibfk_1
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
    ON DELETE CASCADE
);

-- Order Items
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),

    CONSTRAINT order_items_ibfk_1
    FOREIGN KEY (order_id)
    REFERENCES orders(order_id)
    ON DELETE CASCADE,

    CONSTRAINT order_items_ibfk_2
    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
    ON DELETE CASCADE
);

-- Sample Customers
INSERT INTO customers(customer_name,email,city,state)
VALUES
('Rahul','rahul@gmail.com','Jaipur','Rajasthan'),
('Aman','aman@gmail.com','Delhi','Delhi'),
('Priya','priya@gmail.com','Mumbai','Maharashtra');

-- Sample Products
INSERT INTO products(product_name,category,price,stock)
VALUES
('Laptop','Electronics',55000,15),
('Keyboard','Electronics',1200,50),
('Mouse','Electronics',700,70);

-- Sample Orders
INSERT INTO orders(customer_id,order_date,total_amount)
VALUES
(1,'2026-08-01',56200.00),
(2,'2026-08-02',2400.00),
(3,'2026-08-03',700.00);

-- Sample Order Items
INSERT INTO order_items(order_id,product_id,quantity,price)
VALUES
(1,1,1,55000.00),
(1,2,1,1200.00),
(2,2,2,1200.00),
(3,3,1,700.00);