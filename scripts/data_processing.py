import pandas as pd

"""This script loads, cleans, and merges the housing and interest rate datasets 
to produce a final dataset for analysis."""

# load datasets
interest = pd.read_csv("data/interest_rates.csv")
housing = pd.read_csv("data/house_prices.csv", skiprows=1)
# fix housing column names
housing.columns = housing.iloc[0]
housing = housing[1:]
housing.columns = housing.columns.str.strip()
# select relevant housing variables
housing = housing[['Period', 'New dwellings Price']]
# clean housing price data
housing['New dwellings Price'] = housing['New dwellings Price'].replace('[x]', None)
housing['New dwellings Price'] = housing['New dwellings Price'].str.replace(',', '')
housing['New dwellings Price'] = housing['New dwellings Price'].astype(float)
# rename housing variables
housing = housing.rename(columns={
    'Period': 'Date',
    'New dwellings Price': 'House_Price'
})
# convert interest rates to quarterly frequency
interest['Date Changed'] =pd.to_datetime(interest['Date Changed'])

interest = interest.sort_values('Date Changed')

interest['Quarter'] = interest['Date Changed'].dt.to_period('Q')

interest_quarterly = interest.groupby('Quarter')['Rate'].mean().reset_index()

housing['Date'] = housing['Date'].str.replace(' Q1', '-03-31')
housing['Date'] = housing['Date'].str.replace(' Q2', '-06-30')
housing['Date'] = housing['Date'].str.replace(' Q3', '-09-30')
housing['Date'] = housing['Date'].str.replace(' Q4', '-12-31')
housing['Date'] = pd.to_datetime(housing['Date'])

housing['Quarter'] = housing['Date'].dt.to_period('Q')
# merge datasets
merged = pd.merge(housing, interest_quarterly, on='Quarter')
# save cleaned dataset
merged.to_csv("data/cleaned_data.csv", index=False)

