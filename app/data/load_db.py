import json
import sqlite3

# Load the JSON data
with open("./sample_patient_data.json", "r") as f:
    data = json.load(f)

# Connect to (or create) a local SQLite .db file
conn = sqlite3.connect("sample_patients_db.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    date_of_birth TEXT,
    address TEXT,
    zip TEXT,
    order_status TEXT,
    action TEXT
)
''')

# Insert data
for entry in data:
    cursor.execute('''
        INSERT INTO patients (
            id, first_name, last_name, phone_number, date_of_birth,
            address, zip, order_status, action
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        entry["Patient ID"],
        entry["First Name"],
        entry["Last Name"],
        entry["Phone Number"],
        entry["Date of Birth"],
        entry["Address"],
        entry["Zip"],
        entry["Order Status"],
        entry["Action"]
    ))

# Save and close
conn.commit()
conn.close()

print("✅ Created patients.db with JSON data.")
# import sqlite3

# conn = sqlite3.connect("sample_patients_db.db")
# cursor = conn.cursor()
# cursor.execute("PRAGMA table_info(patients)")
# for row in cursor.fetchall():
#     print(row)
# conn.close()