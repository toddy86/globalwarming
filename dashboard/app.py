# Import required libraries
import pandas as pd
import pymysql.cursors
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pymysql.cursors
import pandas as pd


# Load external style sheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Connect to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='globalwarming',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


# Query the database
try: 
    # SQL query
    sql_query = """
    SELECT 
        StationRecords.StationId as StationId, 
        StationRecords.Year as Year,
        StationRecords.`Month` as `Month`,
        StationRecords.AvgMaxTemp as AvgMaxTemp,
        StationRecords.AvgMinTemp as AvgMinTemp,
        StationRecords.MaxTemp as MaxTemp,
        StationRecords.MinTemp as MinTemp,
        StationRecords.MaxMinTemp as MaxMinTemp,
        CONCAT(StationDetails.City, ",", StationDetails.Country) as City
    FROM StationRecords
    JOIN StationDetails ON StationRecords.StationId = StationDetails.StationId
    WHERE Year in (2016, 2017, 2018)
    """ 
    #CONCAT(StationDetails.City, ",", StationDetails.Country) = 'Zermatt,Switzerland' AND

    # Query database
    df = pd.read_sql(sql_query, connection)

    # Create menu options
    cities = list(df.City.unique())
    months = list(df.Month.unique())

    # Calculate City averages (if more than one weather station in the city)
    df = df.groupby(['City','Year']).mean() # month removed temporarily
    df = df.reset_index()  

except:
    print("Something went wrong with the MySQL connection")

finally:
    connection.close()


# *********** TO BE DELETED LATER *******************
# Generate table with dataframe contents
def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )
# *************************************************


# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='Global Warming and You'),

    # Heading
    html.Div(children='''
        A glance into how global warming is affecting you and where you live.
    '''),

    # City selection dropdown menu 
    html.Div([
        dcc.Dropdown(
            id = 'city-selector',
            options = [{'label': i, 'value': i} for i in cities],
            value = 'Zermatt,Switzerland'
        ),
    ],
     style={'width': '48%', 'display': 'inline-block'}),
    

    # Month selection dropdown menu 
    html.Div([
        dcc.Dropdown(
            id = 'month-selector',
            options = [{'label': i, 'value': i} for i in months],
            value = ''
        ),
    ],
     style={'width': '48%', 'display': 'inline-block'}),

    # Display table
    #generate_table(df),

    dcc.Graph(id='temperature-graphic')

    # Display linechart using callback
    #dcc.Graph(id='temperature-graphic')
    #html.Div(id='temperature-graphic')
])


@app.callback(
    Output('temperature-graphic', 'figure'),
    [Input('city-selector', 'value')])

def update_graph(city_value):
    # Create filtered df based on the month_value selected
    dff = df[df.City == city_value]
    dff = dff.reset_index()

    figure={
        'data': [
            go.Scatter(
                x = dff['Year'],
                y = dff['AvgMaxTemp'],
            ) for i in dff.Month.unique()
        ],
        'layout': {
            'title': dff.City[0]
        }
    }

    return figure

  



# Run the app 
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True) #http:127.0.0.1:8050/


