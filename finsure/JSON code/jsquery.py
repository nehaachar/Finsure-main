import mysql.connector
import pandas as pd

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Nithi18',
    database='FinSure'
)

# ✅ Top 5 Spending Categories
query1 = """
SELECT 
    category,
    SUM(amount) AS total_spent
FROM transaction_json_import
WHERE type = 'Expense'
GROUP BY category
ORDER BY total_spent DESC
LIMIT 5;
"""
df1 = pd.read_sql(query1, conn)
df1.to_csv('top spending_categories.csv', index=False)
print("✅ Top 5 Spending Categories saved to 'top_5_spending_categories.csv'")

# ✅ Savings Percentage
query2 = """
SELECT 
    type,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND((SUM(amount) / (SELECT SUM(amount) FROM transaction_json_import)) * 100, 2) AS percentage
FROM transaction_json_import
GROUP BY type;
"""
df2 = pd.read_sql(query2, conn)
df2.to_csv('savings_percentage.csv', index=False)
print("✅ Savings Percentage saved to 'savings_percentage.csv'")

# ✅ Monthly Burn Rate
query3 = """
SELECT 
    DATE_FORMAT(transactionDate, '%Y-%m') AS month,
    SUM(amount) AS total_spent
FROM transaction_json_import
WHERE type = 'Expense'
GROUP BY month
ORDER BY month;
"""
df3 = pd.read_sql(query3, conn)
df3.to_csv('monthly_burn_rate.csv', index=False)
print("✅ Monthly Burn Rate")
