import json

with open('transactions.json') as f:
    data = json.load(f)

import pandas as pd

df = pd.DataFrame(data)
df['transactionDate'] = pd.to_datetime(df['transactionDate']).dt.date

import mysql.connector

# ✅ Convert to DataFrame
df = pd.DataFrame(data)
df['transactionDate'] = pd.to_datetime(df['transactionDate']).dt.date

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Nithi18',
    database='FinSure'
)
cursor = conn.cursor()

# ✅ Create new table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transaction_json_import (
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

# ✅ Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO transaction_json_import (
            userID, username, accountID, transactionDate, category, amount, goal, type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# ✅ Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into transaction_json_import")



