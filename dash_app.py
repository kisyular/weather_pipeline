from get_data import get_today_weather
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import datetime
import os
from dash import html, dcc, Dash, Input, Output

# ---------- LOAD OR FETCH DATA ---------- #
today = datetime.now().strftime("%Y-%m-%d")
if os.path.exists(f"daily_data_{today}.csv") and os.path.exists(
    f"hourly_data_{today}.csv"
):
    df = pd.read_csv(f"daily_data_{today}.csv")
    hourly_df = pd.read_csv(f"hourly_data_{today}.csv")
else:
    df, hourly_df = get_today_weather()

# ---------- KPI CARDS ---------- #
apparent_temp = df["apparent_temperature_max"].mean()
cloud_cover = df["cloud_cover_mean"].mean()
precip_sum = df["precipitation_sum"].sum()

max_temp = df["temperature_2m_max"].max()
mean_wind = df["wind_speed_10m_mean"].mean()
dominant_wind_dir = df["wind_direction_10m_dominant"].mode()[0]
min_humidity = df["relative_humidity_2m_min"].min()


def degrees_to_cardinal(degree):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = round(degree / 45) % 8
    return directions[ix]


cardinal_dir = degrees_to_cardinal(dominant_wind_dir)

kpi_cards = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-thermometer-half me-2"),
                            "Max Temp (°F)",
                        ]
                    ),
                    dbc.CardBody([html.H2(f"{max_temp:.2f}", className="card-text")]),
                ],
                color="danger",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-thermometer-half me-2"),
                            "Feels Like Temp (°F)",
                        ]
                    ),
                    dbc.CardBody(
                        [html.H2(f"{apparent_temp:.2f}", className="card-text")]
                    ),
                ],
                color="secondary",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-cloud-fill me-2"),
                            "Cloud Cover (%)",
                        ]
                    ),
                    dbc.CardBody(
                        [html.H2(f"{cloud_cover:.2f}", className="card-text")]
                    ),
                ],
                color="dark",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-cloud-rain-fill me-2"),
                            "Total Precip (in)",
                        ]
                    ),
                    dbc.CardBody([html.H2(f"{precip_sum:.2f}", className="card-text")]),
                ],
                color="info",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-wind me-2"),
                            "Avg Wind Speed (mph)",
                        ]
                    ),
                    dbc.CardBody(
                        [
                            html.H2(
                                f"{mean_wind:.2f} ({cardinal_dir})",
                                className="card-text",
                            )
                        ]
                    ),
                ],
                color="primary",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        [
                            html.I(className="bi bi-droplet-fill me-2"),
                            "Min Humidity (%)",
                        ]
                    ),
                    dbc.CardBody(
                        [html.H2(f"{min_humidity:.2f}", className="card-text")]
                    ),
                ],
                color="info",
                inverse=True,
                className="shadow-sm rounded-3 mb-3",
            )
        ),
    ]
)


# ---------- DAILY CHARTS ---------- #

fig_temp = px.area(
    df,
    x="date",
    y=["temperature_2m_min", "temperature_2m_mean", "temperature_2m_max"],
    labels={"value": "Temperature (°F)", "variable": "Metric", "date": "Date"},
)
fig_temp.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

fig_wind = px.area(
    df,
    x="date",
    y=["wind_speed_10m_min", "wind_speed_10m_mean", "wind_speed_10m_max"],
    labels={"value": "Wind Speed (mph)", "variable": "Metric", "date": "Date"},
)
fig_wind.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

fig_humidity = px.area(
    df,
    x="date",
    y=[
        "relative_humidity_2m_min",
        "relative_humidity_2m_mean",
        "relative_humidity_2m_max",
    ],
    labels={"value": "Humidity (%)", "variable": "Metric", "date": "Date"},
)
fig_humidity.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

# ---------- FORECAST BAR GRAPHS (Next 7 Days) ---------- #

df["date"] = pd.to_datetime(df["date"])
today_date = pd.to_datetime(today)
forecast_df = df[df["date"] > today_date].sort_values("date").head(7)

fig_forecast_temp = px.bar(
    forecast_df,
    x="date",
    y=["temperature_2m_min", "temperature_2m_mean", "temperature_2m_max"],
    barmode="group",
    labels={"value": "Temperature (°F)", "variable": "Metric", "date": "Date"},
)
fig_forecast_temp.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

fig_forecast_wind = px.bar(
    forecast_df,
    x="date",
    y=["wind_speed_10m_min", "wind_speed_10m_mean", "wind_speed_10m_max"],
    barmode="group",
    labels={"value": "Wind Speed (mph)", "variable": "Metric", "date": "Date"},
)
fig_forecast_wind.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

fig_forecast_humidity = px.bar(
    forecast_df,
    x="date",
    y=[
        "relative_humidity_2m_min",
        "relative_humidity_2m_mean",
        "relative_humidity_2m_max",
    ],
    barmode="group",
    labels={"value": "Humidity (%)", "variable": "Metric", "date": "Date"},
)
fig_forecast_humidity.update_layout(
    legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

# ---------- HOURLY SELECTOR + GRAPHS ---------- #

hourly_df["date"] = pd.to_datetime(hourly_df["date"])
unique_days = hourly_df[hourly_df["date"].dt.date >= pd.to_datetime(today).date()][
    "date"
].dt.date.unique()


def create_hourly_graphs(selected_date):
    filtered = hourly_df[hourly_df["date"].dt.date == selected_date]
    fig_temp = px.line(
        filtered,
        x="date",
        y="temperature_2m",
        labels={
            "temperature_2m": "Temperature (°F)",
            "date": "Time",
            "variable": "Metric",
        },
        title=f"Hourly Temperature – {selected_date}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_hum = px.line(
        filtered,
        x="date",
        y="relative_humidity_2m",
        labels={
            "relative_humidity_2m": "Humidity (%)",
            "date": "Time",
            "variable": "Metric",
        },
        title=f"Hourly Humidity – {selected_date}",
    )
    return fig_temp, fig_hum


# ---------- APP ---------- #
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css",
]
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = dbc.Container(
    [
        html.Div(
            [
                html.H1(
                    "MeteoDashboard: Weather Report",
                    className="text-center mb-4 fw-bold text-primary",
                ),
                kpi_cards,
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Daily Temperature Trends"),
                                    dbc.CardBody([dcc.Graph(figure=fig_temp)]),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Daily Wind Speed Trends"),
                                    dbc.CardBody([dcc.Graph(figure=fig_wind)]),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("Daily Humidity Trends"),
                                    dbc.CardBody([dcc.Graph(figure=fig_humidity)]),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                    ]
                ),
                html.H4("Hourly Weather Selector", className="mt-4 mb-2 text-primary"),
                dcc.Tabs(
                    id="hourly-tabs",
                    value=str(unique_days[0]),
                    children=[
                        dcc.Tab(label=str(day), value=str(day))
                        for day in unique_days[:7]
                    ],
                ),
                html.Div(id="hourly-tab-content"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("7-Day Forecast: Temperature"),
                                    dbc.CardBody([dcc.Graph(figure=fig_forecast_temp)]),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("7-Day Forecast: Wind Speed"),
                                    dbc.CardBody([dcc.Graph(figure=fig_forecast_wind)]),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader("7-Day Forecast: Humidity"),
                                    dbc.CardBody(
                                        [dcc.Graph(figure=fig_forecast_humidity)]
                                    ),
                                ],
                                className="mb-4 shadow-sm rounded-3",
                            ),
                            md=4,
                        ),
                    ]
                ),
            ]
        )
    ],
    fluid=True,
)


@app.callback(Output("hourly-tab-content", "children"), Input("hourly-tabs", "value"))
def update_hourly_graphs(selected_date):
    selected = pd.to_datetime(selected_date).date()
    fig1, fig2 = create_hourly_graphs(selected)
    return dbc.Row(
        [dbc.Col(dcc.Graph(figure=fig1), md=6), dbc.Col(dcc.Graph(figure=fig2), md=6)]
    )


# ---------- MAIN ---------- #

if __name__ == "__main__":
    app.run(debug=True)
