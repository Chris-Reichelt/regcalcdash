# app.py
import dash
from dash import dcc, html, Input, Output, State
import dash_table
import sqlite3
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Reg Calc", style={'textAlign': 'center'}),
    html.Div(id="question-container"),
    html.Div([
        html.Button("Yes", id="yes-button", n_clicks=0),
        html.Button("No", id="no-button", n_clicks=0),
    ], style={'textAlign': 'center'}),
    html.Div(id="answer-summary"),
    html.H2("Summary", style={'textAlign': 'center'}),
    dcc.Store(id='current-stage', data=1),
    dcc.Store(id='current-question', data=0),
    dash_table.DataTable(id='summary-table')
])

# Helper function to retrieve questions based on stage
def get_question(stage, question_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT question_text FROM questions WHERE stage = ? AND id = ?", (stage, question_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# Callback to display the current question
@app.callback(
    Output("question-container", "children"),
    Input("current-stage", "data"),
    Input("current-question", "data"),
)
def display_question(stage, question_id):
    question = get_question(stage, question_id)
    return question or "No more questions for this stage."

# Logic to handle Yes/No responses and advance through questions
@app.callback(
    Output("current-question", "data"),
    Output("answer-summary", "children"),
    Input("yes-button", "n_clicks"),
    Input("no-button", "n_clicks"),
    State("current-stage", "data"),
    State("current-question", "data")
)
def handle_response(yes_clicks, no_clicks, stage, question_id):
    # Move to the next question
    next_question = question_id + 1
    return next_question, f"Response recorded for Question {question_id}"

# Callback to update the summary table
@app.callback(
    Output('summary-table', 'data'),
    Input("current-stage", "data")
)
def update_summary(stage):
    # Example DataFrame for summary display
    if stage > 3:
        summary_data = pd.DataFrame([
            {"Question": "Sample question 1", "Answer": "Yes"},
            {"Question": "Sample question 2", "Answer": "No"},
        ])
        return summary_data.to_dict('records')
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
