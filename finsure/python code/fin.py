import pandas as pd
import mysql.connector

# ✅ Load CSV File
df = pd.read_csv("new.csv")

# ✅ Format date
df['transactionDate'] = pd.to_datetime(df['transactionDate']).dt.date

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Nithi18',
    database='FinSure'
)
cursor = conn.cursor()

# ✅ Create database and tables
cursor.execute("CREATE DATABASE IF NOT EXISTS FinSure")
cursor.execute("USE FinSure")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    username VARCHAR(100),
    accountID INT,
    transactionDate DATE,
    category VARCHAR(100),
    amount DECIMAL(10,2),
    goal VARCHAR(100),
    type VARCHAR(50)
)
""")

cursor.execute("CREATE TABLE IF NOT EXISTS dim1_user (user_id INT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS dim1_account (account_id INT PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS dim1_category (category VARCHAR(100) PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS dim1_goal (goal VARCHAR(100) PRIMARY KEY)")
cursor.execute("CREATE TABLE IF NOT EXISTS dim1_type (type VARCHAR(50) PRIMARY KEY)")

# ✅ Insert into transaction table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO transaction (userID, username, accountID, transactionDate, category, amount, goal, type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()

# ✅ Populate dimension tables from transaction
cursor.execute("INSERT IGNORE INTO dim1_user (user_id) SELECT DISTINCT userID FROM transaction")
cursor.execute("INSERT IGNORE INTO dim1_account (account_id) SELECT DISTINCT accountID FROM transaction")
cursor.execute("INSERT IGNORE INTO dim1_category (category) SELECT DISTINCT category FROM transaction")
cursor.execute("INSERT IGNORE INTO dim1_goal (goal) SELECT DISTINCT goal FROM transaction")
cursor.execute("INSERT IGNORE INTO dim1_type (type) SELECT DISTINCT type FROM transaction")
conn.commit()

# ✅ Top 5 Spending Categories
query1 = """
SELECT category, SUM(amount) AS total_spent
FROM transaction
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5
"""
df1 = pd.read_sql(query1, conn)
df1.to_csv("top_5_spending_categories.csv", index=False)
print("\n✅ top_5_spending_categories.csv saved")

# ✅ Spending vs Saving Percentage
query2 = """
SELECT 
    type,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND((SUM(amount) / (SELECT SUM(amount) FROM transaction)) * 100, 2) AS percentage
FROM transaction
GROUP BY type
"""
df2 = pd.read_sql(query2, conn)
df2.to_csv("spending_vs_saving_percentage.csv", index=False)
print("✅ spending_vs_saving_percentage.csv saved")

# ✅ Monthly Burn Rate
query3 = """
SELECT 
    DATE_FORMAT(transactionDate, '%Y-%m') AS month,
    SUM(amount) AS total_amount
FROM transaction
GROUP BY month
ORDER BY month
"""
df3 = pd.read_sql(query3, conn)
df3.to_csv("monthly_burn_rate.csv", index=False)
print("✅ monthly_burn_rate.csv saved")

# ✅ Close connections
cursor.close()
conn.close()
