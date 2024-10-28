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
           #Stage 1 questions
           ('Will you be communicating with a launch vehicle, spacecraft, satellite,\n or U.S. based earth station via inter-satellite link, uplink or downlink? ', 'FCC – Satellites and earth stations', 1, 'Yes response text', 'No response text'),
           ('Will you be responsible for authorizing the launch of a suborbital or orbital\n vehicle that’s not an Amateur Rocket? ', 'FAA - AST', 1, 'Yes response text', 'No response text'),
           ('Are you seeking to authorize a novel payload? (It hasn’t been done before \n commercially or is high risk due to things like nuclear propulsion, etc.) ','FAA - AST', 1, 'Yes response text', 'No response text'),
           ('Will your mission involve human space flight? ','FAA - AST', 1, 'Yes response text', 'No response text'),
           ('Are you seeking to authorize a spaceport, a launch site or reentry site\n for other than Amateur Rockets for multiple vehicle operators? ','FAA - AST', 1, 'Yes response text', 'No response text'),
           ('Will you have cameras or sensors onboard your spacecraft or satellite that\n image the Earth intentionally or unintentionally? Star trackers are excluded. ','Commerce - NOAA', 1, 'Yes response text', 'No response text'),
           ('Are you a manufacturer or exporter of Defense Articles?','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Are you a US Person or Company or a Foreign Person located in the US that is \n Brokering Defense Articles?','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Are you a Foreign Person employing or contracting with US Persons for a Defense \n Service? Example: Hiring US rocket propulsion engineers or using a US company\n for testing and integration services supporting a US launch vehicle','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Are you a US Person employing a Foreign Person to work on ITAR controlled\n Technical Data?','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Do you intend to temporarily import Defense Articles into the US?','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Are you a foreign company utilizing US origin Technical Data or integrating \n ITAR controlled components in your final product?','State – DDTC', 1, 'Yes response text', 'No response text'),
           ('Are you a US Person employing a Foreign Person to work on EAR controlled\n Technology? ','Commerce – BIS', 1, 'Yes response text', 'No response text'),
           ('Are you a foreign company utilizing US origin Technology or integrating\n EAR controlled components in your final product?','Commerce – BIS', 1, 'Yes response text', 'No response text'),
]
    cursor.executemany('INSERT INTO questions (question_text, category, stage, response_yes, response_no) VALUES (?, ?, ?, ?, ?)', questions)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
