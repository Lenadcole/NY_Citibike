import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image


######################################### Initial dashboard settings ######################################

st.set_page_config(page_title = "Chicago bike strategy dashboard", layout="wide")
st.title("Chicago bike strategy dashboard")

### define sidebar
st.sidebar.title("Aspect selector")
page = st.sidebar.selectbox("Select an aspect of the analysis",
    ["Intro", "Weather component and bike usage",
     "Most popular stations",
     "Interactive map with aggregated bike trips", "Recommendations"])


########################################## Import data #####################################################

df = pd.read_csv("reduced_data_dash.csv", index_col = 0)
top_20 = pd.read_csv("top_20_bike_stations.csv", index_col = 0)


########################################################################################### define pages ###########################################################################################


### create intro page

### Intro page

if page == "Intro":
    st.header("This dashboard will help resolve bike distribution issues and help identify future expansion opportunities.")
    st.markdown("Currently, users of Chicago's bike-sharing platform are finding that there are fewer bikes available at popular stations, while other stations have too many docked bikes, making the return of bikes difficult. The aim of this analysis is to determine the reasons behind these issues and look at ways of improving the service.")
    st.markdown("The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather component and bike usage")
    st.markdown("- Interactive map with aggregated bike trips")
    st.markdown("- Recommendations")
    st.markdown("The 'Aspect Selector' dropdown menu on the left will take you to the different aspects of the analysis undertaken by our team.")

    myImage = Image.open("bikes.jpg") 
    st.image(myImage)


### create dual-axis line chart page

elif page == "Weather component and bike usage":

    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig_2.add_trace(
    go.Scatter(x = df["date"], y = df["bike_rides_daily"], name = "Daily bike trips", marker={"color": df["bike_rides_daily"], "color": "orange"}),
    secondary_y = False
    )

    fig_2.add_trace(
    go.Scatter(x = df["date"], y = df["avgTemp"], name = "Daily temperature", marker={"color": df["avgTemp"], "color": "red"}),
    secondary_y = True
    )

    fig_2.update_layout(
    title = "Daily bike rides and termperatures in 2018",
    height = 400
    )

    st.plotly_chart(fig_2, use_container_width=True)
    st.markdown ("#### It is clear to see that there is a positive correlation between temperatures in Chicago and the number of bike rides undergone daily.")
    st.markdown("As temperatures increase and decrease, so does bike usage. The insight we gained here is that a shortage of bikes mainly occurs at warmer times of the year, generally between May and October.")

### create Most popular stations page

    # create the season variable

elif page == "Most popular stations":

    # create side bar filter

    with st.sidebar:
        season_filter = st.multiselect(label= "Select season", options=df["season"].unique(),
    default=df["season"].unique())

    df_1 = df.query("season == @season_filter")

    # define total bike rides
    total_bike_rides = float(df_1["bike_rides_daily"].count())
    st.metric(label = "Total bike rides", value= numerize(total_bike_rides))

    # bar chart

    fig = go.Figure(go.Bar(x = top_20["from_station_name"], y = top_20["value"], marker={"color": top_20["value"], "colorscale":"YlOrRd"}))
    fig.update_layout(
    title = "20 most popular bike stations in Chicago",
    xaxis_title = "Starting stations",
    yaxis_title = "Sum of bike trips",
    width = 900, height = 700
    )
    fig.update_xaxes(automargin=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("#### The four most popular stations are plain to see - Streeter Drive/Grand Avenue, Canal Street/Adams Street, Clinton Street/Madison Street and Clinton Street/Washington Blvd.")
    st.markdown("The other stations in the top 20 are not as popular, as seen by there only being a small jump between the 5th and 20th bars of the plot. When this is cross referenced with the interactive map (which can be accessed in the side bar), the reasoning for the popularity of the top four stations becomes clear.")


### map page

elif page == "Interactive map with aggregated bike trips":

    # create map

    st.write("Interactive map with aggregated bike trips in Chicago")

    path_to_html = "Chicago_bike_trips.html"

    # read file and keep in variable
    with open(path_to_html,'r') as f: 
        html_data = f.read()

    # show in webpage
    st.header("Aggregated bike trips in Chicago")
    st.components.v1.html(html_data,height=1000)
    st.markdown("### We can see if the most popular starting stations also appear in the most popular trips by using the filter on the left hand side of the map.")
    st.markdown("#### The most popular stations are:")
    st.markdown("#### Streeter Drive/Grand Avenue, Canal Street/Adams Street, Clinton Street/Madison Street and Clinton Street/Washington Blvd.")
    st.markdown("However, while Clinton Street/Madison Street is a popular station, it does not account for the most commonly taken bike trips, unlike the other three.")
    st.markdown("If we use the filter to show the most popular routes (those used more than 3,000 times), it was clear that there were two distinct hubs - one on the coast near Navy Pier and another at Millennium train station.")
    st.markdown("The first (Navy Pier) is the location of some of Chicago's biggest tourist attractions - Chicago's Children's Museum, the pier itself and Ohio Street Beach. The journeys generally finished there, with popular start points including the Theatre on the Lake, Shedd Aquarium and Millennium Park.")
    st.markdown("The second, at Millennium train station, is just north of Millennium Park, one of a number of parks that run alongside the lake. Among its many points of interest is the Art Institute of Chicago and the Abraham Lincoln statue. This forms both a popular start and end stop, linking with important transport hubs at Ogilvie Transportation Center and Chicago Union Station, as well as the Chicago Opera House.")

else:

    st.header("Conclusions and recommendations")
    night_bike = Image.open("night_bike.jpg") #source: Mike Cox - Unsplash
    st.image(night_bike)
    st.markdown("#### Our analysis has shown that the following objectives are what should be focused on going forward:")
    st.markdown("- Increase the number of stations near to Navy Pier and in the parks area in and to the south of Millennium Park.")
    st.markdown("- Add stations along Dusable Lake Shore Drive between the parks area and the lake to better serve the lake-side area of the parks.")
    st.markdown("- Stations should also be added along North Jean Baptiste Point Dusable Lake Shore Drive to further serve the Theatre on the Lake and Lincoln Zoo")
    st.markdown("- In warmer months, consider taking bikes from less busy stations further inland to serve the most popular stations nearer the lake.")
    
    



