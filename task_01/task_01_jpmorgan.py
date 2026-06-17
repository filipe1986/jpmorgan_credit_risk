import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('nat_gas.csv') # creating a dataframe
df.columns = df.columns.str.lower() # changing all column names to lowercase
df['dates'] = pd.to_datetime(df['dates']) # changing the dates columns from str to datetime64

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df['dates'], df['prices'], label='prices', color='blue', linewidth=2)
ax.set(
    title='Prices over time',
    xlabel='dates',
    ylabel='prices'
)
ax.legend()
ax.grid(True)
plt.tight_layout()
#plt.show()

df.set_index('dates', inplace=True) # now, the dates column will be the index

daily_df = df.resample('D').interpolate(method='linear')

# creating a numerical time variable representing the number of days since the start
daily_df['days_since_start'] = (daily_df.index - daily_df.index.min()).days

slope, intercept, r_value, p_value, std_err = linregress(daily_df['days_since_start'], daily_df['prices'])

# calculating the baseline trend price for every historical day
daily_df['trend_price'] = intercept + slope * daily_df['days_since_start']

# finding the deviation 
daily_df['deviation'] = daily_df['prices'] - daily_df['trend_price']

# grouping by month to get the average seasonal kick for each month (1 to 12)
daily_df['month'] = daily_df.index.month
monthly_seasonality = daily_df.groupby('month')['deviation'].mean()

def get_gas_price(date_str):
    target_date = pd.to_datetime(date_str)
    
    # logic path A: The date is within our historical data range
    if target_date <= daily_df.index.max() and target_date >= daily_df.index.min():
        return daily_df.loc[target_date, 'prices']
    
    # logic path B: The date is in the future (Extrapolation)
    else:
        # calc days since dataset start (2020-10-31)
        days_since = (target_date - daily_df.index.min()).days
        
        # calc trend component
        trend_component = intercept + slope * days_since
        
        # geting seasonal component for this month
        target_month = target_date.month
        seasonal_component = monthly_seasonality[target_month]
        
        # final price is trend + seasonal adjustment
        return trend_component + seasonal_component


# creating a daily date range for the extrapolation year (Oct 2024 - Sept 2025)
future_dates = pd.date_range(start='2024-10-01', end='2025-09-30', freq='D')

# using a list comprehension
future_prices = [get_gas_price(str(d)) for d in future_dates]
future_df = pd.DataFrame(data={'prices': future_prices}, index=future_dates)

# plotig both dataframes together to see the final product
plt.figure(figsize=(12, 6))
plt.plot(daily_df.index, daily_df['prices'], label='Historical & Interpolated')
plt.plot(future_df.index, future_df['prices'], label='Extrapolated Forecast', linestyle='--')
plt.title('Natural Gas Price Estimation and Extrapolation')
plt.xlabel('Dates')
plt.ylabel('Prices')
plt.legend()
plt.grid(True)
plt.show()
