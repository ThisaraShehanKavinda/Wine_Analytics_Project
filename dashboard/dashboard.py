import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load your cleaned dataset
data_path = "data/processed/process_wine_data.csv"  # Update this path as needed
wine_df = pd.read_csv(data_path)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Wine Analytics Dashboard"

# App Layout
app.layout = html.Div(
    style={'backgroundColor': '#f5f5f5', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1("Wine Analytics Dashboard", style={'textAlign': 'center', 'color': '#4c4c4c'}),
        html.P(
            "Explore wine data through interactive visualizations.",
            style={'textAlign': 'center', 'color': '#6c6c6c'}
        ),

        # Filters
        html.Div([
            html.Label("Select Country:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in wine_df['Country'].dropna().unique()],
                value=[],
                placeholder="Select one or more countries",
                multi=True
            ),

            html.Label("Price Range (USD):", style={'fontWeight': 'bold', 'marginTop': '10px'}),
            dcc.RangeSlider(
                id='price-slider',
                min=wine_df['Price'].min(),
                max=wine_df['Price'].max(),
                marks={int(price): f"${int(price)}" for price in range(0, int(wine_df['Price'].max()), 20)},
                step=1,
                value=[wine_df['Price'].min(), wine_df['Price'].max()]
            )
        ], style={'width': '30%', 'margin': '0 auto', 'padding': '10px'}),

        # Visualizations
        html.Div([
            dcc.Graph(id='price-histogram', config={'displayModeBar': False}),
            dcc.Graph(id='ratings-scatter', config={'displayModeBar': False}),
            dcc.Graph(id='food-pairings-bar', config={'displayModeBar': False}),
            dcc.Graph(id='alcohol-boxplot', config={'displayModeBar': False}),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'padding': '20px'}),

        # Footer
        html.Div("Dashboard by Your Team", style={'textAlign': 'center', 'color': '#8c8c8c', 'marginTop': '20px'}),
    ]
)

# Callback for filtering and updating visualizations
@app.callback(
    [Output('price-histogram', 'figure'),
     Output('ratings-scatter', 'figure'),
     Output('food-pairings-bar', 'figure'),
     Output('alcohol-boxplot', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('price-slider', 'value')]
)
def update_graphs(selected_countries, price_range):
    # Filter data based on inputs
    filtered_df = wine_df[
        (wine_df['Price'] >= price_range[0]) & 
        (wine_df['Price'] <= price_range[1])
    ]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    
    # Ensure food-pairing columns are numeric
    food_pairing_columns = filtered_df.columns[-21:]  # Adjust based on your data
    filtered_df[food_pairing_columns] = filtered_df[food_pairing_columns].apply(pd.to_numeric, errors='coerce')
    food_counts = filtered_df[food_pairing_columns].sum().sort_values(ascending=False)

    # Create visualizations
    hist_fig = px.histogram(
        filtered_df, x='Price', color='Country',
        title="Price Distribution by Country",
        color_discrete_sequence=px.colors.qualitative.Pastel, nbins=30
    )
    hist_fig.update_layout(autosize=True, template='plotly_white')

    scatter_fig = px.scatter(
        filtered_df, x='Price', y='Rating', color='Country',
        title="Ratings vs Price", size='Number of Ratings',
        template='plotly_white', hover_name='Name'
    )
    scatter_fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))

    bar_fig = px.bar(
        food_counts, x=food_counts.index, y=food_counts.values,
        title="Popular Food Pairings", labels={'x': 'Food', 'y': 'Count'},
        template='plotly_white'
    )
    bar_fig.update_traces(marker_color='darkred')

    box_fig = px.box(
        filtered_df, x='Country', y='Alcohol content', color='Country',
        title="Alcohol Content by Country", template='plotly_white'
    )
    box_fig.update_traces(marker=dict(opacity=0.7))

    return hist_fig, scatter_fig, bar_fig, box_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
