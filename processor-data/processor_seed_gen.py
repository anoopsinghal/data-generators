# Install required packages
#!pip install pandas
#!pip install Faker

import pandas as pd
from faker import Faker
import random
import os

# Initialize Faker and create directory for CSV files
fake = Faker()
dirname = 'csv_files'
if not os.path.exists(dirname):
    os.makedirs(dirname)

# Function to save DataFrame to CSV
def save_to_csv(df, filename):
    df.to_csv(f'{dirname}/{filename}.csv', index=False)
    print(f"saved file for {filename} under {dirname}")
# end save_to_csv

def random_boolean():
  return random.choice([True, False])
# end random_boolean

# Generate Constant Tables
payment_methods = pd.DataFrame({
    'PaymentMethodID': range(1, 6),
    'PaymentMethod': ['Credit Card', 'Debit Card', 'Bank Transfer', 'Cash', 'Check']
})
save_to_csv(payment_methods, 'PaymentMethods')

card_brands = pd.DataFrame({
    'CardBrandID': range(1, 6),
    'CardBrand': ['Visa', 'MasterCard', 'Amex', 'Discover', 'JCB']
})
save_to_csv(card_brands, 'CardBrands')

countries = pd.DataFrame({
    'CountryID': range(1, 6),
    'Country': ['USA', 'Canada', 'UK', 'Australia', 'Germany']
})
save_to_csv(countries, 'Countries')

device_types = pd.DataFrame({
    'DeviceTypeID': range(1, 6),
    'DeviceType': ['Desktop', 'Mobile', 'Tablet', 'POS', 'Others']
})
save_to_csv(device_types, 'DeviceTypes')

customer_segments = pd.DataFrame({
    'CustomerSegmentID': range(1, 6),
    'CustomerSegment': ['Retail', 'Wholesale', 'Government', 'Non-profit', 'Education']
})
save_to_csv(customer_segments, 'CustomerSegments')

channels = pd.DataFrame({
    'ChannelID': range(1, 6),
    'ChannelType': ['CNP', 'Chip', 'Chip & Pin', 'Stripe', 'MOTO']
})
save_to_csv(channels, 'Channels')

# Generate core transactional tables
# For this example, assume we have 10 records for each table. In a real-world scenario, these numbers would be much larger.

# Merchants table
num_merchants = 10
merchants = pd.DataFrame({
    'MerchantID': range(1, num_merchants + 1),
    'MerchantName': [fake.company() for _ in range(num_merchants)],
    'Address': [fake.address() for _ in range(num_merchants)],
    'City': [fake.city() for _ in range(num_merchants)],
    'State': [fake.state() for _ in range(num_merchants)],
    'Zip': [fake.zipcode() for _ in range(num_merchants)],
    'IsEcom': [random_boolean() for _ in range(num_merchants)],
    'IsMOTO': [random_boolean() for _ in range(num_merchants)]
})
save_to_csv(merchants, 'Merchants')

# Merchant Locations table
num_locations = 20
merchant_locations = pd.DataFrame({
    'MerchantLocationID': range(1, num_locations + 1),
    'MerchantID': [random.randint(1, num_merchants) for _ in range(num_locations)],
    'Address': [fake.address() for _ in range(num_locations)],
    'City': [fake.city() for _ in range(num_locations)],
    'State': [fake.state() for _ in range(num_locations)],
    'Zip': [fake.zipcode() for _ in range(num_locations)],
    'NumberOfTerminals': [random.randint(1, 5) for _ in range(num_locations)]
})
save_to_csv(merchant_locations, 'MerchantLocations')

terminal_types = ['POS', 'ATM', 'Mobile Reader', 'Online Payment Gateway']
card_terminals = pd.DataFrame({})
add_index = 1
for ind in merchant_locations.index:
    num_terminals = merchant_locations["NumberOfTerminals"][ind]
    locationID = merchant_locations["MerchantLocationID"][ind]
    loc_terminals = pd.DataFrame({
        "TerminalID" : range(add_index, num_terminals + add_index),
        "MerchantLocationID" : [locationID for _ in range(num_terminals)],
        "TerminalType" :  [random.choice(terminal_types) for _ in range(num_terminals)]
    })
    add_index = add_index + num_terminals
    card_terminals = pd.concat([card_terminals, loc_terminals])
# end for
save_to_csv(card_terminals, 'CardTerminals')

# Continue generating other tables as in the code example above.
