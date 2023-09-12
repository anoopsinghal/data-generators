import csv
import os
import random
import decimal
import datetime

import pandas as pd

from processor_seed_gen import save_to_csv, payment_methods, card_brands
from processor_seed_gen import countries, device_types, customer_segments, channels
from processor_seed_gen import card_terminals
from processor_seed_gen import fake
from processor_seed_gen import merchant_locations

# Function to generate random decimal values
def random_decimal():
  return decimal.Decimal(random.randrange(100, 10000)) / 100
#end random_decimal

# Function to generate a random date within a range
def random_date(start_date, end_date):
  return fake.date_between_dates(date_start=start_date, date_end=end_date)
#end random_date

# Function to generate random integers within a range
def random_integer(min_val, max_val):
  return random.randint(min_val, max_val)
# end random_integer

def gen_transaction_related_data(relatedColumn, num_trans, num_related, filename):
  df = pd.DataFrame({
    'TransactionID': range(1, num_transactions + 1),
    relatedColumn: [random.randint(1, num_related) for _ in range(num_trans)]
  })
  save_to_csv(df, filename)
# end gen_transaction_related_data

# Create CSV file for IndividualTransactions table
num_transactions = 1000
start_date=datetime.date(2022, 1, 1)
end_date=datetime.date(2023, 12, 31)
num_terminals = len(card_terminals.index)
num_channels = len(channels.index)
transactions = pd.DataFrame({
    'TransactionID': range(1, num_transactions + 1),
    'Amount': [random_decimal() for _ in range(num_transactions)],
    'Date': [random_date(start_date, end_date) for _ in range(num_transactions)],
    'Status': [random.choice(['Successful', 'Successful','Successful','Successful','Successful','Failed', 'Refunded', 'Pending'])  for _ in range(num_transactions)],
    'TerminalID': [random.randint(1, num_terminals) for _ in range(num_transactions)],
    'MerchantLocationID': [random.randint(1, len(merchant_locations.index) + 1) for _ in range(num_transactions)],
    'ChannelID' : [random.randint(1, num_channels) for _ in range(num_transactions)]
})
save_to_csv(transactions, 'IndividualTransactions')

gen_transaction_related_data('CardBrandID', num_transactions, len(card_brands.index), 'Transaction_CardBrands')
gen_transaction_related_data('PaymentMethodID', num_transactions, len(payment_methods.index), 'Transaction_PaymentMethods')
gen_transaction_related_data('CountryID', num_transactions, len(countries.index), 'Transaction_Countries')
gen_transaction_related_data('DeviceTypeID', num_transactions, len(device_types.index), 'Transaction_DeviceTypes')
gen_transaction_related_data('CustomerSegmentID', num_transactions, len(customer_segments.index), 'Transaction_CustomerSegments')

