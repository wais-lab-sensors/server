-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 02, 2015 at 04:52 PM
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
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

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
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

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
-- Table structure for table `internal_temperature_readings`
--

CREATE TABLE IF NOT EXISTS `internal_temperature_readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(4) NOT NULL,
  `timestamp` datetime NOT NULL,
  `value` float NOT NULL COMMENT 'Celcius',
  PRIMARY KEY (`id`),
  KEY `device` (`device`),
  KEY `timestamp` (`timestamp`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

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
  `end` int(11) DEFAULT NULL COMMENT 'When the node was moved from here',
  PRIMARY KEY (`id`),
  KEY `device` (`device`,`location`,`start`,`end`),
  KEY `location` (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
-- Constraints for table `internal_temperature_readings`
--
ALTER TABLE `internal_temperature_readings`
  ADD CONSTRAINT `internal_temperature_readings_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `location_mapping`
--
ALTER TABLE `location_mapping`
  ADD CONSTRAINT `location_mapping_ibfk_2` FOREIGN KEY (`location`) REFERENCES `locations` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `location_mapping_ibfk_1` FOREIGN KEY (`device`) REFERENCES `devices` (`id`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
