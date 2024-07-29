import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('time-tracking.db')

# Create a cursor object
cursor = conn.cursor()


# Create user_data table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    role TEXT,
    contract_number TEXT,
    project TEXT,
    date_start TEXT,
    date_end TEXT,
    password_hash TEXT, 
    salt TEXT, 
    hash_algo TEXT, 
    iterations INTEGER   
)
''')


# # Create role table
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS role (
#     role_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     role_name TEXT NOT NULL UNIQUE
# )
# ''')

# # Insert sample role
# cursor.execute('''
# INSERT OR IGNORE INTO role (role_name) VALUES
# ('supervisor'),
# ('employee'),
# ('admin')
# ''')

# Add role_id column to users table
# cursor.execute('''
# ALTER TABLE users ADD COLUMN role_id INTEGER
# ''')

# Update users table to reference role


# cursor.execute('''
# CREATE TABLE IF NOT EXISTS user_credential (
#     user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_name TEXT NOT NULL UNIQUE,
#     password TEXT NOT NULL,
#     role_id INTEGER,
#     FOREIGN KEY (role_id) REFERENCES role (role_id)
# )
# ''')

# cursor.execute('''
# INSERT INTO user_credential (user_id, user_name, password, role_id)
# SELECT user_id, user_name, password, role_id FROM user
# ''')

# cursor.execute(''' CREATE TABLE IF NOT EXISTS client(
#     client_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     client_name TEXT,
#     client_phone TEXT,
#     client_email TEXT,
#     client_contact_name TEXT,
#     client_address TEXT,
#     client_location TEXT,
#     client_date_start TEXT,
#     client_date_end TEXT)
# ''')

# cursor.execute('DROP TABLE users')
# cursor.execute('ALTER TABLE user_new RENAME TO users')


# cursor.execute('DROP TABLE user_new')
# cursor.execute('ALTER TABLE user_new RENAME TO user_credential')

# Commit the changes and close the connection
conn.commit()
conn.close()
