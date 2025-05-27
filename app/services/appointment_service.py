import sqlite3

def create_appointment(department, doctor, time):
    conn = sqlite3.connect('app/database/medical.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT,
            doctor TEXT,
            time TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO appointments (department, doctor, time)
        VALUES (?, ?, ?)
    ''', (department, doctor, time))
    conn.commit()
    conn.close()
