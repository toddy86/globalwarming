# Global Warming Project

**THIS PROJECT IS STILL A WORK IN PROGRESS**  
Last updated 07 July 2019

## Project Goal
The objective of this project is to create an interactive dashboard which provides information about how global warming is affecting individual cities around the globe. It is hoped that if people are able to see the impact which global warming is having on the city in which they live, that they will be more inclined to take action and help prevent further damage to the globe.
  
The technical objective of this project is to learn how to use the Dash library for creating interactive dashboards, along with continiously improve my general tech skills (SQL, git, APIs etc).

## Technology Used
* Python and common libraries (i.e. Pandas, Dash)
* MySQL / SQL
* Google Maps API
* Git

## Skills Used
* Python programming
* Data collection from multiple sources
* Data aggregation, enrichment and cleaning
* Database design
* SQL 
* Data visualisation
* Git
* Statistics

## Data Sources
### Global Surface Summary of the Day Weather Data
The data are obtained from the National Centers for Environmental Information, who hosts and provides public access to one of the most significant archives for environmental data on Earth. 

The data being used is the Global Surface Summary of the Day ("GSOD") dataset, which provides daily weather records from 1929 to present day, although the data from 1973 onwards is considered the most complete. 

URL: https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.ncdc:C00516 

Data were downloaded as .tar.gz files for each calendar year. The zipped files contained a single CSV file for each weather station in the dataset. 

To extract the CSV files, the following command was run in the terminal:

for g in \*.tar.gz; do tar -xjf $g; done

### Weather Station Location Data
The GSOD weather data has been enriched by obtaining the name of the city, state and country where the weather station is located. These data were obtained from the Google Geocoding API, using the lat and lon coordinates of the weather station. 

https://developers.google.com/maps/documentation/geocoding/start

### Weather Forecast Data
The 5 day weather forecast data have been obtained using the APIUX Weather API. The weather API was queried using the city name obtained from the Google Geocoding API

https://www.apixu.com/api.aspx

## Database
The database folder contains: 
* SQL code user to generate the MySQL database, tables and constraints
* **TODO: Finalise and upload the database schema / ERD** 
* Data dictionary

The database has been created using MySQL 5.7.26

## Data Wrangling
**Station Details**  
The following key data cleaning and pre-processing steps have been completed in a Jupyter notebook:
* Using Google Maps API, fetched the geolocation details of the weather stations (e.g. city name, country etc) using the lat and long attributes
  
**Weather Station Records (GSOD)**  
The following key data cleaning and pre-processing steps have been completed in a Jupyter notebook:  
* Dropped unnecessary variables (e.g. latitude, longitude)
* Replace missing values (999.9 and 9999.9 with np.NaN)
* Updated column names for consistency
* Calculated monthly temperature averages (daily too granular and too heavily influenced by outliers)
* Calculated monthly minimum and maximum temperatues
* Saved the data to feater format for faster access in Python
* Loaded the data to MySQL database

**Redundant Weather Stations**  
* Completed set intersection of StationDetails to StationRecords to ensure foreign key constraints do not fail + removal of redundant data

**Data Enrichment**  
* Enriched the GSOD data by adding in the city, state and country name where the weather station is located. Data obtained using the Google Geocoding API, based on the lat and lon coordinates of the weather station


**To-do List**  
* Implement navigation pane to other pages
* Implement 5-day maximum temperature forecast page based on an machine learning algorithm to predict the temperature. Compare ML prediction to met office forecast
* Implement a long-range (i.e. 20-50 year) forecast of expected global temperatures using statistical / machine learning methods
* Host the app on heroku

## Challenges  
During the development of this project, there have been many technical and knowledge gap challenges which I have needed to overcome. These challenges have included:  
* Building the app whilst learning the new frameworks (Dash and Plotly) on the go.
* Effectively cleaning and managing a big dataset with limited resources (i.e. I didn't want to pay for Google Big Query or other services to make managing a very large dataset easy)
* Finding an API for the 5-day weather forecast  which was 1) free 2) provided historical data (most provide forecasts) and 3) looked suitable to work with the city names used in the dataset. Many of the old APIs (Yahoo, Wunderground) had been decommissioned.

## Other Notes  
* Later discovered that the NOAA GSOD dataset is freely available on Google Big Query. Whilst I could have used this, it would not have provided me with the opportunity to display data collection, cleaning and SQL skills. A new version of the app may be created in the future which directly taps into the data on Big Query
https://console.cloud.google.com/marketplace/details/noaa-public/gsod 


I will update the above with more details, including the lessons learnt and how I overcame the challenges in due course.

## Screenshots
The following are a few examples of the current version of the app. These will be updated as the app progresses.

**Dashboard in degrees Celsius**   
![](https://github.com/toddy86/globalwarming/blob/master/screenshots/Screenshot1.png)

**Searching for cities in the database**   
![](https://github.com/toddy86/globalwarming/blob/master/screenshots/Screenshot2.png)

**Updating the graph to only display the maximum temperature**   
![](https://github.com/toddy86/globalwarming/blob/master/screenshots/Screenshot3.png)

**New sidebar menu**   
![](https://github.com/toddy86/globalwarming/blob/master/screenshots/screenshot4.png)

