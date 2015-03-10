-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 10, 2015 at 02:04 PM
-- Server version: 5.5.41-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `wais_sensors`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `accelerometer_converted`
--
CREATE TABLE IF NOT EXISTS `accelerometer_converted` (
`device` varchar(4)
,`timestamp` datetime
,`pitch` double(17,0)
,`roll` double(17,0)
);
-- --------------------------------------------------------

--
-- Table structure for table `accelerometer_readings`
--

CREATE TABLE IF NOT EXISTS `accelerometer_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  `z` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12563 ;

-- --------------------------------------------------------

--
-- Table structure for table `battery_readings`
--

CREATE TABLE IF NOT EXISTS `battery_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'Volts',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12565 ;

-- --------------------------------------------------------

--
-- Stand-in structure for view `combined`
--
CREATE TABLE IF NOT EXISTS `combined` (
`device` varchar(4)
,`timestamp` datetime
,`voltage` float
,`temperature` float
,`x` int(11)
,`y` int(11)
,`z` int(11)
);
-- --------------------------------------------------------

--
-- Stand-in structure for view `current_locations`
--
CREATE TABLE IF NOT EXISTS `current_locations` (
`device` varchar(4)
,`description` text
);
-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE IF NOT EXISTS `devices` (
  `id` varchar(4) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `humidity_readings`
--

CREATE TABLE IF NOT EXISTS `humidity_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'relative humidity %',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`,`timestamp`),
  KEY `device` (`device`,`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=32 ;

-- --------------------------------------------------------

--
-- Table structure for table `internal_temperature_readings`
--

CREATE TABLE IF NOT EXISTS `internal_temperature_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'Celcius',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12573 ;

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

CREATE TABLE IF NOT EXISTS `locations` (
  `id` varchar(2) NOT NULL,
  `Description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `location_mapping`
--

CREATE TABLE IF NOT EXISTS `location_mapping` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `location` varchar(2) NOT NULL,
  `start` datetime NOT NULL COMMENT 'When the node was first deployed here',
  `end` datetime DEFAULT NULL COMMENT 'When the node was moved from here',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`start`),
  KEY `device` (`device`,`location`,`start`,`end`),
  KEY `location` (`location`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `temperature_readings`
--

CREATE TABLE IF NOT EXISTS `temperature_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'Celcius',
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_2` (`device`,`timestamp`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=115 ;

-- --------------------------------------------------------

--
-- Structure for view `accelerometer_converted`
--
DROP TABLE IF EXISTS `accelerometer_converted`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `accelerometer_converted` AS select `accelerometer_readings`.`device` AS `device`,`accelerometer_readings`.`timestamp` AS `timestamp`,round(((atan(`accelerometer_readings`.`y`,`accelerometer_readings`.`z`) * 180) / pi()),0) AS `pitch`,round(((atan(`accelerometer_readings`.`x`,sqrt(((`accelerometer_readings`.`y` * `accelerometer_readings`.`y`) + (`accelerometer_readings`.`z` * `accelerometer_readings`.`z`)))) * 180) / pi()),0) AS `roll` from `accelerometer_readings` where 1;

-- --------------------------------------------------------

--
-- Structure for view `combined`
--
DROP TABLE IF EXISTS `combined`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `combined` AS select `a`.`device` AS `device`,`a`.`timestamp` AS `timestamp`,`b`.`value` AS `voltage`,`i`.`value` AS `temperature`,`a`.`x` AS `x`,`a`.`y` AS `y`,`a`.`z` AS `z` from ((`accelerometer_readings` `a` join `battery_readings` `b`) join `internal_temperature_readings` `i`) where ((`a`.`device` = `b`.`device`) and (`a`.`device` = `i`.`device`) and (`a`.`timestamp` = `b`.`timestamp`) and (`a`.`timestamp` = `i`.`timestamp`));

-- --------------------------------------------------------

--
-- Structure for view `current_locations`
--
DROP TABLE IF EXISTS `current_locations`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `current_locations` AS select `lm`.`device` AS `device`,`l`.`Description` AS `description` from (`location_mapping` `lm` left join `locations` `l` on((`lm`.`location` = `l`.`id`))) where isnull(`lm`.`end`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accelerometer_readings`
--
ALTER TABLE `accelerometer_readings`
  ADD CONSTRAINT `accelerometer_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `battery_readings`
--
ALTER TABLE `battery_readings`
  ADD CONSTRAINT `battery_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `humidity_readings`
--
ALTER TABLE `humidity_readings`
  ADD CONSTRAINT `humidity_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `internal_temperature_readings`
--
ALTER TABLE `internal_temperature_readings`
  ADD CONSTRAINT `internal_temperature_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `location_mapping`
--
ALTER TABLE `location_mapping`
  ADD CONSTRAINT `location_mapping_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `location_mapping_ibfk_2` FOREIGN KEY (`location`) REFERENCES `locations` (`id`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
