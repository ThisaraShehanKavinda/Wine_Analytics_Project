from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Wine Analytics Dashboard"

# Set the layout
app.layout = create_layout(app)

# Import callbacks
import callbacks

if __name__ == '__main__':
    app.run_server(debug=True)
