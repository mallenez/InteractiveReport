# -*- coding: utf-8 -*-
"""
Created on Mon May 6 11:00:45 2024

@author: mallen2
"""

import dash
from dash import dcc, html  # Updated imports to conform with new Dash standards
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

# Load the dataset
df = pd.read_csv('gapminderDataFiveYear.csv')

# Initialize the Dash app with external Bootstrap style
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash_app.server  # Expose the Flask server for deployment

# Define the layout of the Dash app
dash_app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])

# Define the callback to update the graph based on the slider input
@dash_app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df['year'] == selected_year]  # Ensure proper indexing

    # Create a scatter plot
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55, template="plotly_dark")

    # Configure graph animation transition
    fig.update_layout(transition_duration=500)

    return fig

# Run the server if this script is executed directly (useful for local testing)
if __name__ == '__main__':
    dash_app.run_server(debug=True)