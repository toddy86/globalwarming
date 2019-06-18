# Global Warming Project
The objective of this project is to create an interactive dashboard which provides information about how global warming is affecting individual cities around the globe. It is hoped that if people are able to see the impact which global warming is having on the city in which they live, that they will be more inclined to take action and help prevent further damage to the globe.

## Data Source
The data are obtained from the National Centers for Environmental Information, who hosts and provides public access to one of the most significant archives for environmental data on Earth. 

The data being used is the Global Surface Summary of the Day ("GSOD") dataset, which provides daily weather records from 1929 to present day, although the data from 1973 onwards is considered the most complete. 

URL: https://data.nodc.noaa.gov/cgi-bin/iso?id=gov.noaa.ncdc:C00516 

Data were downloaded as .tar.gz files for each calendar year. The zipped files contained a single CSV file for each weather station in the dataset. 

To extract the CSV files, the following command was run in the terminal:

for g in *.tar.gz; do tar -xjf $g; done


## Database
The database folder contains: 
* SQL code user to generate the MySQL database, tables and constraints
* **TODO: Database schema diagram** 
* **TODO: Fix NaN before loading final data into database**
* Data dictionary

The database has been created using MySQL 5.7.26

## Data Wrangling
**Station Details**  
The following key data cleaning and pre-processing steps have been completed in a Jupyter notebook:
* Using Google Maps API, fetched the geolocation details of the weather stations (e.g. city name, country etc) using the lat and long attributes
  
Things to do differently next time:  
* Filter out all weather stations with missing lat / lon coordinates before calling Google Maps API. This would have saved 1,700 unnecessary API calls. I was already part way through the process when I realised. 

**Weather Station Records (GSOD)**  
The following key data cleaning and pre-processing steps have been completed in a Jupyter notebook:  
* Dropped unnecessary variables (e.g. latitude, longitude)
* Replace missing values (999.9 and 9999.9 with np.NaN)
* Updated column names for consistency
* Calculated monthly temperature averages (daily too granular and too heavily influenced by outliers)
* Calculated monthly minimum and maximum temperatues
* Saved the data to feater format for faster access in Python
* Saved the data to JSON for portability (if required)
* Loaded the data to MySQL database


