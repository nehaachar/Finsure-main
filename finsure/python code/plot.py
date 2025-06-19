import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set consistent style
sns.set(style="whitegrid")

# ============================
# 1️⃣ Top 5 Spending Categories → Bar Chart
# ============================
df1 = pd.read_csv("top_5_spending_categories.csv")
plt.figure(figsize=(8, 5))
sns.barplot(x='total_spent', y='category', data=df1, palette='viridis')
plt.title("Top 5 Spending Categories", fontsize=14)
plt.xlabel("Total Spent", fontsize=12)
plt.ylabel("Category", fontsize=12)
plt.tight_layout()
plt.savefig("top_5_spending_categories_bar.png")
plt.show()

# ============================
# 2️⃣ Spending vs Saving → Pie Chart
# ============================
df2 = pd.read_csv("spending_vs_saving_percentage.csv")
plt.figure(figsize=(6, 6))
plt.pie(
    df2['percentage'],
    labels=df2['type'],
    autopct='%1.1f%%',
    startangle=140,
    colors=['#ff9999', '#66b3ff']
)
plt.title("Spending vs Saving Percentage", fontsize=14)
plt.tight_layout()
plt.savefig("spending_vs_saving_percentage_pie.png")
plt.show()

# ============================
df3 = pd.read_csv("monthly_burn_rate.csv")
df3.columns = df3.columns.str.strip()  # clean column names
print("df3 columns:", df3.columns)

plt.figure(figsize=(10, 5))
sns.lineplot(x='month', y='total_spent', data=df3, marker='o', color='crimson')
plt.title("Monthly Burn Rate", fontsize=14)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Amount Spent", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_burn_rate_line.png")
plt.show()


