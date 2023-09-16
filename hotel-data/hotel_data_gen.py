import random
import datetime
import csv
import pandas as pd
import numpy
import string
import names
from faker import Faker
import psycopg2
import os

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

def save_to_csv(df, filename):
  df.to_csv(f'{dirname}/{filename}.csv', index=False)
  print(f"saved file for {filename} under {dirname}")
# end save_to_csv

def random_boolean():
  return random.choice([True, False])
# end random_boolean

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

# Initialize Faker and create directory for CSV files
fake = Faker()
dirname = 'csv_files'
if not os.path.exists(dirname):
    os.makedirs(dirname)

# generate guests
num_guests = 1000
guests = pd.DataFrame({
    'guest_id': range(1, num_guests + 1),
    'first_name': [names.get_first_name() for _ in range(num_guests)],
    'last_name': [names.get_last_name() for _ in range(num_guests)],
    'address': [fake.address() for _ in range(num_guests)],
    'nationality': ['US' for _ in range(num_guests)],
    'passport_number': [random.randint(10000000, 99999999) if random.random() >= 0.8 else None for _ in range(num_guests)],
    'dl_number': [random.randint(10000000, 99999999) if random.random() < 0.8 else None for _ in range(num_guests)],
    'cc_type': [random.choice(['Visa', 'Mastercard', 'Amex', 'Apple Pay']) for _ in range(num_guests)],  # Apple Pay new cc_type
    'cc_last4': [random.randint(1000, 9999) for _ in range(num_guests)],
    'mobile': [fake.phone_number() for _ in range(num_guests)],
    'email': [fake.ascii_email()  for _ in range(num_guests)],
    'num_guests': [random.randint(0, 2) for _ in range(num_guests)],
    'car_license_plate': [f"{random.randint(100, 999)}-XYZ" if random.random() < 0.9 else None for _ in range(num_guests)],
    'loyalty_program': [random.choice(['Silver', 'Gold', 'Platinum', 'None'])  for _ in range(num_guests)],
    'special_requests': ['Extra Towels' if random.random() < 0.2 else None  for _ in range(num_guests)],
    'booking_source': [random.choice(['Direct', 'Online', 'Social Media']) for _ in range(num_guests)],
    'payment_status': ['Paid'  for _ in range(num_guests)],
    'pets': [random.randint(0, 2) for _ in range(num_guests)],
    'age_group': [random.choice(["20-30", "30-40", "40-50", "50-60"]) for _ in range(num_guests)],
    'visit_purpose': ['Leisure' if numpy.random.rand() < 0.8 else 'Business'  for _ in range(num_guests)],
    'previous_stays': [random.randint(0, 10)  for _ in range(num_guests)]
})
save_to_csv(guests, 'guests')

# Generate Rooms
num_rooms = 200
rooms = pd.DataFrame({
  'room_id':range(1, num_rooms + 1),
  'room_type': [random.choice(["Standard", "Deluxe", "Suite"]) for _ in range(num_rooms)],
  'room_rate': [random.uniform(100.0, 300.0)  for _ in range(num_rooms)],
  'room_amenities': ['WiFi, Breakfast' for _ in range(num_rooms)],
  'room_status': [random.choice(["Ready", "Needs Cleaning", "Maintenance", "Occupied"]) for _ in range(num_rooms)],
  'room_view': [random.choice(["Ocean", "City", "Garden"])  for _ in range(num_rooms)],
  'room_floor': [random.randint(1, 20)  for _ in range(num_rooms)] # Added room floor
})
save_to_csv(rooms, 'rooms')

# trial code to see what num bookings with season look like
for month in range(1, 13):
    # Summer peak height 100
    summer_bookings = 80 * numpy.exp(-0.5 * (month - 6) ** 2 / 4 ** 2)
    # Winter peak height 50
    winter_bookings = 50 * numpy.exp(-0.5 * (month - 12) ** 2 / 3 ** 2)
    num_bookings = 10 + summer_bookings + winter_bookings
    num_bookings = int(max(0, num_bookings))

    print(f"{month} - {summer_bookings} {winter_bookings} {num_bookings}")
# end for

# Generate Bookings and Transactions
start_date = datetime.date(2023, 1, 1)

bookings = []
transactions = []

# for every room
for room_id in range(1, num_rooms + 1):
  # for every room
  current_day = 0
  while current_day < 365: # for a whole year
    checkin_date = start_date + datetime.timedelta(days=current_day) #changed this to checkin date
    month = checkin_date.month

    booking_length = random.randint(1, 10)
    booking_date = get_booking_date(checkin_date)  # define booking date based on check in date

    booking_status = "booked" if random.random() < 0.9 else "Cancelled"
    if month < 9: # upto august
      checkout_date = booking_date + datetime.timedelta(days=booking_length)
      booking_status = "Checked Out" if booking_status == "booked" else "Cancelled"
    else:
      checkin_date = None
      checkout_date = None
    # end if

    guest_id = random_integer(1, num_guests)
    booking_id = len(bookings) + 1
    booking = {
      'booking_id' : booking_id,
      'guest_id': guest_id,  # use guest id from guests
      'room_id': room_id,
      'booking_date': booking_date,
      'checkin_date': checkin_date,
      'checkout_date': checkout_date,
      'num_guests': random_integer(1, 5),
      'booking_status': booking_status,  # Consolidated status
      'total_amount': rooms.iloc[room_id - 1]['room_rate'] * booking_length,
      'discount_code': None,
      'upgrade_offer': None,
      'feedback_score': None
    }
    bookings.append(booking)

    # Generate a transaction for the booking
    transaction_id = len(transactions) + 1
    transaction = {
      'booking_id': booking_id,
      'transaction_id': transaction_id,
      'guest_id': guest_id,
      'transaction_type': 'Room charge',
      'amount': booking['total_amount'] if booking['booking_status'] != 'Cancelled' else None,
      'transaction_date': booking_date
    }
    transactions.append(transaction)

    current_day = current_day + booking_length
  # end while
  print(f"processed {room_id}")
# end for room to book and transaction
df = pd.DataFrame(bookings)
save_to_csv(df, "bookings")

df = pd.DataFrame(transactions)
save_to_csv(df, "transactions")

# Commit the changes to the database
connection.commit()

# Close the cursor and the database connection
cursor.close()
connection.close()