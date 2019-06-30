"""
TODO:
- Add today's temp (API)
- Add 5 day forecast (API)
- Add long range forecast (ML algo)
- Find out why cities like London, Paris etc are not in the dataset

"""

# Import required libraries and custom functions
from functions import * 

# Dash app
app = dash.Dash(__name__)

# Load external style sheets
external_css = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    #"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    #"https://cdn.rawgit.com/amadoukane96/8f29daabc5cacb0b7e77707fc1956373/raw/854b1dc5d8b25cd2c36002e1e4f598f5f4ebeee3/test.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

## ******************************** ##
## CREATE MENUS
## ******************************** ##
# SQL query to return cities
select_cities = """
    SELECT CONCAT(IFNULL(StationDetails.City,''), ", ", IFNULL(StationDetails.State,''), ", ", IFNULL(StationDetails.Country,'')) as City
    FROM StationDetails""" 
df = run_sql_query(select_cities)

# Create menu options
cities = list(df.City.unique())
temperature_options = ["Fahrenheit", "Celsius"]



## ******************************** ##
## APP LAYOUT
## ******************************** ##
# Define the app layout
app.layout = html.Div([

    # Left side menu
    html.Div(
        [
            # Title and sub-title
            html.H1([
                'Global Warming'
                ], 
                style={
                "text-align": "center"
                }
            ),

            html.P([
                "A glance into how global warming is affecting you and where you live."
                ], 
                style={
                    "text-align": "center"
                }
            ),

            # City menu
            html.Div(
                [
                    html.P(
                        ["City"], 
                        style={
                            "font-weight": "600"
                        }
                    ),
                    dcc.Dropdown(
                        id = 'city-selector',
                        options = [{'label': i, 'value': i} for i in cities],
                        value = cities[0]
                    )
                ], 
                style={
                    "padding-bottom": "20px"
                }
            ),

            # Temperature selector
            html.Div(
                [
                    html.P(
                        ["Temperature"],
                        style={
                        "font-weight": "600"
                        }
                    ),
                    dcc.RadioItems(
                        id = 'temp-selector',
                        options = [{'label': i, 'value': i} for i in temperature_options],
                        value = 'Fahrenheit'
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
            "height":"100%"
        },
    ),


    # Main content
    html.Div(
        [
        #Row of tiles
            html.Div(
                html.Div(
                    [
                        tile(
                            "#00cc96",
                            "Change in Min Temperature",
                            "tile1",
                            "tile1_year_range",
                        ),
                        tile(
                            "#EF553B",
                            "Change in Max Temperature",
                            "tile2",
                            "tile2_year_range",
                        ),
                        tile(
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
                dcc.Graph(id='temperature-graphic')
            )
        ], 
        className="nine columns",
        id="rightpanel",
        style={
            #"backgroundColor": "#18252E",
            "height": "100%"
        },
    )
])



## ******************************** ##
## CALLBACKS
## ******************************** ##

# Updates tile values
@app.callback(
    Output("tile1", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile1_callback(city_value, temp_value):
   return calc_temp_change(city_value, temp_value, "MinTemp")

@app.callback(
    Output("tile2", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile2_callback(city_value, temp_value):
   return calc_temp_change(city_value, temp_value, "MaxTemp")

@app.callback(
    Output("tile3", "children"),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')],
)
def tile3_callback(city_value, temp_value):
   return calc_temp_change(city_value, temp_value, "AvgTemp")




# Updates the tile year ranges
@app.callback(
    Output("tile1_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile1_year_range_callback(city_value):
    return calc_year_range(city_value)

@app.callback(
    Output("tile2_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile2_year_range_callback(city_value):
    return calc_year_range(city_value)

@app.callback(
    Output("tile3_year_range", "children"),
    [Input('city-selector', 'value')],
)
def tile3_year_range_callback(city_value):
    return calc_year_range(city_value)




# Updates the main temperature over time linechart
@app.callback(
    Output('temperature-graphic', 'figure'),
    [Input('city-selector', 'value'),
    Input('temp-selector', 'value')])

def update_graph(city_value, temp_value):
    # Temperature variables to display on the graph
    temp_vars = ["MaxTemp","MinTemp", "AvgTemp"]

    # Calculate df for the city
    df = calc_city_df(city_value, temp_value) 


    # Create lineplot for each temp variable
    traces = []
    for i in temp_vars:
        traces.append(go.Scatter(
                x = df['Year'],
                y = df[i],
                name = i
        ))

    # Generate and return the plot 
    return {
        'data': traces,
        'layout': {
            'title': df.City[0]
        }
    }



# Run the app 
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True) #http:127.0.0.1:8050/


