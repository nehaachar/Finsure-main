CREATE DATABASE IF NOT EXISTS FinSure;
USE FinSure;

-- Temporary transaction table
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

-- User dimension table
CREATE TABLE dim_user (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(15)
);

-- Account dimension table
CREATE TABLE dim_account (
    account_id INT PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(50) CHECK (account_type IN ('Savings', 'Credit', 'Wallet')),
    bank_name VARCHAR(50),
    balance DECIMAL(12,2) DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
);

-- Category dimension table
CREATE TABLE dim_category (
    category_id VARCHAR(100) PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

-- Goal dimension table
CREATE TABLE dim_goal (
    goal_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    goal_name VARCHAR(100) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    current_amount DECIMAL(12,2) DEFAULT 0.0,
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
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


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dim_user.csv'
INTO TABLE dim_user
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(user_id, user_name, email, phone_number);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dim_account.csv'
INTO TABLE dim_account
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(account_id, user_id, account_type, bank_name, balance);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dim_category.csv'
INTO TABLE dim_category
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(category_id, name);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dim_goal.csv'
INTO TABLE dim_goal
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(goal_id, user_id, goal_name, target_amount, current_amount, target_date);

SELECT * FROM dim_user;
SELECT * FROM dim_account;
SELECT * FROM dim_category;
SELECT * FROM dim_goal;



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