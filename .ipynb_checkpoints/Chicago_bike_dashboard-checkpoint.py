############################################################################################ CHICAGO BIKE DASHBOARD ############################################################################################

############################################################################################ Import libraries ############################################################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt


########################################################################################### Configure page ###########################################################################################

st.set_page_config(page_title = "Chicago bike strategy dashboard', layout='wide")
st.title("Chicago bike strategy dashboard")
st.markdown("This dashboard will help resolve bike distribution issues and help identify future expansion oppotunities")
st.markdown("Currently, users of Chicago's bike-sharing platform are finding that there are fewer bikes available at popular stations, while other stations have too many docked bikes, making the return of bikes difficult. The aim of this analysis is to determine the reasons behind these issues and look at ways of improving the service.") 


########################################################################################### Import data ###########################################################################################

df = pd.read_csv('reduced_size_dataframe.csv', index_col = 0)
top_20 = pd.read_csv('top_20_bike_stations.csv', index_col = 0)


########################################################################################### DEFINE CHARTS ###########################################################################################

## groupby

df['value'] = 1
df_groupby_bar = df.groupby('from_station_name', as_index=False).agg({'value': 'sum'})
top_20 = df_groupby_bar.nlargest(20, 'value')

## bar chart

fig = go.Figure(go.Bar(x = top_20['from_station_name'], y = top_20['value'], marker={'color': top_20['value'], 'colorscale':'YlOrRd'}))
fig.update_layout(
    title = '20 most popular bike stations in Chicago',
    xaxis_title = 'Starting stations',
    yaxis_title = 'Sum of bike trips',
    width = 900, height = 700
)
fig.update_xaxes(automargin=True)
st.plotly_chart(fig, use_container_width=True)

## line chart

fig_2 = make_subplots(specs = [[{'secondary_y': True}]])

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['bike_rides_daily'], name = 'Daily bike trips', marker={'color': df['bike_rides_daily'], 'color': 'orange'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x = df['date'], y = df['avgTemp'], name = 'Daily temperature', marker={'color': df['avgTemp'], 'color': 'red'}),
secondary_y = True
)
st.plotly_chart(fig_2, use_container_width=True)


## add map

path_to_html = 'Chicago_bike_trips.html'

# read file and keep in variable
with open(path_to_html, 'r') as f:
    html_data = f.read()

## show in webpage
st.header('Aggregated Chicago bike trips')
st.components.v1.html(html_data,height=1000)