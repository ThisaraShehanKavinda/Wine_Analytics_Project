import plotly.graph_objects as go
import pandas as pd

# Load NLP data
nlp_wine_df = pd.read_csv("data/reviews/wine_reviews_with_labels.csv")
category_counts = nlp_wine_df["talks_about"].value_counts()

# NLP Bar Chart
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
