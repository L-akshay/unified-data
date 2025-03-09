-- Create the database
CREATE DATABASE IF NOT EXISTS source1_db;

-- Create user for central laptop
CREATE USER IF NOT EXISTS 'root'@'192.168.161.180' IDENTIFIED BY 'tiger';

-- Grant privileges
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.161.180';

-- Create a sample table
USE source1_db;
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    course VARCHAR(50)
);

FLUSH PRIVILEGES;
