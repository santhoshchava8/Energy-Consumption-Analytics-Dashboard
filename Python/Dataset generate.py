import pandas as pd
import numpy as np
#import random
from datetime import datetime, timedelta

# 1. Dim_Utility
# ---------------------------------------------------------
utility_data = {
    'Utility_Key': [1, 2, 3],
    'Utility_Type': ['Electricity', 'Gas', 'Water'],
    'Description': ['Standard household power', 'Heating and cooking supply', 'Water supply'],
    'Unit': ['kWh', 'm3', 'lt']
}
df_utility = pd.DataFrame(utility_data)

# 2. Dim_Vendor
# ---------------------------------------------------------
vendor_data = {
    'Vendor_Key': [1, 2, 3],
    'Vendor_Name': ['National Grid', 'Local Energy Co', 'Thames Water'],
    'Location': ['UK National', 'North East UK', 'Central UK'],
    'Reliability_Score': [95, 90, 99]
}
df_vendor = pd.DataFrame(vendor_data)

# 3. Dim_Customer (Expanded to 50 customers for better variance in 10k rows)
# ---------------------------------------------------------
# We will generate a mix of Residential and Commercial customers in North East locations
locations = ['Newcastle', 'Sunderland', 'Gateshead', 'Durham', 'Middlesbrough', 'London', 'Leeds']
segments = ['Residential', 'Commercial']
customer_list = []

for i in range(1, 51):
    segment = np.random.choice(segments, p=[0.8, 0.2]) # 80% Residential
    customer_list.append({
        'Customer_Key': i,
        'Customer_Name': f"{'Household' if segment == 'Residential' else 'Business'} {i}",
        'Customer_ID': f"C{i:03d}",
        'Location': np.random.choice(locations),
        'Segment': segment
    })
df_customer = pd.DataFrame(customer_list)

# 4. Dim_Calendar (Full year 2025 hourly/daily structure)
# ---------------------------------------------------------
# We will create a calendar for the full year 2025 to support the fact table
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='H') # Hourly resolution

calendar_list = []
for i, dt in enumerate(date_range, 1):
    calendar_list.append({
        'Date_Key': i,
        'Date': dt.strftime('%Y-%m-%d'),
        'Year': dt.year,
        'Month': dt.month,
        'Quarter': (dt.month - 1) // 3 + 1,
        'Day': dt.day,
        'Hour': dt.hour
    })
df_calendar = pd.DataFrame(calendar_list)

# 5. Fact_Consumption (10,000 Rows)
# ---------------------------------------------------------
num_rows = 100000

# Randomly sample keys for the foreign keys
# We select random dates from the calendar we just created
random_date_keys = np.random.choice(df_calendar['Date_Key'], num_rows)
random_customer_keys = np.random.choice(df_customer['Customer_Key'], num_rows)
random_utility_keys = np.random.choice(df_utility['Utility_Key'], num_rows)
random_vendor_keys = np.random.choice(df_vendor['Vendor_Key'], num_rows)

# Generate Consumption (Random float between 5.0 and 50.0)
consumption = np.round(np.random.uniform(5, 50, num_rows), 2)

# Calculate Cost, Revenue, Profit based on your rules
# Cost = £0.10/unit, Revenue = £0.15/unit
cost = np.round(consumption * 0.10, 2)
revenue = np.round(consumption * 0.15, 2)
profit = np.round(revenue - cost, 2)

fact_data = {
    'Read_ID': range(1, num_rows + 1),
    'Date_Key': random_date_keys,
    'Utility_Key': random_utility_keys,
    'Vendor_Key': random_vendor_keys,
    'Customer_Key': random_customer_keys,
    'Consumption_kWh': consumption,
    'Cost': cost,
    'Revenue': revenue,
    'Profit': profit
}
df_fact = pd.DataFrame(fact_data)

# Export to CSV
# ---------------------------------------------------------

export_path = r'C:\Users\chava\Projects\Energy-Consumption-Analytics-Dashboard\Storage'
df_utility.to_csv(export_path+'\Dim_Utility.csv', index=False)
df_vendor.to_csv(export_path+'\Dim_Vendor.csv', index=False)
df_customer.to_csv(export_path+'\Dim_Customer.csv', index=False)
df_calendar.to_csv(export_path+'\Dim_Calendar.csv', index=False)
df_fact.to_csv(export_path+'\Fact_Consumption.csv', index=False)

print(f"Files generated successfully. Fact table contains {len(df_fact)} rows.")
