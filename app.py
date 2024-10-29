# app.py
import dash
from dash import dcc, html, Input, Output, State
import dash_table
import sqlite3
import pandas as pd
import os

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Function to set up the database if it doesn't exist
def setup_database():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Create the questions table if it doesn't exist
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
        
        cursor.executemany('INSERT INTO questions (question_text, category, stage, response_yes, response_no) VALUES (?, ?, ?, ?, ?)', questions)
        conn.commit()
        conn.close()
        print("Database setup complete with questions added.")
    else:
        print("Database already exists. Skipping setup.")

# Call setup_database to ensure the database is ready
setup_database()

# Layout with headers, questions, and buttons
app.layout = html.Div([
    html.H1("Space Regulatory Calculator"),
  
    html.Div([    
    dcc.Markdown('''
# Space Regulatory Calculator 
#### This calculator is for U.S. commercial space companies that want to understand the potential complexity, time, and cost involved in navigating the federal regulatory landscape. 

#### Regulatory compliance is a requirement for U.S. companies and circumvention or noncompliance may lead to fines, penalties, and even incarceration.

#### To use the calculator, answer a series of “yes/no” questions about one mission. The more defined your mission, then better answers you’ll receive. Some regulatory timelines and fees will stack or run in parallel. Based on your input, the calculator will give you probable answers or answer ranges to three main questions:
#### 1. What agencies do I need to talk to?
#### 2. On what timeline should I talk to those agencies prior to launch?
#### 3. How much will the regulatory process cost?

The calculator obviously can’t be 100% accurate based on “yes/no” questions, but it should at least give you a good overview of what achieving your mission might take on the regulatory side of things. Also, keep in mind that this version of the calculator only looks at five regulators (NOAA, FCC, FAA, DDTC, and BIS). There can be many more agencies involved depending on your operations, the exact scope of your mission and external variables like your corporate ownership structure, funding sources, etc.

Finally, while this calculator estimates regulatory costs for space activities, there are a lot of additional, discretionary costs that you may incur in preparing a submission to an agency (E.g. legal fees, consultants, etc.).
### For more resources, reach out to Aegis at hello@aegis.law. 

Definitions:
- [US Person](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/subpart-C/section-120.62)
- [Foreign Person](https://www.ecfr.gov/current/title-22/section-120.63)
- [Defense Service](https://www.ecfr.gov/current/title-22/section-120.32)
- [Defense Article](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-120/subpart-C/section-120.31)
- [Technology](https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-772)
- [Technical Data](https://www.ecfr.gov/current/title-22/section-120.33)
- [Cooperating Country (See column A:1 of Country Group Chart)](https://www.bis.doc.gov/index.php/documents/regulations-docs/2255-supplement-no-1-to-part-740-country-groups-1)
- [Amateur Rocket](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-101/subpart-C/section-101.22)
- [Novel Activities](# "For the purposes of this calculator means an activity that has no established regulatory path or precedent.")
- [Brokering](https://www.ecfr.gov/current/title-22/part-129#p-129.2(a))
- [Space Station](https://www.ecfr.gov/current/title-47/part-2#p-2.1(Space%20Station))
- [Earth Station](https://www.ecfr.gov/current/title-47/part-2#p-2.1(Earth%20Station))
- [Remote Sensing](https://www.ecfr.gov/current/title-15/part-960#p-960.4(Remote%20sensing))
- [Small Satellite System](https://www.fcc.gov/space/small-satellite-and-small-spacecraft-licensing-process)
- [Consolidated Screening List](https://www.trade.gov/consolidated-screening-list)
- [Prohibited Countries List](https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M/part-126/section-126.1)
'''),
    ], className='intro-text'),  # Apply the intro-text class here

    html.H3("Question:", style={'textAlign': 'center'}),

    # Question container styling
    html.Div(id="question-container", style={'textAlign': 'center', 'margin': '20px'}),

    # Buttons with centered alignment and custom CSS styling
    html.Div([
        html.Button("Yes", id="yes-button", n_clicks=0),
        html.Button("No", id="no-button", n_clicks=0),
    ], style={'textAlign': 'center'}),

    # Display recorded responses after each question
    html.Div(id="answer-summary", style={'textAlign': 'center', 'marginTop': '20px'}),

    # Summary header and DataTable for displaying the summary
    html.H2("Summary", style={'textAlign': 'center', 'marginTop': '20px'}),
    dash_table.DataTable(id='summary-table', style_table={'width': '100%', 'margin': 'auto'})
])

# Helper function to retrieve a question based on stage and question ID
def get_question(stage, question_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_text FROM questions WHERE stage = ? LIMIT 1 OFFSET ?", (stage, question_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Initialize list to store responses
responses = []

# Callback to display the current question
@app.callback(
    Output("question-container", "children"),
    [Input("current-stage", "data"), Input("current-question", "data")]
)
def display_question(stage, question_id):
    question = get_question(stage, question_id)
    return question or "No more questions for this stage."

# Callback to handle Yes/No button clicks and update responses
@app.callback(
    Output("current-question", "data"),
    Output("answer-summary", "children"),
    Input("yes-button", "n_clicks"),
    Input("no-button", "n_clicks"),
    State("current-stage", "data"),
    State("current-question", "data")
)
def handle_response(yes_clicks, no_clicks, stage, question_id):
    # Determine if "Yes" or "No" was clicked
    if yes_clicks > no_clicks:
        response = "Yes"
    else:
        response = "No"

    # Retrieve the current question text to store in the response
    question_text = get_question(stage, question_id)
    if question_text:
        responses.append((question_text, response))

    # Move to the next question
    next_question_id = question_id + 1
    return next_question_id, f"Response recorded for Question {question_id + 1}"

# Callback to display the summary once questions are complete
@app.callback(
    Output('summary-table', 'data'),
    [Input("current-stage", "data"), Input("current-question", "data")]
)
def update_summary(stage, question_id):
    # Only display the summary if all questions in the stage are complete
    max_questions_in_stage = 5  # Example max number of questions in a stage (adjust as necessary)
    if question_id >= max_questions_in_stage:
        # Convert responses to a DataFrame and display in table
        df = pd.DataFrame(responses, columns=["Question", "Answer"])
        return df.to_dict('records')
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
