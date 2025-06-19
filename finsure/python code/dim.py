import pandas as pd
import mysql.connector

# ✅ Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Nithi18',
    database='FinSure'
)
cursor = conn.cursor()

# ✅ Drop tables in reverse FK dependency order
cursor.execute("DROP TABLE IF EXISTS dim_account")
cursor.execute("DROP TABLE IF EXISTS dim_goal")
cursor.execute("DROP TABLE IF EXISTS dim_category")
cursor.execute("DROP TABLE IF EXISTS dim_user")

# ✅ Create dim_user table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_user (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL
)
""")

# ✅ Create dim_category table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_category (
    category_id VARCHAR(100) PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
)
""")

# ✅ Create dim_goal table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_goal (
    goal_id VARCHAR(50) PRIMARY KEY,
    goal_name VARCHAR(100) NOT NULL,
    user_id INT,
    target_amount DECIMAL(12,2) NOT NULL,
    target_date DATE,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
)
""")

# ✅ Create dim_account table
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_account (
    account_id VARCHAR(50) PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(50) CHECK (account_type IN ('Savings', 'Credit', 'Wallet')),
    bank_name VARCHAR(50),
    balance DECIMAL(12,2) DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id)
)
""")

# ✅ Insert into dim_user
df_user = pd.read_csv("users.csv")  # Columns: UserID, UserName
for _, row in df_user.iterrows():
    cursor.execute("""
        INSERT INTO dim_user (user_id, user_name)
        VALUES (%s, %s)
    """, (row['UserID'], row['UserName']))

# ✅ Insert into dim_category
df_category = pd.read_csv("categories.csv")  # Columns: CategoryID, CategoryName
for _, row in df_category.iterrows():
    cursor.execute("""
        INSERT INTO dim_category (category_id, category_name)
        VALUES (%s, %s)
    """, (row['CategoryID'], row['CategoryName']))

# ✅ Insert into dim_goal
df_goal = pd.read_csv("goals.csv")  # Columns: GoalID, GoalName, UserID, TargetAmount, TargetDate
df_goal['TargetDate'] = pd.to_datetime(df_goal['TargetDate']).dt.date
for _, row in df_goal.iterrows():
    cursor.execute("""
        INSERT INTO dim_goal (goal_id, goal_name, user_id, target_amount, target_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['GoalID'], row['GoalName'], row['UserID'], row['TargetAmount'], row['TargetDate']))

# ✅ Insert into dim_account with validation
df_account = pd.read_csv("accounts.csv")  # Columns: AccountID, UserID, AccountType, BankName, Balance
df_account['AccountType'] = df_account['AccountType'].str.strip().str.title()
valid_types = ['Savings', 'Credit', 'Wallet']

for _, row in df_account.iterrows():
    if row['AccountType'] not in valid_types:
        continue
    cursor.execute("""
        INSERT INTO dim_account (account_id, user_id, account_type, bank_name, balance)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['AccountID'], row['UserID'], row['AccountType'], row['BankName'], row['Balance']))

# ✅ Commit and close

query = "SELECT * FROM dim_user"  
df = pd.read_sql(query, conn)
print(df)

query = "SELECT * FROM dim_category"  
df = pd.read_sql(query, conn)
print(df)

query = "SELECT * FROM dim_account"  
df = pd.read_sql(query, conn)
print(df)

query = "SELECT * FROM dim_goal"  
df = pd.read_sql(query, conn)
print(df)

conn.commit()
cursor.close()
conn.close()

print("✅ All dimension tables created and inserted successfully.")


