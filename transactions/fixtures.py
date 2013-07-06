import os
import sqlite3


db_filename = 'bank.db'
schema_filename = 'bank_schema.sql'

is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if is_new:
        print("Creating schema...")
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

    conn.execute('DELETE FROM donation')

    print("Inserting data...")
    conn.execute(
        ("INSERT INTO donation (donate_on, donor_name, donor_gender, blood_type)"
         "VALUES ('2013-07-01', 'Ivan Ivanov', 'male', 'A+')")
    )
    conn.execute(
        ("INSERT INTO donation (donate_on, donor_name, donor_gender, blood_type)"
         "VALUES ('2013-06-21', 'Petr Petrov', 'male', 'AB+')")
    )
