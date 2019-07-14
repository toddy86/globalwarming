import pandas as pd
import pymysql.cursors
import dash_html_components as html
import datetime
from apixu.client import ApixuClient
import numpy as np


class WeatherRecords:
    def __init__(self):
        # Create menus and options
        select_cities = """
            SELECT CONCAT(IFNULL(StationDetails.City,''), ", ", IFNULL(StationDetails.State,''), ", ", IFNULL(StationDetails.Country,'')) as City
            FROM StationDetails"""
        df = self.run_sql_query(select_cities)

        # Create menu options
        self.cities = list(df.City.unique())
        self.temperature_options = ["Celsius", "Fahrenheit"]


    def run_sql_query(self, sql):
        """ Run an SQL query against the app database and return the results in a pandas DataFrame.
        Args:
            sql (str): SQL query to be run on the database

        Todo:
            Implement exception handling in case of database connection error

        Returns:
            pd.DataFrame: The results of the SQL query as a pandas DataFrame
        """

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

    def fahrenheit_to_celsius(self, df, columns):
        """ Convert temperture from degrees Fahrenheit to degrees celsius
        Args:
            df (pd.DataFrame): Dataframe containing temperature column(s) in degrees Fahrenehit
            columns (list): A list of strings of the column name(s) to be converted into degrees Celsius
        Todo:
            Exeption handling of non-string values passed in
            Exception handlign of column names which do not exist
            Exception handling for convertion errors
        Returns:
            pd.Dataframe: Returns the entire dataframe with the specified columns converted into degrees Celsius
        """

        # For each specified column, convert the temperature from Fahrenheit to celsius
        for i in columns:
            df[i] = round((df.loc[:, i] - 32) * 5 / 9, 1)

        return df

    def calc_city_df(self, city_value, temp_value="Celsius", temp_vars=["MaxTemp", "MinTemp", "AvgTemp"]):
        """ Calculate and return the historical temperature data for a specified city.
        Args:
            city_value (str): The name of the city to be queried in the database.
            temp_value (str): Whether the data is to be displayed as Fahrenheit or Celsius.
            temp_vars (list): List of strings of the temperature metrics to display
        Todo:
            Make city_value default value (if none) to be dynamic based on the data in the dataset
            Make SQL query iterable / programmatic based on the values in the temp_vars list. Current risk of mismatch
        Returns:
            pd.DataFrame
        """

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
        df = self.run_sql_query(select_data)

        # Temperature variables
        temp_vars = temp_vars

        # If temp_value is Celcius, convert the temperature values
        if temp_value == "Celsius":
            df = self.fahrenheit_to_celsius(df, temp_vars)

        # Calculate min, max and average values for each year
        df_max = df.groupby(['City', 'Year']).max().reset_index()
        df_min = df.groupby(['City', 'Year']).min().reset_index()
        df_avg = df.groupby(['City', 'Year']).mean().reset_index()

        # Combine min, max and average values for the city into a single df
        df = df_avg[['Year', 'AvgTemp', 'City']]
        df = df.join(df_max.MaxTemp)
        df = df.join(df_min.MinTemp)
        df = df.reset_index(drop=True)

        return df

    def tile(self, color, text, id_value, id_year_range):
        """ Create the top row / div for the weather KPI tiles

        Args:
            color (str): colour hex code to display the tile in
            text: (str): Tile title to display
            id_value (str): Unique name of the tile (e.g. tile1)
            id_year_range (str): Text of the year range which the data covers (e.g. "1960 to 2009")

        Returns:
            html.Div: of the tile
        """

        return html.Div(
            [
                html.P(
                    text,
                    className="twelve columns tile_text"
                ),
                html.P(
                    id=id_value,
                    className="tile_value"
                ),
                html.P(
                    id=id_year_range,
                    className="twelve columns tile_text sub_text"
                ),
            ],
            className="four columns tile",
        )

    def calc_year_range(self, city_value):
        """ Create the string of year range which the data covers
        Args:
            city_value (str): Name of the city to query against the database
        Returns:
            str: the year range (e.g. "1960 to 2009")
        """
        # Calulcate and return the dataframe for the city
        df = self.calc_city_df(city_value)

        # Calculate change in temperature between min and max years
        start_year = min(df.Year)
        end_year = max(df.Year)
        year_range = str(str(start_year) + " to " + str(end_year))

        return year_range

    def calc_temp_change(self, city_value, temp_value, temp_var):
        """ Calculate the temperature change from the start date to the end date of the data in the dataset
        Args:
            city_value (str): Name of the city to query in the databas
            temp_value (str): String of either "Fahrenheit" or "Celsius"
            temp_var (str): Name of the temperature variable to calculate the temp change of
        Returns:
            float: Change in temp_var rounded to 2 decimals
        """

        # Calulcate and return the dataframe for the city
        df = self.calc_city_df(city_value, temp_value)

        # Calculate change in temperature between min and max years
        start_year = min(df.Year)
        end_year = max(df.Year)
        start_temp = df.loc[df["Year"] == start_year, temp_var].unique()[0]
        end_temp = df.loc[df["Year"] == end_year, temp_var].unique()[0]
        temp_change = end_temp - start_temp

        return round(temp_change, 2)

    def get_daily_history(self, city_value):
        """ Get 12 day weather history from the earliest records in the database
        Args:
            city_value (str): Name of the city to query in the databas
            temp_value (str): String of either "Fahrenheit" or "Celsius"
        Returns:
            pd.DataFrame: Dataframe with the city (for debugging), date, maxtemp for the 12 day period
        """
        try:
            # Get min year of data from DB (either 60's, 70's or 80's)
            select_data = """
            SELECT
                CONCAT(City, ", " ,State, ", " ,Country) as City,
                MIN(YEAR(Date)) as 'Year'
            FROM DailyAvg
            JOIN StationDetails ON StationDetails.StationId = DailyAvg.StationId
            WHERE CONCAT(City, ", " ,State, ", " ,Country) = {}
            GROUP BY CONCAT(City, ", " ,State, ", " ,Country);
            """.format(("'" + city_value + "'"))

            df_minyear = self.run_sql_query(select_data)
            start_year = int(df_minyear['Year'])

            # Calculate the comparative period based on the start_year
            now = datetime.datetime.now()
            comparative_period = now.year - (now.year - start_year)
            start_date = datetime.date(comparative_period, now.month, now.day) - datetime.timedelta(days=7)
            end_date = datetime.date(comparative_period, now.month, now.day) + datetime.timedelta(days=5)

            # Format the start and end date for SQL
            start_date = ("'" + start_date.strftime('%Y-%m-%d') + "'")
            end_date = ("'" + end_date.strftime('%Y-%m-%d') + "'")

            # Get comparative daily temperatures
            select_data = """
            SELECT
                Date,
                ROUND(AVG(MaxTemp),2) as MaxTemp
            FROM DailyAvg
            JOIN StationDetails ON StationDetails.StationId = DailyAvg.StationId
            WHERE
                CONCAT(City, ", " ,State, ", " ,Country) = {}
                AND Date >= {} AND Date <= {}
            GROUP BY Date
            ORDER BY Date
            """.format(("'" + city_value + "'"), start_date, end_date)

            df = self.run_sql_query(select_data)

            # Rename column and drop date
            df = df.rename(columns={'MaxTemp': df.Date[0].year})
            df = df.drop(columns='Date')

            return df
        except TypeError:
            return

    def get_recent_weather(self, city_value, temp_value="Celsius"):
        """ Get 7 day weather history + 5 day forecast from today's date
        Args:
            city_value (str): Name of the city to query in the databas
            temp_value (str): String of either "Fahrenheit" or "Celsius"
        Returns:
            pd.DataFrame: Dataframe with the date, max, min and average temperatures for the past 7 days + forecast of coming 5
        """

        # Setup for get_7day_history function
        file = open("/Users/todddequincey/globalwarming/app/apixu_weather_api_key.txt")
        api_key = file.read()
        client = ApixuClient(api_key)

        # List of dictionatries of the data
        data = []

        # Get 7 day weather history
        # Individual API calls for historical data req, due to restrictions of free API
        now = datetime.datetime.now()  # TODO: Deal with time zones
        for i in range(0, 8):
            history = client.history(q=city_value, since=datetime.date(now.year, now.month, now.day) - datetime.timedelta(days=i))
            for day in history['forecast']['forecastday']:
                results = {
                    "Date": day['date'],
                    "Last 7 Days": day['day']['maxtemp_f'],
                    "Forecast": np.nan,
                    "MinTemp": day['day']['mintemp_f'],
                    "AvgTemp": day['day']['avgtemp_f'],
                    "MaxWind": day['day']['maxwind_kph'],
                    "TotalPrecip": day['day']['totalprecip_mm'],
                    "AvgVisib": day['day']['avgvis_km'],
                    "AvgHumid": day['day']['avghumidity'],
                    "Condition": day['day']['condition']['text'],
                    "UV": day['day']['uv']
                }
                data.append(results)

        # Get 5 day forecast
        forecast = client.forecast(q=city_value, days=6)
        for day in forecast['forecast']['forecastday']:
            results = {
                    "Date": day['date'],
                    "Last 7 Days": np.nan,
                    "Forecast": day['day']['maxtemp_f'],
                    "MinTemp": day['day']['mintemp_f'],
                    "AvgTemp": day['day']['avgtemp_f'],
                    "MaxWind": day['day']['maxwind_kph'],
                    "TotalPrecip": day['day']['totalprecip_mm'],
                    "AvgVisib": day['day']['avgvis_km'],
                    "AvgHumid": day['day']['avghumidity'],
                    "Condition": day['day']['condition']['text'],
                    "UV": day['day']['uv']
                }
            data.append(results)

        # Create dataframe of results
        df = pd.DataFrame(data, columns=['Date',
                                        'AvgHumid',
                                        'AvgVisib',
                                        'Condition',
                                        'MaxWind',
                                        'TotalPrecip',
                                        'UV',
                                        'MinTemp',
                                        'AvgTemp',
                                        'Forecast',
                                        'Last 7 Days'])
        df = df.sort_values('Date')
        df = df.drop_duplicates('Date')  # Drop dups in case of overlap of forecast + history dates
        df = df.reset_index(drop=True)
        df.loc[7, "Forecast"] = df.loc[7, "Last 7 Days"]  # Replace today np.nan forecast with actual MaxTemp

        # Get and join historical data to the df
        try:
            daily_hist = self.get_daily_history(city_value)
            df = df.join(daily_hist)

            # Return results in Fahrenheit or Celsius
            if temp_value == "Fahrenheit":
                return df
            elif temp_value == "Celsius":
                df = self.fahrenheit_to_celsius(df, ["Last 7 Days", "Forecast", df.columns[-1]])
                return df
        except TypeError:
            # Return results in Fahrenheit or Celsius
            if temp_value == "Fahrenheit":
                return df
            elif temp_value == "Celsius":
                df = self.fahrenheit_to_celsius(df, ["Last 7 Days", "Forecast"])
                return df
