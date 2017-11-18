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

--
-- Base de données: `ecole`
--

-- --------------------------------------------------------

--
-- Structure de la table `classe`
--

CREATE TABLE IF NOT EXISTS `classe` (
  `idClasse` int(11) NOT NULL AUTO_INCREMENT,
  `salle` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idClasse`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Contenu de la table `classe`
--

INSERT INTO `classe` (`idClasse`, `salle`) VALUES
(1, 'TPR1'),
(2, 'TPR2');

-- --------------------------------------------------------

--
-- Structure de la table `eleve`
--

CREATE TABLE IF NOT EXISTS `eleve` (
  `idEleve` int(11) NOT NULL AUTO_INCREMENT,
  `idClasse` int(11) NOT NULL,
  `nom` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `prenom` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `age` int(11) NOT NULL,
  PRIMARY KEY (`idEleve`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;

--
-- Contenu de la table `eleve`
--

INSERT INTO `eleve` (`idEleve`, `idClasse`, `nom`, `prenom`, `age`) VALUES
(1, 1, 'DI', 'Alain', 23),
(2, 1, 'EMMAR', 'Jean', 21),
(3, 2, 'TENRIEN', 'Jean', 20),
(4, 1, 'VEUPLU', 'John', 23),
(5, 1, 'EDEPRE', 'Rose', 22),
(6, 2, 'KILO', 'Sandy', 24);

-- --------------------------------------------------------

--
-- Structure de la table `enseigner`
--

CREATE TABLE IF NOT EXISTS `enseigner` (
  `idProf` int(11) NOT NULL,
  `idClasse` int(11) NOT NULL,
  `matiere` varchar(20) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Contenu de la table `enseigner`
--

INSERT INTO `enseigner` (`idProf`, `idClasse`, `matiere`) VALUES
(1, 1, 'Algorithme'),
(2, 1, 'BDD');

-- --------------------------------------------------------

--
-- Structure de la table `professeur`
--

CREATE TABLE IF NOT EXISTS `professeur` (
  `idProf` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `prenom` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`idProf`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- Contenu de la table `professeur`
--

INSERT INTO `professeur` (`idProf`, `nom`, `prenom`) VALUES
(1, 'CEPTION', 'Alex'),
(2, 'KEND', 'Bowie'),
(3, 'EHA', 'Aline'),
(4, 'TOMI', 'Anna');
