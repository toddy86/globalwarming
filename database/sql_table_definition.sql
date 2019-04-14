-- Create table with list of countries and their IDs
CREATE TABLE `Countries` (
  `CountryId` CHAR(2) NOT NULL,
  `CountryName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`CountryId`),
  UNIQUE KEY `CountryId` (`CountryId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create table with weather stations
CREATE TABLE `StationDetails` (
  `StationId` VARCHAR(6) NOT NULL,
  `WBAN` INT(6) NOT NULL,
  `StationName` VARCHAR(100) DEFAULT NULL,
  `CountryId` CHAR(2) DEFAULT NULL,
  `ICAO` VARCHAR(8) DEFAULT NULL,
  `Lat` DECIMAL(10,8) DEFAULT NULL, 
  `Lon` DECIMAL(11,8) DEFAULT NULL, 
  `Elevation` DECIMAL(5,1) DEFAULT NULL,
  `StartDate` DATE DEFAULT NULL,
  `EndDate` DATE DEFAULT NULL
  PRIMARY KEY (`StationId`),
  UNIQUE KEY `StationId` (`StationId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create table with daily weather station records
CREATE TABLE `StationRecords` (
  `StationId` varchar(6) NOT NULL,
  `WBAN` int(6) NOT NULL,
  `Date` date NOT NULL,
  `Temp` decimal(4,1) DEFAULT NULL,
  `TempPoints` int(11) DEFAULT NULL,
  `Dew` decimal(5,1) DEFAULT NULL,
  `DewPoints` int(11) DEFAULT NULL,
  `SLP` decimal(5,1) DEFAULT NULL,
  `SLPPoints` int(11) DEFAULT NULL,
  `StationPressure` decimal(5,1) DEFAULT NULL,
  `StationPressurePoints` int(11) DEFAULT NULL,
  `Visib` decimal(5,1) DEFAULT NULL,
  `VisibPoints` int(11) DEFAULT NULL,
  `WindSpeed` decimal(5,1) DEFAULT NULL,
  `WindSpeedPoints` int(11) DEFAULT NULL,
  `MaxWindSpeed` decimal(5,1) DEFAULT NULL,
  `Gust` decimal(5,1) DEFAULT NULL,
  `MaxTemp` decimal(5,1) DEFAULT NULL,
  `MinTemp` decimal(5,1) DEFAULT NULL,
  `Precip` decimal(5,2) DEFAULT NULL,
  `SnowDepth` decimal(5,1) DEFAULT NULL,
  `Conditions` decimal(7,1) DEFAULT NULL,
  PRIMARY KEY (`StationId`),
  UNIQUE KEY `StationId` (`StationId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create table with CO2 emission data
CREATE TABLE `CO2` (
  `Country` varchar(100) NOT NULL,
  `Year` smallint(4) NOT NULL,
  `Emissions` float DEFAULT NULL,
  PRIMARY KEY (`Country`,`Year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Set foreign key constraints
ALTER TABLE StationRecords
ADD FOREIGN KEY FK_StationRecords_StationDetails(StationId, WBAN)
REFERENCES StationDetails(StationId, WBAN)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE StationDetails
ADD FOREIGN KEY FK_StationDetails_Countries(CountryId)
REFERENCES Countries(CountryId)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Countries
ADD FOREIGN KEY FK_Countries_CO2(Country)
REFERENCES CO2(Country)
ON DELETE NO ACTION
ON UPDATE NO ACTION;