import csv
import os
import random
import decimal
from datetime import timedelta

import pandas as pd

from processor_seed_gen import fake, save_to_csv
from processor_transaction_gen import random_integer, random_date, random_decimal, start_date, end_date
from processor_transaction_gen import num_transactions, transactions

# Function to generate random time durations
def random_time_duration():
  minutes = random.randint(1, 60)
  seconds = random.randint(1, 60)
  return f'{minutes:02}:{seconds:02}'

fees = pd.DataFrame({
    'FeeID': range(1, num_transactions + 1),
    'TransactionID': range(1, num_transactions + 1),
    'DiscountFees': [random_decimal() for _ in range(num_transactions)],
    'TransactionFees': [random_decimal() for _ in range(num_transactions)],
    'MonthlyFees': [random_decimal() for _ in range(num_transactions)],
    'ChargebackFees': [random_decimal() for _ in range(num_transactions)],
    'TotalFees': [random_decimal() for _ in range(num_transactions)],
    'AverageFeePerTransaction': [random_decimal() for _ in range(num_transactions)],
    'ReportDate': [random_date(start_date, end_date) for _ in range(num_transactions)],
    'OtherFees': [f'Fee type: {random.choice(["A", "B", "C"])}' for _ in range(num_transactions)],
    'FeeDetails': [fake.text() for _ in range(num_transactions)]
})
save_to_csv(fees, 'Fees')

df2 = transactions.groupby(['MerchantLocationID', 'ChannelID', 'Date']).agg({'Amount': ['sum', 'mean']})
batchDict = {name:df2.loc[name]['Amount'] for name in df2.index}

# Groupby and get sum() and count()
df2 = transactions.groupby(['MerchantLocationID', 'ChannelID', 'Date', 'Status']).size()
for name in df2.index:
  key = (name[0], name[1], name[2])
  batchDict[key][name[3]] = df2.loc[name]
  batchDict[key]["MerchantLocationID"] = name[0]
  batchDict[key]["ChannelID"] = name[1]
  batchDict[key]["Date"] = name[2]
# end for

num_batches = len(batchDict)
batch_transactions = pd.DataFrame({
    'BatchID': range(1, num_batches + 1),
    'Date':[val['Date'] for val in batchDict.values()],
    'MerchantLocationID': [val['MerchantLocationID'] for val in batchDict.values()],
    'ChannelID': [val['ChannelID'] for val in batchDict.values()],
    'TotalTransactionAmount': [val['sum'] for val in batchDict.values()],
    'AverageTransactionValue': [val['mean'] for val in batchDict.values()],
    'SuccessfulTransactions': [val['Successful'] if 'Successful' in val else 0 for val in batchDict.values()],
    'FailedTransactions': [val['Failed'] if 'Failed' in val else 0 for val in batchDict.values()],
    'RefundedTransactions': [val['Refunded'] if 'Refunded' in val else 0 for val in batchDict.values()],
    'ChargebackCount': [val['Pending'] if 'Pending' in val else 0 for val in batchDict.values()],
    'AverageAuthorizationTime': [random_integer(3,5) * 1440 for val in batchDict.values()],
    'AverageSettlementTime': [random_integer(3,5) * 1440 for val in batchDict.values()],
})
save_to_csv(batch_transactions, 'BatchTransactions')

# Generate data for the Settlements table
settlements_data = pd.DataFrame({
  "SettlementID" : range(1, num_batches + 1),
  "BatchID" : range(1, num_batches + 1),
  "SettlementDate" : [val['Date'] + timedelta(random_integer(1, 5)) for val in batchDict.values()],
  "TotalSettlementAmount" : [val['sum'] for val in batchDict.values()],
  "BatchTotals": [val['sum'] for val in batchDict.values()],
  "InterchangeFees" : [random_decimal() for _ in range(1, num_batches + 1)],
  "DiscountRates": [random_decimal() for _ in range(1, num_batches + 1)],
  "ReserveAmount" : [random_decimal() for _ in range(1, num_batches + 1)],
  "ClearedFunds" : [random_decimal() for _ in range(1, num_batches + 1)],
  "ReturnedFunds" : [random_decimal() for _ in range(1, num_batches + 1)],
  "NetSettlementAmount": [val['sum'] for val in batchDict.values()],
  "SettlementCurrency": [random.choice(['USD', 'EUR', 'GBP']) for _  in range(1, num_batches + 1)],
  "SettlementStatus" : [fake.random.getstate() for _  in range(1, num_batches + 1)],
  "SettlementDelay" : [random_integer(0,3) for _  in range(1, num_batches + 1)],
  "ReserveReleaseDate" : [val['Date'] + timedelta(random_integer(1, 5)) for val in batchDict.values()],
})
save_to_csv(settlements_data, 'Settlements')

# Generate data for the Reconciliation table

reconciliation_data = pd.DataFrame({
  "ReconciliationID" : range(1, num_batches + 1),
  "BatchID" : range(1, num_batches + 1),
  "ReconciliationDate" : [val['Date'] + timedelta(random_integer(1, 5)) for val in batchDict.values()],
  "DiscrepancyCount" : [random_integer(0, 5) for _ in range(1, num_batches + 1)],
  "DiscrepancyAmount": [val['sum']/10 for val in batchDict.values()],
  "UnsettledTransactions" : [random_integer(0, 5) for _ in range(1, num_batches + 1)],
  "UnsettledAmount": [val['sum'] / 10 for val in batchDict.values()],
  "ReconciliationStatus": [fake.random.getstate() for _ in range(1, num_batches + 1)],
})
save_to_csv(reconciliation_data, 'Reconciliations')

