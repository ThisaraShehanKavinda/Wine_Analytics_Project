import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
data_path = "data/processed/process_wine_data.csv"  # Update this path as needed
wine_df = pd.read_csv(data_path)

# Preprocessing
wine_df['Food pairings'] = wine_df['Food pairings'].apply(eval)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Advanced Wine Analytics Dashboard"

# App Layout
app.layout = html.Div(
    children=[
        # Header
        html.H1("Advanced Wine Analytics Dashboard", style={'textAlign': 'center'}),
        html.P(
            "Dive into the world of wines with insightful and interactive visualizations.",
            style={'textAlign': 'center'}
        ),

        # Filters
        html.Div([
            html.Div([
                html.Label("Select Country:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': c, 'value': c} for c in sorted(wine_df['Country'].unique())],
                    value=[],
                    placeholder="Select one or more countries",
                    multi=True
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div([
                html.Label("Select Wine Style:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='wine-style-dropdown',
                    options=[{'label': s, 'value': s} for s in sorted(wine_df['Wine style'].unique())],
                    value=[],
                    placeholder="Select wine style(s)",
                    multi=True
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

            html.Div([
                html.Label("Price Range (USD):", style={'fontWeight': 'bold'}),
                dcc.RangeSlider(
                    id='price-slider',
                    min=wine_df['Price'].min(),
                    max=wine_df['Price'].max(),
                    marks={int(p): f"${int(p)}" for p in range(0, int(wine_df['Price'].max()), 10)},
                    step=1,
                    value=[wine_df['Price'].min(), wine_df['Price'].max()]
                ),
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        ]),

        # Visualizations
        html.Div([
            dcc.Graph(id='price-histogram'),
            dcc.Graph(id='ratings-scatter'),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'padding': '20px'}),

        html.Div([
            dcc.Graph(id='food-pairings-bar'),
            dcc.Graph(id='alcohol-boxplot'),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'padding': '20px'}),

        html.Div([
            dcc.Graph(id='wine-style-pie'),
        ], style={'padding': '20px'}),

        html.Footer("Dashboard by Your Name", style={'textAlign': 'center', 'marginTop': '20px'})
    ]
)

# Callback for interactivity
@app.callback(
    [Output('price-histogram', 'figure'),
     Output('ratings-scatter', 'figure'),
     Output('food-pairings-bar', 'figure'),
     Output('alcohol-boxplot', 'figure'),
     Output('wine-style-pie', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('wine-style-dropdown', 'value'),
     Input('price-slider', 'value')]
)
def update_charts(selected_countries, selected_styles, price_range):
    # Filter data
    filtered_df = wine_df[
        (wine_df['Price'] >= price_range[0]) & 
        (wine_df['Price'] <= price_range[1])
    ]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    if selected_styles:
        filtered_df = filtered_df[filtered_df['Wine style'].isin(selected_styles)]

    # Histogram: Price distribution
    hist_fig = px.histogram(
        filtered_df, x='Price', color='Country',
        title="Price Distribution by Country",
        nbins=30, color_discrete_sequence=px.colors.sequential.Agsunset
    )

    # Scatter Plot: Ratings vs Price
    scatter_fig = px.scatter_3d(
        filtered_df, x='Price', y='Rating', z='Number of Ratings',
        color='Country', title="Ratings vs Price",
        hover_name='Name', animation_frame='Country'
    )

    # Bar Chart: Popular Food Pairings
    food_counts = filtered_df['Food pairings'].explode().value_counts()
    bar_fig = px.bar(
        food_counts, x=food_counts.index, y=food_counts.values,
        title="Popular Food Pairings", labels={'x': 'Food', 'y': 'Count'},
        text_auto=True, color=food_counts.values, color_continuous_scale='Viridis'
    )

    # Box Plot: Alcohol Content by Country
    box_fig = px.box(
        filtered_df, x='Country', y='Alcohol content', color='Country',
        title="Alcohol Content by Country", color_discrete_sequence=px.colors.qualitative.Safe
    )

    # Pie Chart: Wine Style Distribution
    pie_fig = px.pie(
        filtered_df, names='Wine style', title="Wine Style Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return hist_fig, scatter_fig, bar_fig, box_fig, pie_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
