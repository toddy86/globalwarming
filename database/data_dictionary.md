## StationRecords
* StationId - Weather station ID (WMO/DATSAV3 number).
* WBAN - Historical "Weather Bureau Air Force Navy" number.
* Date - The date of the daily weather recording.
* Temp - Mean temperature for the day in degrees Fahrenheit to tenths.  Missing data represented by 9999.9.
* TempPoints - 	Number of observations used in calculating mean temperature.
* Dew - Mean dew point for the day in degrees Fahrenheit to tenths.  Missing data represented by 9999.9
* DewPoints -	Number of observations used in calculating mean dew point.
* SLP	- Mean sea level pressure for the day in millibars to tenths.  Missing data represented by 9999.9
* SLPPoints -	Number of observations used in calculating mean sea level pressure.
* StationPressure - Mean station pressure for the day in millibars to tenths.  Missing data represented by 9999.9
* StationPressurePoints -	Number of observations used in calculating mean station pressure.
* Visib - Mean visibility for the day in miles to tenths.  Missing data represented by 999.9
* VisibPoints - Number of observations used in calculating mean visibility.
* WindSpeed -	Mean wind speed for the day in knots to tenths.  Missing data represented by 999.9
* WindSpeedPoints - Number of observations used in calculating mean wind speed.
* MaxSpeed - Maximum sustained wind speed reported for the day in knots to tenths. Missing data represented by 999.9
* Gust - Maximum wind gust reported for the day in knots to tenths.  Missing data represented by 999.9
* MaxTemp - Maximum temperature of the day measured in degrees Fahrenheit. 
* MinTemp - Minimum temperature of the day measured in degrees Fahrenheit.
* Precip - Amount of precipritation
* SnowDepth - Snow depth in inches to tenths--last report for the day if reported more than once.  Missing data represented by 999.9  Most stations do not report '0' on days with no snow on the ground--therefore, '999.9' will often appear on these days.
* Conditions - Indicators (1 = yes, 0 = no/not reported) for the occurrence during the day of: Fog ('F' - 1st digit). Rain or Drizzle ('R' - 2nd digit). Snow or Ice Pellets ('S' - 3rd digit). Hail ('H' - 4th digit). Thunder ('T' - 5th digit). Tornado or Funnel Cloud ('T' - 6th digit).

## StationDetails
* StationId - Station ID number (WMO/DATSAV3 number).
* WBAN - The historical "Weather Bureau Air Force Navy" number.
* StationName -	The name of the weather station.
* CountryId	- Two-digit code to identify the country where the weather station is located.
* ICAO	- ICAO ID
* Lat - Latitude in thousandths of decimal degrees of the weather station.
* Lon - Longitude in thousandths of decimal degrees of the weather station.
* Elevation - Elevation of the weather station in meters
* StartDate - Beginning period of record (YYYYMMDD) for the weather station. There may be reporting gaps within the P.O.R.
* EndDate - Ending period of record for the weather station (YYYYMMDD). There may be reporting gaps within the P.O.R.

## Countries
* CountryId - Two-digit code to identify the country where the weather station is located.
* Country - The name of the country.

## CO2
* Country - The name of the country.
* Year - The year which the CO2 emissions are recorded for.
* Emissions - The CO2 emissions for the year in million tonnes.