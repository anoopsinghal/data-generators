create_guests_table = """
CREATE TABLE IF NOT EXISTS guests (
    guest_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    address VARCHAR(255),
    nationality VARCHAR(255),
    passport_number VARCHAR(255),
    dl_number VARCHAR(255),
    cc_type VARCHAR(255),
    cc_last4 VARCHAR(255),
    mobile VARCHAR(255),
    email VARCHAR(255),
    num_guests INTEGER,
    car_license_plate VARCHAR(255),
    loyalty_program VARCHAR(255),
    special_requests VARCHAR(255),
    booking_source VARCHAR(255),
    payment_status VARCHAR(255),
    age_group VARCHAR(255),
    pets VARCHAR(255),
    visit_purpose VARCHAR(255),
    previous_stays VARCHAR(255)
);
"""

create_rooms_table = """
CREATE TABLE IF NOT EXISTS rooms (
    room_id SERIAL PRIMARY KEY,
    room_type VARCHAR(255),
    room_rate DECIMAL,
    room_amenities VARCHAR(255),
    room_status VARCHAR(255),
    room_view VARCHAR(255),
    room_floor INTEGER
);
"""

create_bookings_table = """
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    guest_id INTEGER REFERENCES guests(guest_id),
    room_id INTEGER REFERENCES rooms(room_id),
    booking_date DATE,
    checkin_date DATE,
    checkout_date DATE,
    num_guests INTEGER,
    booking_status VARCHAR(255),
    total_amount DECIMAL,
    discount_code VARCHAR(255),
    upgrade_offer VARCHAR(255),
    feedback_score INTEGER
);
"""

create_transactions_table = """
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(booking_id),
    guest_id INTEGER REFERENCES guests(guest_id),
    transaction_type VARCHAR(255),
    amount DECIMAL,
    transaction_date DATE
);
"""

def create_schema(connection, cursor):
  # Execute SQL statements to create tables
  try:
      cursor.execute(create_guests_table)
      cursor.execute(create_rooms_table)
      cursor.execute(create_bookings_table)
      cursor.execute(create_transactions_table)
      connection.commit()
      print("Tables created successfully.")

      for table in ["transactions", "bookings", "rooms", "guests"]:
        cursor.execute(f"truncate {table} cascade")
      # end for
      print("Tables truncated successfully.")
  except Exception as e:
      print(f"Error creating tables: {str(e)}")

# end create_schema