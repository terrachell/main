-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Апр 07 2026 г., 17:30
-- Версия сервера: 12.2.2-MariaDB
-- Версия PHP: 8.5.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `messager`
--
CREATE DATABASE IF NOT EXISTS `messager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `messager`;

-- --------------------------------------------------------

--
-- Структура таблицы `chats`
--

CREATE TABLE `chats` (
  `ID` int(11) NOT NULL,
  `chat_id` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `created_at_int` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `chats`
--

INSERT INTO `chats` (`ID`, `chat_id`, `user_id`, `message`, `created_at`, `created_at_int`) VALUES
(73, '1', 4, 'dghxdfgjcfhjc', '2026-04-03 05:53:56', 1775195636);

--
-- Триггеры `chats`
--
DELIMITER $$
CREATE TRIGGER `chats_set_created_int` BEFORE INSERT ON `chats` FOR EACH ROW SET NEW.created_at_int = UNIX_TIMESTAMP(NEW.created_at)
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `chats_update_created_int` BEFORE UPDATE ON `chats` FOR EACH ROW SET NEW.created_at_int = UNIX_TIMESTAMP(NEW.created_at)
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Структура таблицы `private_room`
--

CREATE TABLE `private_room` (
  `ID` int(11) NOT NULL,
  `user0` varchar(16) NOT NULL,
  `user1` varchar(16) NOT NULL,
  `hash` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `private_room`
--

INSERT INTO `private_room` (`ID`, `user0`, `user1`, `hash`) VALUES
(14, 'taga', 'user1', '116e30a3c16783d5b32ff70ecd34c7a89a2e316966905fc87fba113fa1055d69');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `username` varchar(16) NOT NULL,
  `password` varchar(64) NOT NULL,
  `chats` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`ID`, `username`, `password`, `chats`) VALUES
(3, 'taga', '$2b$12$zuMnQ3lLa0dTEzLlBaInHe2SIhGtbnhUbSnhzoQtFlABtHdTkWa6W', '1'),
(4, 'user1', '$2b$12$W83g0CeS.mnFYlo4wrKrqOERYB7YolR1DE.zKJqHF5/sReGlbDOmS', '1');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `chats`
--
ALTER TABLE `chats`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `private_room`
--
ALTER TABLE `private_room`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `chats`
--
ALTER TABLE `chats`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

--
-- AUTO_INCREMENT для таблицы `private_room`
--
ALTER TABLE `private_room`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
