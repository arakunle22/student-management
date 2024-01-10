# CREATE DATABASE FOR USER AUTHENTICATION
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
print("Connected to database successfully")

cursor = conn.cursor()

# CREATE TABEL FOR STUDENT
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PersonalInformation (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        middle_name TEXT,
        date_of_birth DATE NOT NULL,
        gender TEXT NOT NULL,
        phone_number TEXT,
        address TEXT,
        emergency_contact TEXT,
        FOREIGN KEY (student_id) REFERENCES AcademicInformation(student_id),
        FOREIGN KEY (student_id) REFERENCES AdministrativeInformation(student_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS AcademicInformation (
        student_id INTEGER PRIMARY KEY,
        department TEXT NOT NULL,
        Mathematics  REAL, 
        English REAL, 
        Chemistry REAL,
        Physics REAL,
        Biology REAL, 
        Computer REAL, 
        Commerce REAL,
        Acccounting REAL,
        Literature REAL,
        Government REAL,
        Economic REAL, 
        year_grade INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES PersonalInformation(student_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS AdministrativeInformation (
        student_id INTEGER PRIMARY KEY,
        admission_date DATE NOT NULL,
        advisor_guardian TEXT,
        tuition_fees REAL,
        payments REAL,
        class_attendance INTEGER,
        absence INTEGER,
        tardiness INTEGER,
        FOREIGN KEY (student_id) REFERENCES PersonalInformation(student_id)
    )
''')


# Insert into the newly created table
# cursor.execute("INSERT INTO users VALUES ('admin', '123')")
# print("Data add to the table successfully!")

conn.commit()

conn.close()

