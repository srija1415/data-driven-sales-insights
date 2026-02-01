import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams['figure.figsize'] = (10, 6)

# -----------------------------
# 1. Load Dataset
# -----------------------------
#df = pd.read_csv("superstore.csv")
df = pd.read_csv("superstore.csv", encoding="latin1")


print("Dataset Shape:", df.shape)
print(df.head())

# -----------------------------
# 2. Data Cleaning
# -----------------------------

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Check missing values
print("\nMissing Values:\n", df.isnull().sum())

# Drop duplicates
df.drop_duplicates(inplace=True)

# Create new columns
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Profit Margin'] = df['Profit'] / df['Sales']

print("\nCleaned Dataset Shape:", df.shape)

# -----------------------------
# 3. Sales Trend Analysis
# -----------------------------

sales_trend = df.groupby('Year')['Sales'].sum()

plt.figure()
sales_trend.plot(marker='o')
plt.title("Yearly Sales Trend")
plt.xlabel("Year")
plt.ylabel("Total Sales")
plt.show()

# -----------------------------
# 4. Category-wise Sales
# -----------------------------

plt.figure()
sns.barplot(x='Category', y='Sales', data=df, estimator=sum)
plt.title("Sales by Category")
plt.show()

# -----------------------------
# 5. Top 10 Products by Sales
# -----------------------------

top_products = (
    df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_products.plot(kind='barh')
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.show()

# -----------------------------
# 6. Region-wise Profit
# -----------------------------

plt.figure()
sns.barplot(x='Region', y='Profit', data=df, estimator=sum)
plt.title("Profit by Region")
plt.show()

# -----------------------------
# 7. Customer Analysis
# -----------------------------

customer_sales = (
    df.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
)

top_20_percent = int(0.2 * len(customer_sales))
revenue_share = (
    customer_sales.head(top_20_percent).sum()
    / customer_sales.sum()
) * 100

print(f"\nTop 20% customers contribute {revenue_share:.2f}% of revenue")

# -----------------------------
# 8. Business Insights
# -----------------------------

print("\nBUSINESS INSIGHTS:")
print("- Sales show clear yearly growth trends.")
print("- Technology category contributes highest revenue.")
print("- Few customers generate majority of revenue (Pareto principle).")
print("- Some regions generate high sales but low profit.")

monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()

plt.figure()
sns.lineplot(data=monthly_sales, x='Month', y='Sales', hue='Year', marker='o')
plt.title("Monthly Sales Trend by Year")
plt.show()

loss_products = df.groupby('Product Name')['Profit'].sum().sort_values()

print("\nTop 10 Loss-Making Products:")
print(loss_products.head(10))

plt.figure()
sns.scatterplot(x='Discount', y='Profit', data=df)
plt.title("Discount vs Profit Relationship")
plt.show()

customer_revenue = df.groupby('Customer Name')['Sales'].sum()

df['Customer Segment'] = df['Customer Name'].map(
    lambda x: 'High Value' if customer_revenue[x] > 5000
    else 'Medium Value' if customer_revenue[x] > 2000
    else 'Low Value'
)

print(df[['Customer Name', 'Customer Segment']].drop_duplicates().head())



