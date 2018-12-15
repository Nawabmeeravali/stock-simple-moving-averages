'''
Created on Nov 29, 2018

@author: Todd
'''
import numpy as np
import pandas as pd
from pandas_datareader import data
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#choose stock you wish to analyze
symb = input('Input a stock to analyze: ')

#find start and end dates relative to today
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=1825)

#convert dates to strings
end_date = end_date.strftime('%Y-%m-%d')
start_date = start_date.strftime('%Y-%m-%d')

#load data using pandas_datareader
df = data.DataReader(symb, 'iex', start_date, end_date)

#convert dataframe index to datetime
df.index = pd.to_datetime(df.index)

#filter for closing price
close = df['close']

#get all weekdays in date range
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
 
#reindex close using all_weekdays as the new index
close = close.reindex(all_weekdays)

#fill NaN values with previous close price
close = close.fillna(method='ffill')

#format for Seaborn
sns.set(style='darkgrid', context='talk', palette='Dark2')

#calculate 20 and 100 day simple moving averages
short_rolling = close.rolling(window=20).mean()
long_rolling = close.rolling(window=100).mean()

#plot daily close and simple moving averages
fig, ax = plt.subplots(figsize=(16,9))

ax.plot(close.index, close, label=symb, color='lightblue')
ax.plot(short_rolling.index, short_rolling, 
        label='20 day SMA', color='firebrick')
ax.plot(long_rolling.index, long_rolling, 
        label='100 day SMA', color='black')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()
plt.title('Closing Price and SMAs of ' + symb)

sns.set(style='darkgrid', context='talk', palette='Dark2')
plt.show()

