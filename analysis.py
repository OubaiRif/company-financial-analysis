# =============================================================
# Company Financial Data Analysis
# Dataset: Synthetic company financial data (200 companies)
# Author: Oubai
# Description: Data exploration, cleaning, outlier detection,
#              summary statistics, and visualizations
# =============================================================

import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. LOAD DATA
# -------------------------------------------------------------

df = pd.read_csv('sample_company_data.csv')

# Check dataset dimensions (rows, columns)
print("Dataset shape:", df.shape)

# Preview first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Check column data types
print("\nColumn data types:")
print(df.dtypes)

# -------------------------------------------------------------
# 2. ADD DERIVED COLUMN
# -------------------------------------------------------------

# Calculate profit margin as a percentage of sales
df['profit_margin'] = (df['profits'] / df['sales']) * 100

# Confirm new column was added with correct data type
print("\nUpdated data types:")
print(df.dtypes)

# Preview profit margin values alongside key columns
print("\nProfit margin preview:")
print(df[['company_name', 'sales', 'profits', 'profit_margin']].head())

# -------------------------------------------------------------
# 3. SUMMARY STATISTICS
# -------------------------------------------------------------

# Calculate min, max, mean, median and count for numeric columns
stats = df[['sales', 'profits', 'assets', 'profit_margin']].agg(
    ['min', 'max', 'mean', 'median', 'count']
)

print("\nSummary statistics:")
print(stats.round(2))

# -------------------------------------------------------------
# 4. OUTLIER DETECTION
# -------------------------------------------------------------

# Flag rows where profits exceed sales (financially impossible)
# This indicates bad data in the synthetic dataset
df['data_quality_flag'] = df.apply(
    lambda row: 'OUTLIER' if row['profits'] > row['sales'] else 'OK',
    axis=1
)

# Display outliers
outliers = df[df['data_quality_flag'] == 'OUTLIER']
print(f"\nOutliers found: {len(outliers)}")
print(outliers[['company_name', 'sales', 'profits', 'profit_margin']])

# -------------------------------------------------------------
# 5. FILTER CLEAN DATA
# -------------------------------------------------------------

# Remove outliers for charting and further analysis
df_clean = df[df['data_quality_flag'] == 'OK']
print(f"\nClean dataset size: {len(df_clean)} companies")

# -------------------------------------------------------------
# 6. CHART 1 — TOP 10 COMPANIES BY PROFIT (BAR CHART)
# -------------------------------------------------------------

# Get top 10 companies by profit from clean data
top10 = df_clean.nlargest(10, 'profits')

plt.figure(figsize=(10, 6))
plt.bar(top10['company_name'], top10['profits'])
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Companies by Profit')
plt.xlabel('Company Name')
plt.ylabel('Profit ($)')
plt.ylim(0, None)  # Y-axis starts at 0 for honest representation

# Format y-axis numbers with comma separators
plt.gca().yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
)

plt.tight_layout()
plt.savefig('top_10_chart.png')
plt.show()

# -------------------------------------------------------------
# 7. CHART 2 — SALES VS PROFIT MARGIN (SCATTER PLOT)
# -------------------------------------------------------------

# Plot all 197 clean companies to explore relationship
# between sales volume and profit margin
plt.figure(figsize=(10, 6))
plt.scatter(df_clean['sales'], df_clean['profit_margin'], alpha=0.6)
plt.title('Sales vs Profit Margin')
plt.xlabel('Sales ($)')
plt.ylabel('Profit Margin (%)')
plt.ylim(0, None)  # Y-axis starts at 0 for honest representation

# Format x-axis numbers with comma separators
plt.gca().xaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
)

plt.tight_layout()
plt.savefig('profit_vs_sales.png')
plt.show()