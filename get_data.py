import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime

# ---------- WEATHER DATA LOADING ---------- #
today = datetime.now().strftime("%Y-%m-%d")


def get_today_weather(latitude=38.2469, longitude=85.7664):
    import openmeteo_requests
    import numpy as np
    import requests_cache
    from retry_requests import retry

    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "apparent_temperature_max",
            "apparent_temperature_min",
            "wind_speed_10m_mean",
            "wind_speed_10m_min",
            "wind_speed_10m_max",
            "relative_humidity_2m_mean",
            "relative_humidity_2m_max",
            "relative_humidity_2m_min",
            "cloud_cover_mean",
            "precipitation_sum",
            "sunrise",
            "sunset",
            "daylight_duration",
            "wind_direction_10m_dominant",
            "precipitation_hours",
        ],
        "hourly": [
            "temperature_2m",
            "wind_speed_10m",
            "wind_direction_10m",
            "relative_humidity_2m",
        ],
        "timezone": "America/New_York",
        "past_days": 31,
        "wind_speed_unit": "mph",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left",
        ).date
    }
    daily_data["temperature_2m_max"] = np.round(daily.Variables(0).ValuesAsNumpy(), 2)
    daily_data["temperature_2m_min"] = np.round(daily.Variables(1).ValuesAsNumpy(), 2)
    daily_data["temperature_2m_mean"] = np.round(daily.Variables(2).ValuesAsNumpy(), 2)
    daily_data["wind_speed_10m_mean"] = np.round(daily.Variables(3).ValuesAsNumpy(), 2)
    daily_data["wind_speed_10m_min"] = np.round(daily.Variables(4).ValuesAsNumpy(), 2)
    daily_data["wind_speed_10m_max"] = np.round(daily.Variables(5).ValuesAsNumpy(), 2)
    daily_data["relative_humidity_2m_mean"] = daily.Variables(6).ValuesAsNumpy()
    daily_data["relative_humidity_2m_max"] = daily.Variables(7).ValuesAsNumpy()
    daily_data["relative_humidity_2m_min"] = daily.Variables(8).ValuesAsNumpy()
    daily_data["wind_direction_10m_dominant"] = daily.Variables(9).ValuesAsNumpy()

    daily_data["apparent_temperature_max"] = np.round(
        daily.Variables(3).ValuesAsNumpy(), 2
    )
    daily_data["apparent_temperature_min"] = np.round(
        daily.Variables(4).ValuesAsNumpy(), 2
    )
    daily_data["cloud_cover_mean"] = np.round(daily.Variables(5).ValuesAsNumpy(), 2)
    daily_data["precipitation_sum"] = np.round(daily.Variables(6).ValuesAsNumpy(), 2)

    daily_df = pd.DataFrame(data=daily_data)
    print(daily_df.columns)
    daily_df.to_csv(f"daily_data_{today}.csv", index=False)

    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["temperature_2m"] = hourly.Variables(0).ValuesAsNumpy()
    hourly_data["wind_speed_10m"] = hourly.Variables(1).ValuesAsNumpy()
    hourly_data["wind_direction_10m"] = hourly.Variables(2).ValuesAsNumpy()
    hourly_data["relative_humidity_2m"] = hourly.Variables(3).ValuesAsNumpy()
    hourly_df = pd.DataFrame(data=hourly_data)
    hourly_df.to_csv(f"hourly_data_{today}.csv", index=False)

    # print done
    print("Done")

    return daily_df, hourly_df


# get_today_weather()
