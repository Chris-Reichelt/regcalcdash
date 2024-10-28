# app.py
from dash import Dash, html  # Import html directly from dash

app = Dash(__name__)  # Define the Dash app instance
server=app.server

# Set up the layout using html components
app.layout = html.Div("Hello, Dash!")


if __name__ == '__main__':
    app.run_server(debug=True)
