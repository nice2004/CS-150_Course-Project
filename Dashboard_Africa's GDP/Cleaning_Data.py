import pandas as pd


# Load data
df = pd.read_csv('../Dataset/data.csv')
print(df.columns)
print(df['Personal remittances, received (% of GDP)'].max())
# Initialize the Dash app with Bootstrap


# Define African country ISO codes for filtering
african_countries = [
    'DZA', 'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD',
    'COM', 'COG', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 'ETH', 'GAB',
    'GMB', 'GHA', 'GIN', 'GNB', 'CIV', 'KEN', 'LSO', 'LBR', 'LBY', 'MDG',
    'MWI', 'MLI', 'MRT', 'MUS', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA',
    'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TZA', 'TGO',
    'TUN', 'UGA', 'ZMB', 'ZWE'
]

# Get unique years and countries
years = df['Year'].unique()
years.sort()
countries = df['Entity'].unique()
countries.sort()

# Get African countries from the dataset
african_countries_in_data = df[df['Code'].isin(african_countries)]['Entity'].unique()
african_countries_in_data.sort()

