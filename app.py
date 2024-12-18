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



# Layout with headers, questions, and buttons
app.layout = html.Div([
    html.H1("Space Regulatory Calculator"),
  
    html.Div([    
    dcc.Markdown('''

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
    cursor.execute("SELECT question_text FROM questions WHERE stage = ? ORDER BY id LIMIT 1 OFFSET ?", (stage, question_id))
    result = cursor.fetchone()
    conn.close()
    
    # Debugging output to check if the question is retrieved correctly
    if result:
        print(f"Retrieved question for stage {stage}, question ID {question_id}: {result[0]}")
    else:
        print(f"No question found for stage {stage}, question ID {question_id}.")
    
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
    if question:
        print(f"Displaying question: {question}")
    else:
        print("No more questions to display.")
    return question or "No more questions for this stage."

# Callback to handle Yes/No button clicks and update responses
@app.callback(
    [Output("current-question", "data"), Output("answer-summary", "children")],
    [Input("yes-button", "n_clicks"), Input("no-button", "n_clicks")],
    [State("current-stage", "data"), State("current-question", "data")]
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
        print(f"Recorded response for question {question_id}: {response}")

    # Move to the next question
    next_question_id = question_id + 1
    return next_question_id, f"Response recorded for Question {question_id + 1}"

# Callback to display the summary once questions are complete
@app.callback(
    Output('summary-table', 'data'),
    [Input("current-stage", "data"), Input("current-question", "data")]
)
def update_summary(stage, question_id):
    max_questions_in_stage = 5  # Adjust this to the actual number of questions per stage
    if question_id >= max_questions_in_stage:
        # Convert responses to a DataFrame and display in table
        df = pd.DataFrame(responses, columns=["Question", "Answer"])
        return df.to_dict('records')
    return []

if __name__ == '__main__':
    app.run_server(debug=True)