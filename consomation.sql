-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 11 avr. 2024 à 15:21
-- Version du serveur : 10.4.22-MariaDB
-- Version de PHP : 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `consomation`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add water consumption', 7, 'add_waterconsumption'),
(26, 'Can change water consumption', 7, 'change_waterconsumption'),
(27, 'Can delete water consumption', 7, 'delete_waterconsumption'),
(28, 'Can view water consumption', 7, 'view_waterconsumption'),
(29, 'Can add energy consumption', 8, 'add_energyconsumption'),
(30, 'Can change energy consumption', 8, 'change_energyconsumption'),
(31, 'Can delete energy consumption', 8, 'delete_energyconsumption'),
(32, 'Can view energy consumption', 8, 'view_energyconsumption');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(8, 'Eau', 'energyconsumption'),
(7, 'Eau', 'waterconsumption'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-03-30 03:56:40.251643'),
(2, 'auth', '0001_initial', '2024-03-30 03:56:40.713790'),
(3, 'admin', '0001_initial', '2024-03-30 03:56:40.815938'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-03-30 03:56:40.823917'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-03-30 03:56:40.840995'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-03-30 03:56:40.889335'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-03-30 03:56:40.932229'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-03-30 03:56:40.945195'),
(9, 'auth', '0004_alter_user_username_opts', '2024-03-30 03:56:40.952176'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-03-30 03:56:40.994093'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-03-30 03:56:40.998053'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-03-30 03:56:41.005034'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-03-30 03:56:41.018001'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-03-30 03:56:41.029557'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-03-30 03:56:41.042343'),
(16, 'auth', '0011_update_proxy_permissions', '2024-03-30 03:56:41.048029'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-03-30 03:56:41.058884'),
(18, 'sessions', '0001_initial', '2024-03-30 03:56:41.096118'),
(19, 'Eau', '0001_initial', '2024-04-01 20:55:30.338444'),
(20, 'Eau', '0002_energyconsumption', '2024-04-03 16:17:00.083080');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `eau_energyconsumption`
--

CREATE TABLE `eau_energyconsumption` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `meter_reading` int(11) NOT NULL,
  `daily_consumption` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `eau_energyconsumption`
--

INSERT INTO `eau_energyconsumption` (`id`, `date`, `meter_reading`, `daily_consumption`) VALUES
(2, '2024-01-01', 0, 0),
(3, '2024-01-02', 29791121, 5328),
(4, '2024-01-03', 29796449, 5089),
(5, '2024-01-04', 29801538, 5274),
(6, '2024-01-05', 29806812, 5172),
(7, '2024-01-06', 29811984, 10679),
(8, '2024-01-07', 0, 0),
(9, '2024-01-08', 29822663, 5983),
(10, '2024-01-09', 29828646, 5769),
(11, '2024-01-10', 29834415, 6030),
(12, '2024-01-11', 29840445, 5539),
(13, '2024-01-12', 29845984, 6115),
(14, '2024-01-13', 29852099, 10431),
(15, '2024-01-14', 0, 0),
(16, '2024-01-15', 29862530, 5227),
(17, '2024-01-16', 29867757, 5080),
(18, '2024-01-17', 29872837, 4624),
(19, '2024-01-18', 29877461, 5269),
(20, '2024-01-19', 29882730, 5346),
(21, '2024-01-20', 29888076, 8766),
(22, '2024-01-21', 0, 0),
(23, '2024-01-22', 29896842, 6081),
(24, '2024-01-23', 29902923, 6124),
(25, '2024-01-24', 29909047, 5597),
(26, '2024-01-25', 29914644, 5297),
(27, '2024-01-26', 29919941, 5126),
(28, '2024-01-27', 29925067, 10145),
(29, '2024-01-28', 0, 0),
(30, '2024-01-29', 29935212, 5601),
(31, '2024-01-30', 29940813, 6076),
(32, '2024-01-31', 29946889, 5855),
(33, '2024-04-11', 31324, 22);

-- --------------------------------------------------------

--
-- Structure de la table `eau_waterconsumption`
--

CREATE TABLE `eau_waterconsumption` (
  `id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `meter_reading` int(11) NOT NULL,
  `daily_consumption` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `eau_waterconsumption`
--

INSERT INTO `eau_waterconsumption` (`id`, `date`, `meter_reading`, `daily_consumption`) VALUES
(2, '2024-01-01', 0, 0),
(3, '2024-01-02', 83555, 13),
(4, '2024-01-03', 83568, 30),
(5, '2024-01-04', 83598, 11),
(6, '2024-01-05', 83609, 10),
(7, '2024-01-06', 83619, 6),
(8, '2024-01-07', 0, 0),
(9, '2024-01-08', 83625, 13),
(10, '2024-01-09', 83638, 15),
(11, '2024-01-10', 83653, 14),
(12, '2024-01-11', 83667, 14),
(13, '2024-01-12', 83681, 15),
(14, '2024-01-13', 83696, 11),
(15, '2024-01-14', 0, 0),
(16, '2024-01-15', 83707, 14),
(17, '2024-01-16', 83721, 11),
(18, '2024-01-17', 83732, 10),
(19, '2024-01-18', 83742, 11),
(20, '2024-01-19', 83753, 14),
(21, '2024-01-20', 83767, 9),
(22, '2024-01-21', 0, 0),
(23, '2024-01-22', 83776, 31),
(24, '2024-01-23', 83807, 13),
(25, '2024-01-24', 83820, 15),
(26, '2024-01-25', 83835, 15),
(27, '2024-01-26', 83850, 19),
(28, '2024-01-27', 83869, 18),
(29, '2024-01-28', 0, 0),
(30, '2024-01-29', 83887, 15),
(31, '2024-01-30', 83902, 12),
(32, '2024-01-31', 83914, 12),
(33, '2024-01-04', 83598, 11);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Index pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `eau_energyconsumption`
--
ALTER TABLE `eau_energyconsumption`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `eau_waterconsumption`
--
ALTER TABLE `eau_waterconsumption`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT pour la table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT pour la table `eau_energyconsumption`
--
ALTER TABLE `eau_energyconsumption`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT pour la table `eau_waterconsumption`
--
ALTER TABLE `eau_waterconsumption`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
