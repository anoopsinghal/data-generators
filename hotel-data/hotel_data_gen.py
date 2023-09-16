import random
import datetime
import csv
import numpy
import string

import random
import datetime
import csv
import numpy
import string

import psycopg2

from hotel_schema import create_schema

# Replace these with your ElephantSQL database credentials
db_credentials = {
    'host': 'localhost',
    'database': 'hotel',
    'user': 'anoopsinghal',
    'password': ''
}

cursor = None
connection = None
try:
    connection = psycopg2.connect(
        host=db_credentials['host'],
        database=db_credentials['database'],
        user=db_credentials['user'],
        password=db_credentials['password']
    )
    cursor = connection.cursor()
    print("created cursor")
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")
    exit(1)
# end try

create_schema(connection, cursor)

exit(0)
# Initialize lists to store generated data
guests = []
rooms = []
bookings = []
transactions = []
used_guest_ids = set() # Create an empty list to store used guest IDs

# Function to generate unique guest_id values
def generate_guest_id():
    while True:
        guest_id = str(random.randint(100000, 999999))  # Generate a 6-digit random number
        if guest_id not in used_guest_ids:  # Check if the ID is not in the list of used IDs
            used_guest_ids.add(guest_id)  # Add the new ID to the set of used IDs
            return guest_id

# Function to generate random mobile numbers
def random_mobile():
    return f"{random.randint(201, 650)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Function to generate random email addresses
def random_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

# Function to generate random booking date based on check in date
def get_booking_date(checkin_date):
    days_before = numpy.random.randint(0,365)

    if days_before < 7:
        # Increase chance of 0-7 day bookings
        if numpy.random.rand() < 0.2:
            days_before = numpy.random.randint(0,7)
    elif numpy.random.rand() < 0.9:
        # 80-90% of bookings 0-90 days before
        days_before = numpy.random.randint(0,90)
    elif numpy.random.rand() < 0.95:
        # 10% of bookings 90-180 days before
        days_before = numpy.random.randint(90,180)
    elif numpy.random.rand() < 0.99:
        # 5% of bookings 180-270 days before
        days_before = numpy.random.randint(180,270)
    else:
        # 5% of bookings 270-365 days before
        days_before = numpy.random.randint(270,365)

    # Calculate booking date
    booking_date = checkin_date - datetime.timedelta(days=days_before)

    return booking_date

#Funtion to generate random addresses
def generate_random_address():

    # Street number between 1 and 9999
    street_num = random.randint(1, 9999)

    # Random street name of 1-3 words
    street_name = ' '.join(random.choices(string.ascii_lowercase, k=random.randint(1,3)))

    # Random choice of US state abbreviations
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state = random.choice(states)

    # Random 5 digit ZIP code
    zip_code = random.randint(10000, 99999)

    return f'{street_num} {street_name}, {state} {zip_code}'

import names

def generate_guest():

  first_name = names.get_first_name()
  last_name = names.get_last_name()

  guest = {
        'guest_id' : generate_guest_id(), # guest id
        'first_name': first_name,
        'last_name': last_name,
        'address': generate_random_address(),
        'nationality': 'US', #if random.random() < 0.8 else 'Non-US',
        'passport_number': random.randint(10000000, 99999999) if random.random() >= 0.8 else None,
        'dl_number': random.randint(10000000, 99999999) if random.random() < 0.8 else None,
        'cc_type': random.choice(['Visa', 'Mastercard', 'Amex', 'Apple Pay']), #Apple Pay new cc_type
        'cc_last4': random.randint(1000, 9999),
        'mobile': random_mobile(),
        'email': random_email(first_name, last_name),
        'num_guests': random.randint(0, 2),
        'car_license_plate': f"{random.randint(100, 999)}-XYZ" if random.random() < 0.9 else None,
        'loyalty_program': random.choice(['Silver', 'Gold', 'Platinum', 'None']), #None as new choice
        'special_requests': 'Extra Towels' if random.random() < 0.2 else None,
        'booking_source': random.choice(['Direct', 'Online', 'Social Media']), #social media as new source
        'payment_status': 'Paid', #what if cancelled?
        'pets': random.randint(0, 2),
        'age_group': random.choice(["20-30", "30-40", "40-50", "50-60"]),
        'visit_purpose': 'Leisure' if numpy.random.rand() <0.8 else 'Business', #80% Leisure and 20% business
        'previous_stays': random.randint(0, 10)
    }
  return guest

# Generate Rooms
for i in range(100, 200):
    room = {
        'room_type': random.choice(["Standard", "Deluxe", "Suite"]),
        'room_rate': random.uniform(100.0, 300.0),
        'room_amenities': 'WiFi, Breakfast',
        'room_status': random.choice(["Ready", "Needs Cleaning", "Maintenance"]),
        'room_view': random.choice(["Ocean", "City", "Garden"]),
        'room_floor': random.randint(1, 20)  # Added room floor
    }
    rooms.append(room)

# Current date is August 31, 2023
current_date = datetime.date(2023, 8, 31)

# Generate Bookings and Transactions
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)

for day in range((end_date - start_date).days):
    checkin_date = start_date + datetime.timedelta(days=day) #changed this to checkin date
    month = checkin_date.month

    # Summer peak height 100
    summer_bookings = 80 * numpy.exp(-0.5*(month-6)**2/4**2)
    # Winter peak height 50
    winter_bookings = 50 * numpy.exp(-0.5*(month-12)**2/3**2)
    num_bookings = 10 + summer_bookings + winter_bookings
    num_bookings = int(max(0, num_bookings))


    for i in range(num_bookings):
        room = random.choice(rooms)

        if len(guests) > 0 and random.random() < 0.2:  # Reuse existing guest 20% of the time
          guest = random.choice(guests)
        else:     # Create new guest 80% of the time
          guest = generate_guest()
        guests.append(guest)

        booking_length = random.randint(1, 5)
        booking_date = get_booking_date(checkin_date) #define booking date based on check in date
        checkout_date = booking_date + datetime.timedelta(days=booking_length)


        # 10% cancellation rate
        if random.random() < 0.1:
            booking_status = 'Cancelled'
        else:
            booking_status = 'Checked Out'

        booking = {
            'guest_id': guest['guest_id'], #use guest id from guests
            'room_id': rooms.index(room),
            'booking_date': booking_date,
            'checkin_date': checkin_date,
            'checkout_date': checkout_date,
            'num_guests': guest['num_guests'],
            'booking_status': booking_status,  # Consolidated status
            'total_amount': room['room_rate'] * booking_length,
            'discount_code': None,
            'upgrade_offer': None,
            'feedback_score': None
        }
        bookings.append(booking)

        # Generate a transaction for the booking
        transaction = {
            'booking_id': bookings.index(booking),
            'guest_id': guest['guest_id'],
            'transaction_type': 'Room charge',
            'amount': booking['total_amount'] if booking['booking_status'] != 'Cancelled' else 'N/A',
            'transaction_date': booking_date
        }
        transactions.append(transaction)

# Write data to CSV files and download them
def write_and_download_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    files.download(filename)

write_and_download_csv('guests.csv', guests)
write_and_download_csv('rooms.csv', rooms)
write_and_download_csv('bookings.csv', bookings)
write_and_download_csv('transactions.csv', transactions)

# Function to insert a guest into the database and handle duplicate guest_id values
def insert_guest(guest):
    while True:
        try:
            insert_guest_query = """
            INSERT INTO guests (guest_id, first_name, last_name, address, nationality, passport_number, dl_number, cc_type, cc_last4, mobile, email, num_guests, car_license_plate, loyalty_program, special_requests, booking_source, payment_status, pets, age_group, visit_purpose, previous_stays)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_guest_query, (
                guest['guest_id'],
                guest['first_name'],
                guest['last_name'],
                guest['address'],
                guest['nationality'],
                guest['passport_number'],
                guest['dl_number'],
                guest['cc_type'],
                guest['cc_last4'],
                guest['mobile'],
                guest['email'],
                guest['num_guests'],
                guest['car_license_plate'],
                guest['loyalty_program'],
                guest['special_requests'],
                guest['booking_source'],
                guest['payment_status'],
                guest['pets'],
                guest['age_group'],
                guest['visit_purpose'],
                guest['previous_stays']
            ))
            break  # If the insert succeeds, exit the loop
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                # Generate a new guest_id and try again
                guest['guest_id'] = generate_guest_id()
            else:
                raise e

# Insert data into the guests table
for guest in guests:
    insert_guest(guest)


# Function to insert a guest into the database and handle duplicate guest_id values
def insert_guest(guest):
    while True:
        try:
            insert_guest_query = """
            INSERT INTO guests (guest_id, first_name, last_name, address, nationality, passport_number, dl_number, cc_type, cc_last4, mobile, email, num_guests, car_license_plate, loyalty_program, special_requests, booking_source, payment_status, pets, age_group, visit_purpose, previous_stays)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_guest_query, (
                guest['guest_id'],
                guest['first_name'],
                guest['last_name'],
                guest['address'],
                guest['nationality'],
                guest['passport_number'],
                guest['dl_number'],
                guest['cc_type'],
                guest['cc_last4'],
                guest['mobile'],
                guest['email'],
                guest['num_guests'],
                guest['car_license_plate'],
                guest['loyalty_program'],
                guest['special_requests'],
                guest['booking_source'],
                guest['payment_status'],
                guest['pets'],
                guest['age_group'],
                guest['visit_purpose'],
                guest['previous_stays']
            ))
            connection.commit()  # Commit the transaction
            break  # If the insert succeeds, exit the loop
        except psycopg2.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                # Generate a new guest_id and try again
                guest['guest_id'] = generate_guest_id()
            else:
                connection.rollback()  # Rollback the transaction in case of other errors
                raise e

# Insert data into the guests table
for guest in guests:
    insert_guest(guest)

# Insert data into the rooms table
for room in rooms:
    insert_room_query = """
    INSERT INTO rooms (room_type, room_rate, room_amenities, room_status, room_view, room_floor)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_room_query, (
        room['room_type'],
        room['room_rate'],
        room['room_amenities'],
        room['room_status'],
        room['room_view'],
        room['room_floor']
    ))

# Insert data into the bookings table
for booking in bookings:
    insert_booking_query = """
    INSERT INTO bookings (guest_id, room_id, booking_date, checkin_date, checkout_date, num_guests, booking_status, total_amount, discount_code, upgrade_offer, feedback_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(insert_booking_query, (
        booking['guest_id'],
        booking['room_id'] + 1,  # Adding 1 to room_id to match the room_id in PostgreSQL (which starts from 1)
        booking['booking_date'],
        booking['checkin_date'],
        booking['checkout_date'],
        booking['num_guests'],
        booking['booking_status'],
        booking['total_amount'],
        booking['discount_code'],
        booking['upgrade_offer'],
        booking['feedback_score']
    ))

# Insert data into the transactions table
for transaction in transactions:
    insert_transaction_query = """
    INSERT INTO transactions (booking_id, guest_id, transaction_type, amount, transaction_date)
    VALUES (%s, %s, %s, %s, %s);
    """
    cursor.execute(insert_transaction_query, (
        transaction['booking_id'] + 1,  # Adding 1 to booking_id to match the booking_id in PostgreSQL (which starts from 1)
        transaction['guest_id'],
        transaction['transaction_type'],
        transaction['amount'],
        transaction['transaction_date']
    ))

# Commit the changes to the database
connection.commit()

# Close the cursor and the database connection
cursor.close()
connection.close()

print("Data inserted into the database successfully.")










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

