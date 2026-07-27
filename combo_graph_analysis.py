import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Load the data
df = pd.read_csv('data/prepared/customers_data_prepared_cjjade.csv')

# Convert JoinDate to datetime
df['JoinDate'] = pd.to_datetime(df['JoinDate'])

# Extract year and month for grouping
df['YearMonth'] = df['JoinDate'].dt.to_period('M')
df['Year'] = df['JoinDate'].dt.year

# Create a cross-tabulation of join dates and payment types
payment_by_date = pd.crosstab(df['YearMonth'], df['DefaultPaymentType'])

# Create figure with subplots for combo visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: Stacked Area Chart - Payment Types Over Time
ax1 = axes[0]
payment_by_date.plot(kind='area', stacked=True, ax=ax1, alpha=0.7, 
                     color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
ax1.set_title('Payment Type Distribution Over Join Dates (Stacked Area)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Join Date (Year-Month)', fontsize=11)
ax1.set_ylabel('Number of Customers', fontsize=11)
ax1.legend(title='Payment Type', bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Combination of Line Chart + Bar Chart
ax2 = axes[1]

# Calculate total customers by month
total_by_month = df.groupby('YearMonth').size()

# Create bar chart for total customers
ax2.bar(range(len(total_by_month)), total_by_month.values, alpha=0.6, color='skyblue', label='Total Customers')

# Overlay line chart for most common payment type
payment_counts = df.groupby(['YearMonth', 'DefaultPaymentType']).size().unstack(fill_value=0)
most_common = payment_counts.idxmax(axis=1)

# Create line chart for Credit/Debit trend (most common)
credit_debit_data = df[df['DefaultPaymentType'] == 'Credit/Debit'].groupby('YearMonth').size()
ax2_twin = ax2.twinx()
ax2_twin.plot(range(len(credit_debit_data)), credit_debit_data.values, 'ro-', linewidth=2.5, 
              markersize=6, label='Credit/Debit Transactions')

ax2.set_title('Customer Join Dates vs Payment Type Trends (Combo: Bars + Line)', fontsize=14, fontweight='bold')
ax2.set_xlabel('Join Date (Year-Month)', fontsize=11)
ax2.set_ylabel('Total Customers (Bar)', fontsize=11, color='skyblue')
ax2_twin.set_ylabel('Credit/Debit Customers (Line)', fontsize=11, color='red')
ax2.set_xticks(range(len(total_by_month)))
ax2.set_xticklabels(total_by_month.index.astype(str), rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

# Add legends
ax2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')

plt.tight_layout()
plt.savefig('join_date_payment_combo_graph.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary statistics
print("=" * 60)
print("SUMMARY: Join Dates vs Payment Types Analysis")
print("=" * 60)
print(f"\nTotal Customers: {len(df)}")
print(f"\nPayment Type Distribution:")
print(df['DefaultPaymentType'].value_counts())
print(f"\nCustomers by Year:")
print(df['Year'].value_counts().sort_index())
print(f"\nPayment Type by Join Month:")
print(payment_by_date)
