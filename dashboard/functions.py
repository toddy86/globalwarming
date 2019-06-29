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


def run_sql_query(sql):
    ''' Run an SQL query against the app database and return the results in a pandas DataFrame.

    Args: 
        sql (str): SQL query to be run on the database

    Todo:
        Implement exception handling in case of database connection error

    Returns:
        pd.DataFrame: The results of the SQL query as a pandas DataFrame
    '''

    # Connect to the database
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='globalwarming',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    # Query database
    df = pd.read_sql(sql, connection)
    df = df.reset_index()

    # Close the connection to database
    connection.close()  

    # Return the results as a dataframe
    return df

def fahrenheit_to_celsius(df, columns):
    ''' Convert temperture from degrees Fahrenheit to degrees celsius

    Args: 
        df (pd.DataFrame): Dataframe containing temperature column(s) in degrees Fahrenehit
        columns (list): A list of strings of the column name(s) to be converted into degrees Celsius

    Todo:
        Exeption handling of non-string values passed in
        Exception handlign of column names which do not exist
        Exception handling for convertion errors

    Returns:
        pd.Dataframe: Returns the entire dataframe with the specified columns converted into degrees Celsisus
    '''

    # For each specified column, convert the temperature from Fahrenheit to celsius
    for i in columns:
        df[i] = (df.loc[:,i] - 32) * 5 / 9

    return df 


def calc_city_df(city_value, temp_value = "Fahrenheit", temp_vars = ["MaxTemp","MinTemp", "AvgTemp"]):
    ''' Calculate and return the historical temperature data for a specified city.

    Args:
        city_value (str): The name of the city to be queried in the database. 
        temp_value (str): Whether the data is to be displayed as Fahrenheit or Celsius.
        temp_vars (list): List of strings of the temperature metrics to display
    
    Todo: 
        Make city_value default value (if none) to be dynamic based on the data in the dataset
        Make SQL query iterable / programmatic based on the values in the temp_vars list. Current risk of mismatch

    Returns: 
        pd.DataFrame
    '''

    ## Set city value to default city if selection is cleared to avoid error
    if city_value is None:
        city_value = "New York, New York, United States"

    select_data = """
    SELECT 
        StationRecords.StationId as StationId, 
        StationRecords.Year as Year,
        StationRecords.Month as `Month`,
        StationRecords.MaxTemp as MaxTemp,
        StationRecords.MinTemp as MinTemp,
        StationRecords.Temp as AvgTemp,
        CONCAT(IFNULL(StationDetails.City,''), ", ", IFNULL(StationDetails.State,''), ", ", IFNULL(StationDetails.Country,'')) as City
    FROM StationRecords
    JOIN StationDetails ON StationRecords.StationId = StationDetails.StationId
    WHERE CONCAT(IFNULL(StationDetails.City,''), ", ", IFNULL(StationDetails.State,''), ", ", IFNULL(StationDetails.Country,''))  = {}
    """.format(("'" + city_value + "'"))

    # Query database and create dataframe
    df = run_sql_query(select_data)

    # Temperature variables
    temp_vars = temp_vars

    # If temp_value is Celcius, convert the temperature values
    if temp_value == "Celsius":
        df = fahrenheit_to_celsius(df, temp_vars)
    
    # Calculate min, max and average values for each year
    df_max = df.groupby(['City','Year']).max().reset_index()
    df_min = df.groupby(['City','Year']).min().reset_index()
    df_avg = df.groupby(['City','Year']).mean().reset_index()

    # Combine min, max and average values for the city into a single df
    df = df_avg[['Year', 'AvgTemp', 'City']]
    df = df.join(df_max.MaxTemp)
    df = df.join(df_min.MinTemp)
    df = df.reset_index(drop=True)  

    return df


def tile(color, text, id_value, id_year_range):
    """ Create the top row / div for the weather KPI tiles

    Args:
        color (str): colour hex code to display the tile in
        text: (str): Tile title to display
        id_value (str): Unique name of the tile (e.g. tile1)
        id_year_range (str): Text of the year range which the data covers (e.g. "1960 to 2009")

    Returns:
        html.Div
    """

    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns tile_text"
            ),
            html.P(
                id = id_value,
                className="tile_value"
            ),
            html.P(
                id = id_year_range,
                className="twelve columns tile_text sub_text"
            ),
        ],
        className="four columns tile",
        
    )


def calc_year_range(city_value):
    ''' Create the string of year range which the data covers

    Args: 
        city_value (str): Name of the city to query against the database

    Returns: 
        str: the year range (e.g. "1960 to 2009")
    '''

    # Calulcate and return the dataframe for the city
    df = calc_city_df(city_value)

    # Calculate change in temperature between min and max years
    start_year = min(df.Year)
    end_year = max(df.Year)
    year_range = str(str(start_year) + " to " + str(end_year))

    return year_range



def calc_temp_change(city_value, temp_value, temp_var):
    ''' Calculate the temperature change from the start date to the end date of the data in the dataset
 
    Args: 
        city_value (str): Name of the city to query in the databas
        temp_value (str): String of either "Fahreneheit" or "Celsisus" 
        temp_var (str): Name of the temperature variable to calculate the temp change of

    Returns:
        float: Change in temp_var rounded to 2 decimals
    '''

    # Calulcate and return the dataframe for the city
    df = calc_city_df(city_value, temp_value)

    # Calculate change in temperature between min and max years
    start_year = min(df.Year)
    end_year = max(df.Year)
    start_temp = df.loc[df["Year"] == start_year, temp_var].unique()[0]
    end_temp = df.loc[df["Year"] == end_year, temp_var].unique()[0]
    temp_change = end_temp - start_temp

    return round(temp_change,2)

