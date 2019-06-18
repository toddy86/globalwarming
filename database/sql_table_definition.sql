-- Create database
CREATE DATABASE `globalwarming`;
USE `globalwarming`;

-- Create table with weather stations
CREATE TABLE `StationDetails` (
  `StationId` VARCHAR(12) NOT NULL,
  `StationName` VARCHAR(100) DEFAULT NULL,
  `Elevation` DECIMAL(6,1) DEFAULT NULL,
  `StartDate` DATE DEFAULT NULL,
  `EndDate` DATE DEFAULT NULL,
  `City` VARCHAR(100) NOT NULL,
  `State` VARCHAR(100) DEFAULT NULL,
  `Country` VARCHAR(100) NOT NULL,
  `Lat` DECIMAL(10,8) DEFAULT NULL, 
  `Lon` DECIMAL(11,8) DEFAULT NULL, 
  PRIMARY KEY (`StationId`),
  UNIQUE KEY `StationId` (`StationId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Create table with monthly weather station records
CREATE TABLE `StationRecords` (
  `StationId` varchar(12) NOT NULL,
  `Year` int(4) NOT NULL,
  `Month` int(2) NOT NULL,
  `Temp` decimal(6,3) DEFAULT NULL,
  `Dew` decimal(7,3) DEFAULT NULL,
  `SLP` decimal(7,3) DEFAULT NULL,
  `StationPressure` decimal(7,3) DEFAULT NULL,
  `Visib` decimal(7,3) DEFAULT NULL,
  `WindSpeed` decimal(7,3) DEFAULT NULL,
  `MaxWindSpeed` decimal(7,3) DEFAULT NULL,
  `Gust` decimal(7,3) DEFAULT NULL,
  `AvgMaxTemp` decimal(7,3) DEFAULT NULL,
  `AvgMinTemp` decimal(7,3) DEFAULT NULL,
  `Precip` decimal(7,3) DEFAULT NULL,
  `SnowDepth` decimal(7,3) DEFAULT NULL,
  `MaxTemp` decimal(7,3) DEFAULT NULL,
  `MaxMinTemp` decimal(7,3) DEFAULT NULL,
  `MinMaxTemp` decimal(7,3) DEFAULT NULL,
  `MinTemp` decimal(7,3) DEFAULT NULL,
  `NumberDailyRecords` int(2) DEFAULT NULL,
  PRIMARY KEY (`StationId`,`Year`,`Month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Set foreign key constraints
ALTER TABLE StationRecords
ADD FOREIGN KEY FK_StationRecords_StationDetails(StationId)
REFERENCES StationDetails(StationId)
ON DELETE NO ACTION
ON UPDATE NO ACTION;








-- OLD KEPT JUST IN CASE
-- Create table with list of countries and their IDs
CREATE TABLE `Countries` (
  `CountryId` CHAR(2) NOT NULL,
  `CountryName` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`CountryId`),
  UNIQUE KEY `CountryId` (`CountryId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- Create table with CO2 emission data
CREATE TABLE `CO2` (
  `Country` varchar(100) NOT NULL,
  `Year` smallint(4) NOT NULL,
  `Emissions` float DEFAULT NULL,
  PRIMARY KEY (`Country`,`Year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE Countries
ADD FOREIGN KEY FK_Countries_CO2(Country)
REFERENCES CO2(Country)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE StationDetails
ADD FOREIGN KEY FK_StationDetails_Countries(CountryId)
REFERENCES Countries(CountryId)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
