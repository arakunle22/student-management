import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('student_database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PersonalInformation (
        student_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        middle_name TEXT,
        date_of_birth DATE NOT NULL,
        gender TEXT NOT NULL,
        phone_number TEXT,
        email TEXT,
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


# Commit changes and close connection
conn.commit()
conn.close()
