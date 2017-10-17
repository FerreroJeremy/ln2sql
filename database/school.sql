-- phpMyAdmin SQL Dump
-- version 3.3.2
-- http://www.phpmyadmin.net
--
-- Serveur: localhost
-- Généré le : Ven 29 Mars 2013 à 13:31
-- Version du serveur: 5.1.41
-- Version de PHP: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


-- --------------------------------------------------------


CREATE TABLE IF NOT EXISTS `class` (
  `idClass` int(11) NOT NULL AUTO_INCREMENT,
  `classroom` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idClass`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;


INSERT INTO `class` (`idClass`, `classroom`) VALUES
(1, 'TPR1'),
(2, 'TPR2');

-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS `student` (
  `idStudent` int(11) NOT NULL AUTO_INCREMENT,
  `idClass` int(11) NOT NULL,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `firstname` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `age` int(11) NOT NULL,
  PRIMARY KEY (`idStudent`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;


INSERT INTO `student` (`idStudent`, `idClass`, `name`, `firstname`, `age`) VALUES
(1, 1, 'DI', 'Alain', 23),
(2, 1, 'EMMAR', 'Jean', 21),
(3, 2, 'TENRIEN', 'Jean', 20),
(4, 1, 'VEUPLU', 'John', 23),
(5, 1, 'EDEPRE', 'Rose', 22),
(6, 2, 'KILO', 'Sandy', 24);

-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS `teaching` (
  `idProf` int(11) NOT NULL,
  `idClass` int(11) NOT NULL,
  `field` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


INSERT INTO `teaching` (`idProf`, `idClass`, `field`) VALUES
(1, 1, 'Algorithm'),
(2, 1, 'Database');

-- --------------------------------------------------------


CREATE TABLE IF NOT EXISTS `professor` (
  `idProf` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `firstname` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idProf`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;


INSERT INTO `professor` (`idProf`, `name`, `firstname`) VALUES
(1, 'CEPTION', 'Alex'),
(2, 'KEND', 'Bowie'),
(3, 'EHA', 'Aline'),
(4, 'TOMI', 'Anna');
