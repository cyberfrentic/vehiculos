-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-12-2019 a las 20:56:17
-- Versión del servidor: 5.6.21
-- Versión de PHP: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `vehiculos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE IF NOT EXISTS `users` (
`id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(93) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `privilegios` varchar(20) DEFAULT NULL,
  `idCiudad` int(11) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `privilegios`, `idCiudad`, `created_date`) VALUES
(1, 'hugocanul', 'pbkdf2:sha256:50000$cfbv5P4i$7770be9bf01a6aa9e8455ea19ff08587de7411b19389cb005000461b7b056ccf', 'cyber.frenetic@gmail.com', '0.0.0.1.0', 4, '2018-11-07 07:28:41'),
(7, 'merlenovelo', 'pbkdf2:sha256:50000$U5QjJCZS$89077d6e67b92a67ae4094cfd7af15d74f5f95ca4c3ec66b98e27605f8f95067', 'merlenovelo@homail.com', '1.1.1.0.1', 4, '2019-06-18 11:56:12'),
(5, 'hugocanul2', 'pbkdf2:sha256:50000$cfbv5P4i$7770be9bf01a6aa9e8455ea19ff08587de7411b19389cb005000461b7b056ccf', 'cyber.frenetic@gmail.com', '0.1.0.0.0', 4, '2019-03-25 13:55:24'),
(8, 'oscarQuime', 'pbkdf2:sha256:50000$qOwueiCu$8511bb292f018cfff0b440af3cc44c8bc10a288accea3d04dd1b6b0724aa4b03', 'supcrack6@hotmail.com', '1.1.1.0.1', 2, '2019-09-02 13:18:14'),
(9, 'martasosa', 'pbkdf2:sha256:50000$zZMlXuLR$787e70f7124f07c1a655fc22f6ecfb695c2567b7eef68be7a569b7af40bd411c', 'somm62@hotmail.com', '1.1.1.0.1', 4, '2019-10-21 08:58:10'),
(10, 'pascualmtz', 'pbkdf2:sha256:50000$v5oFxBnL$f55e277b00d30711ca915fa897807dc67530d2906f7e813f7206edda8c44cc0f', 'pmtzg6904@hotmail.com', '1.1.1.0.1', 4, '2019-12-11 10:53:38');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
 ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=11;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
