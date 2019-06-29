"""
TODO:
- Add today's temp (API)
- Add 5 day forecast (API)
- Add long range forecast (ML algo)
- Find out why cities like London, Paris etc are not in the dataset

"""

# Import required libraries and custom functions
from functions import * 


# Load external style sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
app.layout = html.Div(children=[
    html.H1(children='Global Warming and You'),

    # Heading
    html.Div(children='''
        A glance into how global warming is affecting you and where you live.
    '''),


    # City selection dropdown menu 
    html.Div(
        [
            dcc.Dropdown(
                id = 'city-selector',
                options = [{'label': i, 'value': i} for i in cities],
                value = cities[0]
            ),
        ],
     style={'width': '48%', 'display': 'inline-block'}),
    


    # Temperature format radio selection menu 
    html.Div(
        [
            dcc.RadioItems(
                id = 'temp-selector',
                options = [{'label': i, 'value': i} for i in temperature_options],
                value = 'Fahrenheit'
            ),
        ],
     style={'width': '48%', 'display': 'inline-block'}),



    #Row of tiles
    html.Div(
        [
            tile(
                "#00cc96",
                "Minimum Temperature",
                "tile1",
                "tile1_year_range",
            ),
            tile(
                "#EF553B",
                "Maximum Temperature",
                "tile2",
                "tile2_year_range",
            ),
            tile(
                "#EF553B",
                "Average Temperature",
                "tile3",
                "tile3_year_range",
            ),            
            
        ],
        className="row"),

    # Main lineplot of temperature over time
    dcc.Graph(id='temperature-graphic')
    
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


