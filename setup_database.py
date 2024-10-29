import sqlite3
import os

def setup_database():
    # Check if the database already exists
    db_exists = os.path.exists('database.db')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create the questions table if it doesn't exist
    if not db_exists:
        print("Creating database and questions table...")
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
        conn.commit()
        print("Table 'questions' created.")
    else:
        print("Database already exists. Skipping table creation.")

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

           #Stage 2 questions
          ('Will the mission be experimental?','6-12 months for experimental space stations. Less for earth stations. \n',2),
          ('Will the mission be a commercial licensing\n of a space station operating in geostationary orbit?','12-18 months \n',2),
          ('If licensing a commercial space station, will your system qualify\n as a small satellite system?','3-12 months \n',2),
          ('If licensing a commercial space station, will your non-geostationary satellite\n system use 20 or more earth stations?','6 months to 2 years depending on spectral allocation \n',2),
          ('If licensing a commercial space station,\n will your non-geostationary satellite system use less than 20 earth stations?','6 months to 1.5 years depending on spectral allocation \n',2),
          ('If licensing an earth station, will your earth station be mobile?','6-18 months \n',2),
          ('If licensing an earth station, will it be for a single site?', '3-12 months \n',2),
          ('If licensing an earth station, will it be for ubiquitous use?', '8-18 months \n',2),
          ('Do you plan to license and operate your own earth stations?','4-12 months \n',2)
]

    # Insert the questions if the database was just created (to avoid duplicates)
    if not db_exists:
        cursor.executemany(
            'INSERT INTO questions (question_text, category, stage, response_yes, response_no) VALUES (?, ?, ?, ?, ?)', 
            questions
        )
        conn.commit()
        print(f"Inserted {len(questions)} questions into the database.")
    else:
        print("Database already has questions. Skipping insertion.")

    # Verify the contents of the database
    cursor.execute("SELECT * FROM questions")
    all_questions = cursor.fetchall()
    if all_questions:
        print("Database contents:")
        for question in all_questions:
            print(question)
    else:
        print("No questions found in the database.")
    
    conn.close()

if __name__ == "__main__":
    setup_database()


        
