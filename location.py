from geopy.geocoders import Nominatim
from datetime import datetime
from get_data import get_today_weather

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import sys

# Ask for city input
city = input("Enter the name of the city: ")
geolocator = Nominatim(user_agent='myapplication')
location = geolocator.geocode(city)

if location is None:
    print("Location not found.")
    sys.exit()

latitude = location.latitude
longitude = location.longitude

# Get data
daily_df, hourly_df = get_today_weather(latitude, longitude)

# Use local timezone datetime strings for the x-axis
hourly_df["time"] = hourly_df["date"].dt.strftime("%H:%M")

# Start Dash app
app = dash.Dash(__name__)
app.title = f"Weather in {city}"

app.layout = html.Div([
    html.H1(f"Weather in {city}", style={"textAlign": "center"}),

    dcc.Graph(
        id='temperature-graph',
        figure={
            'data': [
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["temperature_2m"],
                    mode='lines+markers',
                    name='Temperature (°F)'
                )
            ],
            'layout': go.Layout(
                title='Hourly Temperature',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Temperature (°F)'}
            )
        }
    ),

    dcc.Graph(
        id='wind-speed-graph',
        figure={
            'data': [
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["wind_speed_10m"],
                    mode='lines+markers',
                    name='Wind Speed (mph)'
                )
            ],
            'layout': go.Layout(
                title='Hourly Wind Speed',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Wind Speed (mph)'}
            )
        }
    ),

    dcc.Graph(
        id='humidity-graph',
        figure={
            'data': [
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["relative_humidity_2m"],
                    mode='lines+markers',
                    name='Humidity (%)'
                )
            ],
            'layout': go.Layout(
                title='Hourly Humidity',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Humidity (%)'}
            )
        }
    ),

    dcc.Graph(
        id='wind-direction-graph',
        figure={
            'data': [
                go.Scatter(
                    x=hourly_df["time"],
                    y=hourly_df["wind_direction_10m"],
                    mode='lines+markers',
                    name='Wind Direction (°)'
                )
            ],
            'layout': go.Layout(
                title='Hourly Wind Direction',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Wind Direction (degrees)'}
            )
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)
