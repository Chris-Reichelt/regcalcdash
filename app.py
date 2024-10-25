# app.py
from dash import Dash, html  # Import html directly from dash

app = Dash(__name__)  # Define the Dash app instance

# Set up the layout using html components
app.layout = html.Div("Hello, Dash!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))  # Use the PORT environment variable or 8050 as default
    app.run_server(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 and the provided port
