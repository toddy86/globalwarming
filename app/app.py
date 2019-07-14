import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input
from dash.dependencies import Output
from weather_records import WeatherRecords


app = dash.Dash(__name__)

external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

# Initialise WeatherRecords
wr = WeatherRecords()

# Define the app layout
app.layout = html.Div([
    # Left side menu
    html.Div(
        [
            # Title and sub-title
            html.H1(
                ['Global Warming'],
                style={"text-align": "center"}
            ),

            html.P(
                ["A glance into how global warming is affecting you and where you live."],
                style={"text-align": "center"}
            ),

            # City menu
            html.Div(
                [
                    html.P(
                        ["City"],
                        style={"font-weight": "600"}
                    ),
                    dcc.Dropdown(
                        id='city-selector',
                        options=[{'label': i, 'value': i} for i in wr.cities],
                        value='New York, New York, United States',
                        clearable=False
                    )
                ],
                style={"padding-bottom": "20px"}
            ),

            # Temperature selector
            html.Div(
                [
                    html.P(
                        ["Temperature"],
                        style={"font-weight": "600"}
                    ),
                    dcc.RadioItems(
                        id='temp-selector',
                        options=[{'label': i, 'value': i} for i in wr.temperature_options],
                        value='Celsius'
                    )
                ]
            ),
        ],
        className="three columns",
        style={
            'height': '100%',
            "padding": "10",
            "margin-top": "10px",
            "margin-left": "10px",
            "height": "100%"
        },
    ),

    # Main content
    html.Div(
        [
        html.H3(
            ["Historical Averages"],
            style={"text-align": "center"}
        ),
            # Row of tiles
            html.Div(
                html.Div(
                    [
                        wr.tile(
                            "#00cc96",
                            "Change in Min Temperature",
                            "tile1",
                            "tile1_year_range",
                        ),
                        wr.tile(
                            "#EF553B",
                            "Change in Max Temperature",
                            "tile2",
                            "tile2_year_range",
                        ),
                        wr.tile(
                            "#EF553B",
                            "Change in Avg Temperature",
                            "tile3",
                            "tile3_year_range",
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "display": "-moz-inline-box",
                        "width": "100%",
                        "text-align": "center"
                    }
                ),
                className="row",
            ),

            # Main lineplot of temperature over time
            html.Div(
                [dcc.Graph(id='temperature-graphic')]
            ),

            # 5-day forecast
            html.Div(
                [
                    # Heading
                    html.Div(
                        [
                            html.H3("5-Day Forecast"),
                            html.P("Please be patient while the data are fetched...")
                        ],
                        style={"text-align": "center"}
                    ),
                    # 5-day forecast graphic
                    html.Div(
                        [
                            dcc.Graph(id='forecast-graphic')
                        ]
                    )
                ]
            )
        ],
        # Styling of the main div element
        className="nine columns",
        id="rightpanel",
        style={
            "height": "100%",
            "margin-top": "10px"
        }
    )
])


# Callbacks to update tile values
@app.callback(
    Output("tile1", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile1_callback(city_value, temp_value):
    return wr.calc_temp_change(city_value, temp_value, "MinTemp")


@app.callback(
    Output("tile2", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile2_callback(city_value, temp_value):
    return wr.calc_temp_change(city_value, temp_value, "MaxTemp")


@app.callback(
    Output("tile3", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile3_callback(city_value, temp_value):
    return wr.calc_temp_change(city_value, temp_value, "AvgTemp")


# Callbacks to update tile year ranges
@app.callback(
    Output("tile1_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile1_year_range_callback(city_value):
    return wr.calc_year_range(city_value)


@app.callback(
    Output("tile2_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile2_year_range_callback(city_value):
    return wr.calc_year_range(city_value)


@app.callback(
    Output("tile3_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile3_year_range_callback(city_value):
    return wr.calc_year_range(city_value)


# Callback to generate historical temperature linechart
@app.callback(
    Output('temperature-graphic', 'figure'),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')]
)
def update_graph(city_value, temp_value):
    # Temperature variables to display on the graph
    temp_vars = ["MaxTemp", "MinTemp", "AvgTemp"]

    # Calculate df for the city
    df = wr.calc_city_df(city_value, temp_value)

    # Create lineplot for each temp variable
    traces = []
    for i in temp_vars:
        traces.append(go.Scatter(
                x=df['Year'],
                y=df[i],
                name=i
        ))

    # Generate and return the plot
    return {
        'data': traces,
        'layout': {
            'title': df.City[0]
        }
    }


# Callback to update 5 day forecast
@app.callback(
    Output('forecast-graphic', 'figure'),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')]
)
def update_forecast(city_value, temp_value):
    # Get 7 day history + 5 day forecast
    df = wr.get_recent_weather(city_value, temp_value)

    # Temperature variables to display on the graph - if there isn't any historical data, just plot the MaxTemp and forecast
    if df.columns[-1] == "MaxTemp":
        temp_vars = ["Last 7 Days", "Forecast"]
    else:
        temp_vars = ["Last 7 Days", "Forecast", df.columns[-1]]

    # Create lineplot for each temp variable
    traces = []
    for i in temp_vars:
        traces.append(go.Scatter(
                x=df['Date'],
                y=df[i],
                name=i
        ))
    # Generate and return the plot
    return {
        'data': traces,
        'layout': {
            'title': city_value
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
