# setup_database.py
import sqlite3

def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create the questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT,
            category TEXT,
            stage INTEGER,
            response_yes TEXT,
            response_no TEXT
        )
    ''')

    # Insert questions into the database
    questions = [
        ('Will you be communicating with a launch vehicle, spacecraft, satellite, or U.S. based earth station?', 'FCC – Satellites and earth stations', 1, 'Move to Stage 2', ''),
        # Add more questions here
    ]
    cursor.executemany('INSERT INTO questions (question_text, category, stage, response_yes, response_no) VALUES (?, ?, ?, ?, ?)', questions)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
