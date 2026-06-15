import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('sample_company_data.csv')

print(df.shape)
print (df.head())
print(df.dtypes)

#create profit_margin column
df['profit_margin']=df['profits']/df['sales']*100
#testing code
print(df.dtypes)
print(df[['company_name', 'profits', 'sales', 'profit_margin']].head())
#create summery table with calculations
stats= df[['sales', 'profits', 'assets', 'profit_margin']].agg(['min','max','mean','median','count'])
print(stats.round(2))

#create a flag column for outliers
df['data_quality_flag']=df.apply(
    lambda row: 'OUTLIER' if row['profits'] > row['sales'] else 'OK', axis=1
)
outlier=df[df['data_quality_flag']=='OUTLIER']

print(f"outliers found: {len(outlier)}")
print(outlier[['company_name', 'sales','profits', 'profit_margin']])

#filter outliers
df_clean = df[df['data_quality_flag'] == 'OK']

#chart 1 - Top 10 by Profits
topten = df_clean.nlargest(10, 'profits')

plt.figure(figsize= (10,6))
plt.bar(topten['company_name'], topten['profits'])
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 companies by profit')
plt.xlabel('Company Name')
plt.ylabel('Profit ($)')
plt.ylim(0, None)
plt.gca().yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
)
plt.tight_layout()
plt.savefig('top_10_chart.png')
plt.show()

#Chart 2 - profit vs margin 
plt.figure(figsize= (10,6))
plt.scatter(df_clean['sales'], df_clean['profit_margin'])
plt.title('Profits vs. Sales Scatter Plot')
plt.xlabel('Sales ($)')
plt.ylabel('Profit Margin($)')
plt.ylim(0, None)
plt.gca().xaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda y, _: f'{y:,.0f}')
)
plt.gca().yaxis.set_major_formatter(
    plt.matplotlib.ticker.FuncFormatter(lambda x, _: f'{x:,.0f}')
)
plt.tight_layout()
plt.savefig('profit_vs_sales.png')
plt.show()