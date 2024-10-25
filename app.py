from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize questions and data storage
question1 = [
    ["Will you be communicating with a launch vehicle...", "FCC – Satellites and earth stations"],
    # Add other questions as needed
]

# Store answers in a dictionary
state_data = {
    "answer1": set(),
    "all1": pd.DataFrame(columns=("Question", "Answer")),
}

# Define the app layout
app.layout = dbc.Container([
    html.H1("Regulatory Calculator", className="text-center mt-4"),
    dcc.Tabs(id="tabs", value="tab-1", children=[
        dcc.Tab(label="Section 1: Agencies", value="tab-1"),
        dcc.Tab(label="Section 2: Timeline", value="tab-2"),
        dcc.Tab(label="Section 3: Costs", value="tab-3"),
        dcc.Tab(label="Summary", value="tab-summary"),
    ]),
    html.Div(id="tab-content")
], fluid=True)

# Callbacks for Tabs
@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "tab-1":
        return section_one_content()
    elif tab == "tab-2":
        return section_two_content()
    elif tab == "tab-3":
        return section_three_content()
    elif tab == "tab-summary":
        return summary_content()

# Define the content for each section
def section_one_content():
    return html.Div([
        html.H3("Section 1: Agencies"),
        html.P(question1[0][0]),  # Display question text
        dbc.Button("Yes", id="q1-yes", color="success", n_clicks=0),
        dbc.Button("No", id="q1-no", color="danger", n_clicks=0),
        html.Div(id="output-q1")
    ])

def section_two_content():
    return html.Div([
        html.H3("Section 2: Timeline"),
        # Add content as needed
    ])

def section_three_content():
    return html.Div([
        html.H3("Section 3: Costs"),
        # Add content as needed
    ])

def summary_content():
    return html.Div([
        html.H3("Summary"),
        html.H4("You need to talk to:"),
        DataTable(
            id="summary-table",
            columns=[{"name": i, "id": i} for i in state_data["all1"].columns],
            data=state_data["all1"].to_dict("records"),
            style_table={"overflowX": "auto"},
        ),
    ])

# Callback for Section 1 buttons
@app.callback(
    Output("output-q1", "children"),
    Input("q1-yes", "n_clicks"),
    Input("q1-no", "n_clicks"),
    State("output-q1", "children")
)
def update_section_one(q1_yes, q1_no, existing_output):
    if q1_yes > 0:
        # Store the answer
        state_data["answer1"].add(question1[0][1])
        state_data["all1"] = state_data["all1"].append({"Question": question1[0][0], "Answer": question1[0][1]}, ignore_index=True)
        return f"You answered Yes. Current answers: {', '.join(state_data['answer1'])}"
    elif q1_no > 0:
        return "You answered No."
    return existing_output

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
