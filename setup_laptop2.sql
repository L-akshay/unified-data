-- Create the database
CREATE DATABASE IF NOT EXISTS source2_db;

-- Create user for central laptop
CREATE USER IF NOT EXISTS 'root'@'192.168.161.180' IDENTIFIED BY 'uyobaby123';

-- Grant privileges
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.161.180';

-- Create a sample table
USE source2_db;
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100),
    instructor VARCHAR(100),
    credits INT
);

FLUSH PRIVILEGES;
