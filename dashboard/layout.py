from dash import dcc, html
import dash_bootstrap_components as dbc
from figures import nlp_bar_fig
import pandas as pd

# Load data for layout components
wine_df = pd.read_csv("data/processed/process_wine_data.csv")

def create_layout(app):
    return html.Div(
        children=[
            # Header
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Img(src="/assets/wine.png", style={"height": "80px", "marginRight": "20px"}),
                            html.Div(
                                children=[
                                    html.H1(
                                        "Wine Analytics Dashboard",
                                        style={'textAlign': 'center', 'color': '#4a4a4a', 'fontWeight': 'bold', 'margin': '0'}
                                    ),
                                    html.P(
                                        "Dive into the world of wines with insightful and interactive visualizations.",
                                        style={'textAlign': 'center', 'color': '#6c757d', 'margin': '0'}
                                    )
                                ],
                                style={"flex": "1"}
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "justifyContent": "center"},
                    ),
                ],
                style={"background": "linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%)", "padding": "20px", "borderRadius": "10px", "marginBottom": "20px"}
            ),

            # Filters
            html.Div([
                html.Button("Toggle Filters", id="filter-toggle", style={
                    "backgroundColor": "#007bff", "color": "white", "padding": "10px", "border": "none",
                    "borderRadius": "5px", "cursor": "pointer"
                }),
                html.Div(
                    id="filter-panel",
                    children=[
                        html.Div([
                            html.Label("Select Country:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='country-dropdown',
                                options=[{'label': c, 'value': c} for c in sorted(wine_df['Country'].unique())],
                                value=[],
                                placeholder="Select one or more countries",
                                multi=True
                            ),
                        ], style={'padding': '10px'}),

                        html.Div([
                            html.Label("Select Wine Style:", style={'fontWeight': 'bold'}),
                            dcc.Dropdown(
                                id='wine-style-dropdown',
                                options=[{'label': s, 'value': s} for s in sorted(wine_df['Wine style'].unique())],
                                value=[],
                                placeholder="Select wine style(s)",
                                multi=True
                            ),
                        ], style={'padding': '10px'}),

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
                        ], style={'padding': '10px'}),
                    ],
                    style={"display": "block", "border": "1px solid #ccc", "padding": "10px", "borderRadius": "5px", "marginTop": "10px"}
                )
            ]),

            # Tabs
            dcc.Tabs([
                dcc.Tab(label="Price Analysis", children=[
                    dcc.Graph(id='price-histogram', style={'padding': '20px'}),
                    dcc.Graph(id='ratings-scatter', style={'padding': '20px'})
                ]),
                dcc.Tab(label="Food & Alcohol Analysis", children=[
                    dcc.Graph(id='food-pairings-bar', style={'padding': '20px'}),
                    dcc.Graph(id='alcohol-boxplot', style={'padding': '20px'})
                ]),
                dcc.Tab(label="Wine Styles", children=[
                    dcc.Graph(id='wine-style-pie', style={'padding': '20px'})
                ]),
                dcc.Tab(label="NLP Analysis", children=[
                    dcc.Graph(id='nlp-bar-chart', figure=nlp_bar_fig, style={'padding': '20px'})
                ])
            ]),

            # Footer
            html.Footer(
                "Dashboard by USJ OUTLIERS",
                style={'textAlign': 'center', 'marginTop': '20px', 'padding': '10px', 'backgroundColor': '#f1f1f1'}
            )
        ],
        style={"fontFamily": "Arial, sans-serif", "margin": "0 auto", "maxWidth": "1200px"}
    )
