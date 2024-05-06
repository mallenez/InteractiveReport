# -*- coding: utf-8 -*-
"""
Created on Mon May 6 11:00:45 2024

@author: mallen2
"""

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

# Load the dataset
df = pd.read_csv('environmental_data.csv')

# Initialize the Dash app with external Bootstrap style
dash_app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app = dash_app.server  # Expose the Flask server for deployment

# Create figure and update layout inside the callback to make it interactive
def create_figure(date_range=None):
    fig = go.Figure()

    # Filter data based on date range
    filtered_df = df if date_range is None else df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    
    # Add trace for rainfall
    fig.add_trace(go.Bar(
        x=filtered_df['Date'],
        y=filtered_df['Rainfall'],
        name='Rainfall',
        yaxis='y2',
        marker_color='rgba(135, 206, 250, 0.7)',
        opacity=0.5
    ))
    
    # Add traces for groundwater levels
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'], 
        y=filtered_df['Groundwater_Borehole1'],
        name='Groundwater Borehole 1',
        line=dict(color='rgba(219, 219, 141, 1)', width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['Date'], 
        y=filtered_df['Groundwater_Borehole2'],
        name='Groundwater Borehole 2',
        line=dict(color='rgba(77, 77, 77, 1)', width=1.5)
    ))

    # Update layout
    fig.update_layout(
        title='Groundwater Levels and Rainfall',
        title_x=0.5,
        xaxis=dict(
            domain=[0.05, 1],
            showline=True,
            linecolor='black',
            linewidth=1,
            rangeslider=dict(visible=True, thickness=0.1),
            type="date"
        ),
        yaxis=dict(
            title='Groundwater Level (m)',
            showline=True,
            linewidth=2,
            linecolor='black',
            gridcolor='rgba(211, 211, 211, 0.8)'
        ),
        yaxis2=dict(
            title='Rainfall (mm)',
            overlaying='y',
            side='right',
            showline=True,
            linewidth=2,
            linecolor='black'
        ),
        legend_orientation="h",
        legend=dict(x=0.5, xanchor="center", y=-0.10),
        plot_bgcolor='white'
    )
    
    return fig

# Define the layout of the Dash app
dash_app.layout = html.Div([
    html.H1("Groundwater Levels and Rainfall Dashboard"),
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df['Date'].min(),
        max_date_allowed=df['Date'].max(),
        start_date=df['Date'].min(),
        end_date=df['Date'].max()
    ),
    dcc.Graph(id='interactive-groundwater-graph')
])

# Define the callback to update the graph based on the date picker input
@dash_app.callback(
    Output('interactive-groundwater-graph', 'figure'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')
)
def update_graph(start_date, end_date):
    return create_figure(date_range=[start_date, end_date])

# Run the server if this script is executed directly (useful for local testing)
if __name__ == '__main__':
    dash_app.run_server(debug=True)


