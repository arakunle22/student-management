# CREATE DATABASE FOR USER AUTHENTICATION
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

cursor = conn.cursor()

# CREATE TABEL FOR USERS
conn.execute('CREATE TABLE users (username TEXT, password TEXT)')
print("Created table successfully!")


# Insert into the newly created table
cursor.execute("INSERT INTO users VALUES ('admin', '123')")
print("Data add to the table successfully!")

conn.commit()

conn.close()

