from dash.dependencies import Input, Output
import plotly.express as px
from app import app
import pandas as pd

# Load data
wine_df = pd.read_csv("data/processed/process_wine_data.csv")

@app.callback(
    Output("filter-panel", "style"),
    Input("filter-toggle", "n_clicks"),
    prevent_initial_call=True
)
def toggle_filters(n_clicks):
    if n_clicks % 2 == 0:
        return {"display": "block", "border": "1px solid #ccc", "padding": "10px", "borderRadius": "5px"}
    else:
        return {"display": "none"}

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
    filtered_df = wine_df[
        (wine_df['Price'] >= price_range[0]) &
        (wine_df['Price'] <= price_range[1])
    ]
    if selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    if selected_styles:
        filtered_df = filtered_df[filtered_df['Wine style'].isin(selected_styles)]

    hist_fig = px.histogram(filtered_df, x='Price', color='Country', title="Price Distribution by Country", nbins=30)
    scatter_fig = px.scatter_3d(filtered_df, x='Price', y='Rating', z='Number of Ratings', color='Country', title="Ratings vs Price")
    food_counts = filtered_df['Food pairings'].explode().value_counts()
    bar_fig = px.bar(food_counts, x=food_counts.index, y=food_counts.values, title="Popular Food Pairings")
    box_fig = px.box(filtered_df, x='Country', y='Alcohol content', color='Country', title="Alcohol Content by Country")
    pie_fig = px.pie(filtered_df, names='Wine style', title="Wine Style Distribution")

    return hist_fig, scatter_fig, bar_fig, box_fig, pie_fig
