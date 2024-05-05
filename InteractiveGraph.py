#!/usr/bin/env python
# coding: utf-8



# app.py
from dash import Dash, dcc, html
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
data = pd.read_csv('environmental_data.csv')

# Create a DataFrame
df = pd.DataFrame(data)

# Create figure with secondary y-axis
fig = go.Figure()

# Add trace for rainfall as a bar chart first to ensure it's in the background
fig.add_trace(go.Bar(
    x=df['Date'],
    y=df['Rainfall'],
    name='Rainfall',
    yaxis='y2',
    marker_color='rgba(135, 206, 250, 0.7)',
    opacity=0.5
))

# Add traces for groundwater levels over the rainfall bars
fig.add_trace(go.Scatter(
    x=df['Date'], 
    y=df['Groundwater_Borehole1'],
    name='Groundwater Borehole 1',
    line=dict(color='rgba(219, 219, 141, 1)', width=1.5)
))
fig.add_trace(go.Scatter(
    x=df['Date'], 
    y=df['Groundwater_Borehole2'],
    name='Groundwater Borehole 2',
    line=dict(color='rgba(77, 77, 77, 1)', width=1.5)
))

# Set up layout
fig.update_layout(
    title='Groundwater Levels and Rainfall',
    title_x=0.5,
    xaxis=dict(
        domain=[0.05, 1],
        showline=True,
        linecolor='black',
        linewidth=1,
        rangeslider=dict(visible=True, thickness=0.1),
        type="date",
        rangeselector=dict(
            buttons=[
                {'count': 1, 'label': '1m', 'step': 'month', 'stepmode': 'backward'},
                {'count': 6, 'label': '6m', 'step': 'month', 'stepmode': 'backward'},
                {'count': 1, 'label': 'YTD', 'step': 'year', 'stepmode': 'todate'},
                {'count': 1, 'label': '1y', 'step': 'year', 'stepmode': 'backward'},
                {'step': 'all'}
            ],
            x=0,
            xanchor='left',
            y=1.15,
            yanchor='top'
        )
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
    legend=dict(x=0.5, xanchor="center", y=-0.50),
    plot_bgcolor='white'
)

# Create the Dash application
app = Dash(__name__)
server = app.server  # Expose the server variable for gunicorn

app.layout = html.Div([
    html.H1("Groundwater Levels and Rainfall Dashboard"),
    dcc.Graph(id='groundwater-graph', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)  # Production settings

