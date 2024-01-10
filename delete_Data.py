import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Replace 'your_table_name' with the name of the table you want to delete
table_to_delete = 'users'

# Drop the table if it exists
drop_table_query = f"DROP TABLE IF EXISTS {table_to_delete};"

# Execute the query to delete the table
cursor.execute(drop_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()
