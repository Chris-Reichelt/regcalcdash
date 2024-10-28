# app.py
import dash
from dash import dcc, html, Input, Output, State
import dash_table
import sqlite3
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Layout with headers, questions, and buttons
app.layout = html.Div([
    html.H1("Reg Calc", style={'textAlign': 'center'}),
    html.Div([
        # Introductory text for the app, similar to Streamlit's header
        html.P("This calculator is for U.S. commercial space companies that want to understand the potential complexity, time, and cost involved in navigating the federal regulatory landscape.", style={'textAlign': 'center'}),
        html.P("To use the calculator, answer a series of 'yes/no' questions about one mission. The more defined your mission, the better answers you'll receive.", style={'textAlign': 'center'}),
    ]),
    
    html.H3("Question:", style={'textAlign': 'center'}),
    html.Div(id="question-container", style={'textAlign': 'center', 'margin': '20px'}),

    # Yes/No buttons for the question responses
    html.Div([
        html.Button("Yes", id="yes-button", n_clicks=0, style={'margin': '10px', 'padding': '10px 20px'}),
        html.Button("No", id="no-button", n_clicks=0, style={'margin': '10px', 'padding': '10px 20px'}),
    ], style={'textAlign': 'center'}),

    # Display recorded responses after each question
    html.Div(id="answer-summary", style={'textAlign': 'center', 'marginTop': '20px'}),

    # Summary header and DataTable
    html.H2("Summary", style={'textAlign': 'center', 'marginTop': '20px'}),
    dcc.Store(id='current-stage', data=1),
    dcc.Store(id='current-question', data=0),
    dash_table.DataTable(id='summary-table', style_table={'width': '80%', 'margin': 'auto'})
])

# Helper function to retrieve a question based on stage and question ID
def get_question(stage, question_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_text FROM questions WHERE stage = ? LIMIT 1 OFFSET ?", (stage, question_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Callback to display the current question
@app.callback(
    Output("question-container", "children"),
    [Input("current-stage", "data"), Input("current-question", "data")]
)
def display_question(stage, question_id):
    question = get_question(stage, question_id)
    return question or "No more questions for this stage."

# Store the user's responses
responses = []

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

    # Append the response to the list (for tracking)
    responses.append((f"Question {question_id + 1}", response))

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
