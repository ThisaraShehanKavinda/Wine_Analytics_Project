import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go


data_path = "data/processed/process_wine_data.csv"
wine_df = pd.read_csv(data_path)


nlp_data_path = r"C:\Users\NETHU\Desktop\New folder (2)\Wine_Analytics_Project\data\reviews\wine_reviews_with_labels.csv"
nlp_wine_df = pd.read_csv(nlp_data_path)


category_counts = nlp_wine_df["talks_about"].value_counts()


nlp_bar_fig = go.Figure([go.Bar(
    x=category_counts.index,
    y=category_counts.values,
    marker=dict(color='skyblue')
)])
nlp_bar_fig.update_layout(
    title="Distribution of Review Categories from NLP",
    xaxis_title="Category",
    yaxis_title="Count"
)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])  
app.title = "Wine Analytics Dashboard"


app.layout = html.Div(
    children=[
        
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Img(src="/assets/wine.png", style={"height": "80px", "marginRight": "20px"}),
                        html.Div(
                            children=[
                                html.H1(
                                    "Wine Analytics Dashboard",
                                    style={
                                        'textAlign': 'center',
                                        'color': '#4a4a4a',
                                        'fontWeight': 'bold',
                                        'margin': '0'
                                    }
                                ),
                                html.P(
                                    "Dive into the world of wines with insightful and interactive visualizations.",
                                    style={
                                        'textAlign': 'center',
                                        'color': '#6c757d',
                                        'margin': '0'
                                    }
                                )
                            ],
                            style={"flex": "1"}
                        ),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                ),
            ],
            style={
                "background": "linear-gradient(90deg, #ff9a9e 0%, #fad0c4 100%)",
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px"
            }
        ),

        
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

        html.Footer(
            "Dashboard by Your Name",
            style={'textAlign': 'center', 'marginTop': '20px', 'padding': '10px', 'backgroundColor': '#f1f1f1'}
        )
    ],
    style={"fontFamily": "Arial, sans-serif", "margin": "0 auto", "maxWidth": "1200px"}
)


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

    
    hist_fig = px.histogram(
        filtered_df, x='Price', color='Country',
        title="Price Distribution by Country",
        nbins=30, color_discrete_sequence=px.colors.sequential.Agsunset
    )
    hist_fig.update_layout(transition_duration=500)

    
    scatter_fig = px.scatter_3d(
        filtered_df, x='Price', y='Rating', z='Number of Ratings',
        color='Country', title="Ratings vs Price",
        hover_name='Name'
    )

    
    food_counts = filtered_df['Food pairings'].explode().value_counts()
    bar_fig = px.bar(
        food_counts, x=food_counts.index, y=food_counts.values,
        title="Popular Food Pairings", labels={'x': 'Food', 'y': 'Count'},
        text_auto=True, color=food_counts.values, color_continuous_scale='Viridis'
    )

    
    box_fig = px.box(
        filtered_df, x='Country', y='Alcohol content', color='Country',
        title="Alcohol Content by Country", color_discrete_sequence=px.colors.qualitative.Safe
    )

    
    pie_fig = px.pie(
        filtered_df, names='Wine style', title="Wine Style Distribution",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    return hist_fig, scatter_fig, bar_fig, box_fig, pie_fig


if __name__ == '__main__':
    app.run_server(debug=True)
