CREATE DATABASE IF NOT EXISTS FinSure;
USE FinSure;

CREATE TABLE temp_transaction (
    transaction_id INT,
    user_id INT,
    account_id INT,
    transaction_date DATE,
    amount DECIMAL(10,2),
    category VARCHAR(100),
    type VARCHAR(50),
    goal VARCHAR(100)
);

CREATE TABLE dim_user (
    user_id INT PRIMARY KEY
);

CREATE TABLE dim_account (
    account_id INT PRIMARY KEY
);

CREATE TABLE dim_category (
    category VARCHAR(100) PRIMARY KEY
);

CREATE TABLE dim_goal (
    goal VARCHAR(100) PRIMARY KEY
);

CREATE TABLE dim_type (
    type VARCHAR(50) PRIMARY KEY
);


SHOW VARIABLES LIKE 'secure_file_priv';


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/new.csv'
INTO TABLE temp_transaction
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(userID, username, accountID, transactionDate, category, amount, goal, type);

select count( *) from temp_transaction;


INSERT IGNORE INTO dim_user (user_id)
SELECT DISTINCT userID FROM temp_transaction;

INSERT IGNORE INTO dim_account (account_id)
SELECT DISTINCT accountID FROM temp_transaction;

INSERT IGNORE INTO dim_category (category)
SELECT DISTINCT category FROM temp_transaction;

INSERT IGNORE INTO dim_goal (goal)
SELECT DISTINCT goal FROM temp_transaction;

INSERT IGNORE INTO dim_type (type)
SELECT DISTINCT type FROM temp_transaction;



SELECT 
    category,
    SUM(amount) AS total_spent
FROM temp_transaction
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;

SELECT 
    type,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND((SUM(amount) / (SELECT SUM(amount) FROM temp_transaction)) * 100, 2) AS percentage
FROM temp_transaction
GROUP BY type;

SELECT 
    transactionDate AS month,
    SUM(amount) AS total_amount
FROM temp_transaction
GROUP BY transactionDate
ORDER BY month;
select * from transaction_json_import;