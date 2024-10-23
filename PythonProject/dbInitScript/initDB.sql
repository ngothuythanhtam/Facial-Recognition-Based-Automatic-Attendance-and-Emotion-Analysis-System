-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: face_recognition
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `acc_ID` int(11) NOT NULL AUTO_INCREMENT,
  `acc_username` varchar(255) NOT NULL,
  `acc_password` varchar(255) NOT NULL,
  `role_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`acc_ID`),
  UNIQUE KEY `acc_username` (`acc_username`),
  KEY `role_ID` (`role_ID`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`role_ID`) REFERENCES `roles` (`role_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,'admin','admin',3),(2,'B2111989','1',1),(3,'B2111959','1',1),(4,'B2111949','1',1),(5,'1','1',3),(6,'B2105661','1',1),(7,'A0005','1',2),(10,'A0002','1',2);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `administrator`
--

DROP TABLE IF EXISTS `administrator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrator` (
  `ad_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ad_code` varchar(10) NOT NULL,
  `ad_name` varchar(255) NOT NULL,
  `ad_phoneNumber` varchar(10) DEFAULT NULL,
  `ad_pass` varchar(15) NOT NULL,
  PRIMARY KEY (`ad_ID`),
  UNIQUE KEY `ad_code` (`ad_code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrator`
--

LOCK TABLES `administrator` WRITE;
/*!40000 ALTER TABLE `administrator` DISABLE KEYS */;
INSERT INTO `administrator` VALUES (1,'1','Thanh Tam','0123456789','1');
/*!40000 ALTER TABLE `administrator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `att_ID` int(11) NOT NULL AUTO_INCREMENT,
  `studying_st_code` varchar(8) DEFAULT NULL,
  `studying_clCourse_ID` int(11) DEFAULT NULL,
  `session_date` date DEFAULT NULL,
  `time_status` time DEFAULT NULL,
  PRIMARY KEY (`att_ID`),
  UNIQUE KEY `studying_st_code` (`studying_st_code`,`studying_clCourse_ID`,`session_date`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`studying_st_code`, `studying_clCourse_ID`) REFERENCES `studying` (`st_code`, `clCourse_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=261 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (1,'B2105681',213,'2024-08-05','16:59:53'),(2,'B2105684',213,'2024-08-05','17:00:26'),(3,'B2105695',213,'2024-08-05','16:59:59'),(4,'B2110011',213,'2024-08-05','16:59:59'),(5,'B2110058',213,'2024-08-05','17:00:27'),(6,'B2111915',213,'2024-08-05','16:59:59'),(7,'B2111930',213,'2024-08-05','16:59:59'),(8,'B2111936',213,'2024-08-05','17:00:28'),(9,'B2111946',213,'2024-08-05','16:59:59'),(10,'B2111949',213,'2024-08-05','16:59:59'),(11,'B2111955',213,'2024-08-05','17:00:29'),(12,'B2111956',213,'2024-08-05','16:59:59'),(13,'B2111959',213,'2024-08-05','16:59:59'),(14,'B2111994',213,'2024-08-05','17:00:30'),(15,'B2111995',213,'2024-08-05','16:59:59'),(16,'B2111996',213,'2024-08-05','16:59:59'),(17,'B2112000',213,'2024-08-05','17:00:31'),(18,'B2112004',213,'2024-08-05','16:59:59'),(19,'B2112010',213,'2024-08-05','16:59:59'),(20,'B2112011',213,'2024-08-05','17:00:32'),(41,'B2105681',214,'2024-08-06','16:59:53'),(42,'B2105684',214,'2024-08-06','17:00:26'),(43,'B2105695',214,'2024-08-06','16:59:59'),(44,'B2110011',214,'2024-08-06','16:59:59'),(45,'B2110058',214,'2024-08-06','17:00:27'),(46,'B2111915',214,'2024-08-06','16:59:59'),(47,'B2111930',214,'2024-08-06','16:59:59'),(48,'B2111936',214,'2024-08-06','17:00:28'),(49,'B2111946',214,'2024-08-06','16:59:59'),(50,'B2111949',214,'2024-08-06','16:59:59'),(51,'B2111955',214,'2024-08-06','17:00:29'),(52,'B2111956',214,'2024-08-06','16:59:59'),(53,'B2111959',214,'2024-08-06','16:59:59'),(54,'B2111994',214,'2024-08-06','17:00:30'),(55,'B2111995',214,'2024-08-06','16:59:59'),(56,'B2111996',214,'2024-08-06','16:59:59'),(57,'B2112000',214,'2024-08-06','17:00:31'),(58,'B2112004',214,'2024-08-06','16:59:59'),(59,'B2112010',214,'2024-08-06','16:59:59'),(60,'B2112011',214,'2024-08-06','17:00:32'),(61,'B2105681',215,'2024-08-06','07:00:53'),(62,'B2105684',215,'2024-08-06','07:00:26'),(63,'B2105695',215,'2024-08-06','07:00:59'),(64,'B2110011',215,'2024-08-06','07:00:59'),(65,'B2110058',215,'2024-08-06','07:00:27'),(66,'B2111915',215,'2024-08-06','07:00:59'),(67,'B2111930',215,'2024-08-06','07:00:59'),(68,'B2111936',215,'2024-08-06','07:00:28'),(69,'B2111946',215,'2024-08-06','07:00:59'),(70,'B2111949',215,'2024-08-06','07:00:59'),(71,'B2111955',215,'2024-08-06','07:00:29'),(72,'B2111956',215,'2024-08-06','07:00:59'),(73,'B2111959',215,'2024-08-06','07:00:59'),(74,'B2111994',215,'2024-08-06','07:00:30'),(75,'B2111995',215,'2024-08-06','07:00:59'),(76,'B2111996',215,'2024-08-06','07:00:59'),(77,'B2112000',215,'2024-08-06','07:00:31'),(78,'B2112004',215,'2024-08-06','07:00:59'),(79,'B2112010',215,'2024-08-06','07:00:59'),(80,'B2112011',215,'2024-08-06','07:00:32'),(81,'B2105681',216,'2024-08-07','07:00:53'),(82,'B2105684',216,'2024-08-07','07:00:26'),(83,'B2105695',216,'2024-08-07','07:00:59'),(84,'B2110011',216,'2024-08-07','07:00:59'),(85,'B2110058',216,'2024-08-07','07:00:27'),(86,'B2111915',216,'2024-08-07','07:00:59'),(87,'B2111930',216,'2024-08-07','07:00:59'),(88,'B2111936',216,'2024-08-07','07:00:28'),(89,'B2111946',216,'2024-08-07','07:00:59'),(90,'B2111949',216,'2024-08-07','07:00:59'),(91,'B2111955',216,'2024-08-07','07:00:29'),(92,'B2111956',216,'2024-08-07','07:00:59'),(93,'B2111959',216,'2024-08-07','07:00:59'),(94,'B2111994',216,'2024-08-07','07:00:30'),(95,'B2111995',216,'2024-08-07','07:00:59'),(96,'B2111996',216,'2024-08-07','07:00:59'),(97,'B2112000',216,'2024-08-07','07:00:31'),(98,'B2112004',216,'2024-08-07','07:00:59'),(99,'B2112010',216,'2024-08-07','07:00:59'),(100,'B2112011',216,'2024-08-07','07:00:32'),(101,'B2105681',217,'2024-08-07','13:00:53'),(102,'B2105684',217,'2024-08-07','13:00:26'),(103,'B2105695',217,'2024-08-07','13:00:59'),(104,'B2110011',217,'2024-08-07','13:00:59'),(105,'B2110058',217,'2024-08-07','13:00:27'),(106,'B2111915',217,'2024-08-07','13:00:59'),(107,'B2111930',217,'2024-08-07','13:00:59'),(108,'B2111936',217,'2024-08-07','13:00:28'),(109,'B2111946',217,'2024-08-07','13:00:59'),(110,'B2111949',217,'2024-08-07','13:00:59'),(111,'B2111955',217,'2024-08-07','13:00:29'),(112,'B2111956',217,'2024-08-07','13:00:59'),(113,'B2111959',217,'2024-08-07','13:00:59'),(114,'B2111994',217,'2024-08-07','13:00:30'),(115,'B2111995',217,'2024-08-07','13:00:59'),(116,'B2111996',217,'2024-08-07','13:00:59'),(117,'B2112000',217,'2024-08-07','13:00:31'),(118,'B2112004',217,'2024-08-07','13:00:59'),(119,'B2112010',217,'2024-08-07','13:00:59'),(120,'B2112011',217,'2024-08-07','13:00:32'),(121,'B2105681',218,'2024-08-08','13:00:53'),(122,'B2105684',218,'2024-08-08','13:00:26'),(123,'B2105695',218,'2024-08-08','13:00:59'),(124,'B2110011',218,'2024-08-08','13:00:59'),(125,'B2110058',218,'2024-08-08','13:00:27'),(126,'B2111915',218,'2024-08-08','13:00:59'),(127,'B2111930',218,'2024-08-08','13:00:59'),(128,'B2111936',218,'2024-08-08','13:00:28'),(129,'B2111946',218,'2024-08-08','13:00:59'),(130,'B2111949',218,'2024-08-08','13:00:59'),(131,'B2111955',218,'2024-08-08','13:00:29'),(132,'B2111956',218,'2024-08-08','13:00:59'),(133,'B2111959',218,'2024-08-08','13:00:59'),(134,'B2111994',218,'2024-08-08','13:00:30'),(135,'B2111995',218,'2024-08-08','13:00:59'),(136,'B2111996',218,'2024-08-08','13:00:59'),(137,'B2112000',218,'2024-08-08','13:00:31'),(138,'B2112004',218,'2024-08-08','13:00:59'),(139,'B2112010',218,'2024-08-08','13:00:59'),(140,'B2112011',218,'2024-08-08','13:00:32'),(141,'B2105661',213,'2024-08-05',NULL),(142,'B2105661',213,'2024-08-12','17:00:26'),(143,'B2105661',213,'2024-08-19','16:59:59'),(144,'B2105661',213,'2024-08-26','16:59:59'),(145,'B2105661',213,'2024-09-02',NULL),(146,'B2105661',213,'2024-09-09','16:59:59'),(147,'B2105661',213,'2024-09-16','16:59:59'),(148,'B2105661',213,'2024-09-23',NULL),(149,'B2105661',213,'2024-09-30','16:59:59'),(150,'B2105661',213,'2024-10-07',NULL),(151,'B2105661',213,'2024-10-14',NULL),(152,'B2105661',213,'2024-10-21','16:59:59'),(153,'B2105661',213,'2024-10-28',NULL),(154,'B2105661',213,'2024-11-04','17:00:30'),(155,'B2105661',213,'2024-11-11','16:59:59'),(156,'B2105661',213,'2024-11-18',NULL),(157,'B2105661',213,'2024-11-25','17:00:31'),(158,'B2105661',213,'2024-12-02','16:59:59'),(159,'B2105661',213,'2024-12-09','16:59:59'),(160,'B2105661',213,'2024-12-16',NULL),(161,'B2105661',214,'2024-08-06','16:59:53'),(162,'B2105661',214,'2024-08-13','17:00:26'),(163,'B2105661',214,'2024-08-20','16:59:59'),(164,'B2105661',214,'2024-08-27','16:59:59'),(165,'B2105661',214,'2024-09-03','17:00:27'),(166,'B2105661',214,'2024-09-10','16:59:59'),(167,'B2105661',214,'2024-09-17','16:59:59'),(168,'B2105661',214,'2024-09-24','17:00:28'),(169,'B2105661',214,'2024-10-01','16:59:59'),(170,'B2105661',214,'2024-10-08','16:59:59'),(171,'B2105661',214,'2024-10-15','17:00:29'),(172,'B2105661',214,'2024-10-22','16:59:59'),(173,'B2105661',214,'2024-10-29','16:59:59'),(174,'B2105661',214,'2024-11-05','17:00:30'),(175,'B2105661',214,'2024-11-12','16:59:59'),(176,'B2105661',214,'2024-11-19','16:59:59'),(177,'B2105661',214,'2024-11-26','17:00:31'),(178,'B2105661',214,'2024-12-03','16:59:59'),(179,'B2105661',214,'2024-12-10','16:59:59'),(180,'B2105661',214,'2024-12-17','17:00:32'),(181,'B2105661',215,'2024-08-06','07:00:53'),(182,'B2105661',215,'2024-08-13','07:00:26'),(183,'B2105661',215,'2024-08-20','07:00:59'),(184,'B2105661',215,'2024-08-27','07:00:59'),(185,'B2105661',215,'2024-09-03','07:00:27'),(186,'B2105661',215,'2024-09-10','07:00:59'),(187,'B2105661',215,'2024-09-17','07:00:59'),(188,'B2105661',215,'2024-09-24','07:00:28'),(189,'B2105661',215,'2024-10-01','07:00:59'),(190,'B2105661',215,'2024-10-08','07:00:59'),(191,'B2105661',215,'2024-10-15','07:00:29'),(192,'B2105661',215,'2024-10-22','07:00:59'),(193,'B2105661',215,'2024-10-29','07:00:59'),(194,'B2105661',215,'2024-11-05','07:00:30'),(195,'B2105661',215,'2024-11-12','07:00:59'),(196,'B2105661',215,'2024-11-19','07:00:59'),(197,'B2105661',215,'2024-11-26','07:00:31'),(198,'B2105661',215,'2024-12-03','07:00:59'),(199,'B2105661',215,'2024-12-10','07:00:59'),(200,'B2105661',215,'2024-12-17','07:00:32'),(201,'B2105661',216,'2024-08-07','07:00:53'),(202,'B2105661',216,'2024-08-14','07:00:26'),(203,'B2105661',216,'2024-08-21','07:00:59'),(204,'B2105661',216,'2024-08-28','07:00:59'),(205,'B2105661',216,'2024-09-04','07:00:27'),(206,'B2105661',216,'2024-09-11','07:00:59'),(207,'B2105661',216,'2024-09-18','07:00:59'),(208,'B2105661',216,'2024-09-25','07:00:28'),(209,'B2105661',216,'2024-10-02','07:00:59'),(210,'B2105661',216,'2024-10-09','07:00:59'),(211,'B2105661',216,'2024-10-16','07:00:29'),(212,'B2105661',216,'2024-10-23','07:00:59'),(213,'B2105661',216,'2024-10-30','07:00:59'),(214,'B2105661',216,'2024-11-06','07:00:30'),(215,'B2105661',216,'2024-11-13','07:00:59'),(216,'B2105661',216,'2024-11-20','07:00:59'),(217,'B2105661',216,'2024-11-27','07:00:31'),(218,'B2105661',216,'2024-12-04','07:00:59'),(219,'B2105661',216,'2024-12-11','07:00:59'),(220,'B2105661',216,'2024-12-18','07:00:32'),(221,'B2105661',217,'2024-08-07','13:00:53'),(222,'B2105661',217,'2024-08-14','13:00:26'),(223,'B2105661',217,'2024-08-21','13:00:59'),(224,'B2105661',217,'2024-08-28','13:00:59'),(225,'B2105661',217,'2024-09-04','13:00:27'),(226,'B2105661',217,'2024-09-11','13:00:59'),(227,'B2105661',217,'2024-09-18','13:00:59'),(228,'B2105661',217,'2024-09-25','13:00:28'),(229,'B2105661',217,'2024-10-02','13:00:59'),(230,'B2105661',217,'2024-10-09','13:00:59'),(231,'B2105661',217,'2024-10-16','13:00:29'),(232,'B2105661',217,'2024-10-23','13:00:59'),(233,'B2105661',217,'2024-10-30','13:00:59'),(234,'B2105661',217,'2024-11-06','13:00:30'),(235,'B2105661',217,'2024-11-13','13:00:59'),(236,'B2105661',217,'2024-11-20','13:00:59'),(237,'B2105661',217,'2024-11-27','13:00:31'),(238,'B2105661',217,'2024-12-04','13:00:59'),(239,'B2105661',217,'2024-12-11','13:00:59'),(240,'B2105661',217,'2024-12-18','13:00:32'),(241,'B2105661',218,'2024-08-08','13:00:53'),(242,'B2105661',218,'2024-08-15','13:00:26'),(243,'B2105661',218,'2024-08-22','13:00:59'),(244,'B2105661',218,'2024-08-29','13:00:59'),(245,'B2105661',218,'2024-09-05','13:00:27'),(246,'B2105661',218,'2024-09-12','13:00:59'),(247,'B2105661',218,'2024-09-19','13:00:59'),(248,'B2105661',218,'2024-09-26','13:00:28'),(249,'B2105661',218,'2024-10-03','13:00:59'),(250,'B2105661',218,'2024-10-10','13:00:59'),(251,'B2105661',218,'2024-10-17','13:00:29'),(252,'B2105661',218,'2024-10-24','13:00:59'),(253,'B2105661',218,'2024-10-31','13:00:59'),(254,'B2105661',218,'2024-11-07','13:00:30'),(255,'B2105661',218,'2024-11-14','13:00:59'),(256,'B2105661',218,'2024-11-21','13:00:59'),(257,'B2105661',218,'2024-11-28','13:00:31'),(258,'B2105661',218,'2024-12-05','13:00:59'),(259,'B2105661',218,'2024-12-12','13:00:59'),(260,'B2105661',218,'2024-12-19','13:00:32');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `cl_className` varchar(10) NOT NULL,
  `maj_Code` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`cl_className`),
  KEY `maj_Code` (`maj_Code`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`maj_Code`) REFERENCES `majors` (`maj_Code`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES ('DI21V7F1','7480201C'),('DI21V7F2','7480201C'),('DI21V7F3','7480201C'),('DI21V7F4','7480201C');
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classcourse`
--

DROP TABLE IF EXISTS `classcourse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classcourse` (
  `clCourse_ID` int(11) NOT NULL AUTO_INCREMENT,
  `clCourse_code` varchar(10) DEFAULT NULL,
  `clCourse_amount` int(11) NOT NULL,
  `cfa_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`clCourse_ID`),
  UNIQUE KEY `clCourse_code` (`clCourse_code`,`cfa_ID`),
  KEY `cfa_ID` (`cfa_ID`),
  CONSTRAINT `classcourse_ibfk_1` FOREIGN KEY (`cfa_ID`) REFERENCES `coursefollowacayear` (`cfa_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=229 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classcourse`
--

LOCK TABLES `classcourse` WRITE;
/*!40000 ALTER TABLE `classcourse` DISABLE KEYS */;
INSERT INTO `classcourse` VALUES (137,'M01',40,67),(138,'M01',40,68),(140,'M01',40,69),(141,'M01',40,70),(142,'M01',40,71),(143,'M01',40,72),(144,'M01',40,73),(145,'M01',40,74),(146,'M01',40,75),(147,'M01',40,76),(148,'M01',40,77),(150,'M01',40,78),(151,'M01',40,79),(153,'M01',40,80),(154,'M01',40,81),(155,'M01',40,82),(156,'M01',40,83),(157,'M01',40,84),(158,'M01',40,85),(159,'M01',40,86),(160,'M01',40,87),(161,'M01',40,88),(162,'M01',40,89),(163,'M01',40,90),(165,'M01',40,91),(166,'M01',40,92),(167,'M01',40,93),(168,'M01',40,94),(170,'M01',40,95),(171,'M01',40,96),(173,'M01',40,97),(174,'M01',40,98),(175,'M01',40,99),(176,'M01',40,100),(177,'M01',40,101),(178,'M01',40,102),(179,'M01',40,103),(180,'M01',40,104),(181,'M01',40,105),(182,'M01',40,106),(183,'M01',40,107),(184,'M01',40,108),(185,'M01',40,109),(186,'M01',40,110),(187,'M01',40,111),(188,'M01',40,112),(189,'M01',40,113),(190,'M01',40,114),(191,'M01',40,115),(213,'M01',40,116),(214,'M01',40,117),(215,'M01',40,118),(216,'M01',40,119),(217,'M01',40,120),(218,'M01',40,121),(219,'M01',40,122),(220,'M01',40,123),(221,'M01',40,124),(222,'M01',40,125),(223,'M01',40,126),(224,'M01',40,127),(227,'M01',40,128),(228,'M01',40,129);
/*!40000 ALTER TABLE `classcourse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classroom`
--

DROP TABLE IF EXISTS `classroom`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classroom` (
  `room_id` int(11) NOT NULL AUTO_INCREMENT,
  `room_name` varchar(255) NOT NULL,
  PRIMARY KEY (`room_id`),
  UNIQUE KEY `room_name` (`room_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classroom`
--

LOCK TABLES `classroom` WRITE;
/*!40000 ALTER TABLE `classroom` DISABLE KEYS */;
INSERT INTO `classroom` VALUES (1,'Phòng 201'),(2,'Phòng 202'),(3,'Phòng 203'),(4,'Phòng 204'),(5,'Phòng 205'),(6,'Phòng 206'),(7,'Phòng 207'),(8,'Phòng 208'),(9,'Phòng 209'),(10,'Phòng 210'),(11,'Phòng 211'),(12,'Phòng 212'),(13,'Phòng 213'),(14,'Phòng 214'),(15,'Phòng 215'),(16,'Phòng 216'),(17,'Phòng 217'),(18,'Phòng 218'),(19,'Phòng 219'),(20,'Phòng 220');
/*!40000 ALTER TABLE `classroom` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coursefollowacayear`
--

DROP TABLE IF EXISTS `coursefollowacayear`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coursefollowacayear` (
  `cfa_ID` int(11) NOT NULL AUTO_INCREMENT,
  `course_code` varchar(10) DEFAULT NULL,
  `ay_schoolYear` varchar(255) DEFAULT NULL,
  `se_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`cfa_ID`),
  KEY `course_code` (`course_code`),
  KEY `se_ID` (`se_ID`),
  KEY `ay_schoolYear` (`ay_schoolYear`),
  CONSTRAINT `coursefollowacayear_ibfk_1` FOREIGN KEY (`course_code`) REFERENCES `courses` (`course_code`),
  CONSTRAINT `coursefollowacayear_ibfk_2` FOREIGN KEY (`se_ID`) REFERENCES `semester` (`se_ID`),
  CONSTRAINT `coursefollowacayear_ibfk_3` FOREIGN KEY (`ay_schoolYear`) REFERENCES `years` (`ay_schoolYear`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coursefollowacayear`
--

LOCK TABLES `coursefollowacayear` WRITE;
/*!40000 ALTER TABLE `coursefollowacayear` DISABLE KEYS */;
INSERT INTO `coursefollowacayear` VALUES (67,'FL009H','2021-2022',1),(68,'FL008H','2021-2022',1),(69,'FL007H','2021-2022',1),(70,'FL001H','2021-2022',1),(71,'FL003H','2021-2022',1),(72,'FL005H','2021-2022',1),(73,'TC005','2021-2022',2),(74,'CT054H','2021-2022',2),(75,'CT051H','2021-2022',2),(76,'TN033H','2021-2022',2),(77,'TN034H','2021-2022',2),(78,'FL004H','2021-2022',2),(79,'FL006H','2021-2022',2),(80,'FL002H','2021-2022',2),(81,'CT056H','2021-2022',2),(82,'QP012','2021-2022',3),(83,'QP013','2021-2022',3),(84,'QP011','2021-2022',3),(85,'QP010','2021-2022',3),(86,'CT111H','2022-2023',1),(87,'CT103H','2022-2023',1),(88,'CT102H','2022-2023',1),(89,'CT057H','2022-2023',1),(90,'CT053H','2022-2023',1),(91,'CT052H','2022-2023',1),(92,'ML014','2022-2023',1),(93,'CT110H','2022-2023',2),(94,'CT107H','2022-2023',2),(95,'ML016','2022-2023',2),(96,'CT108H','2022-2023',2),(97,'CT109H','2022-2023',2),(98,'CT104H','2022-2023',2),(99,'XH014','2022-2023',3),(100,'ML018','2022-2023',3),(101,'KL001','2022-2023',3),(102,'CT206H','2023-2024',1),(103,'CT106H','2023-2024',1),(104,'CT101H','2023-2024',1),(105,'TC006','2023-2024',1),(106,'CT208H','2023-2024',1),(107,'CT203H','2023-2024',2),(108,'CT216H','2023-2024',2),(109,'CT214H','2023-2024',2),(110,'CT105H','2023-2024',2),(111,'ML019','2023-2024',2),(112,'CT112H','2023-2024',2),(113,'FL100H','2023-2024',3),(114,'ML021','2023-2024',3),(115,'TC020','2023-2024',3),(116,'CT201H','2024-2025',1),(117,'CT213H','2024-2025',1),(118,'CT501H','2024-2025',1),(119,'CT308H','2024-2025',1),(120,'CT209H','2024-2025',1),(121,'CT313H','2024-2025',1),(122,'CT301H','2024-2025',2),(123,'CT310H','2024-2025',2),(124,'CT312H','2024-2025',2),(125,'CT205H','2024-2025',2),(126,'CT202H','2024-2025',2),(127,'CT204H','2024-2025',2),(128,'CT215H','2024-2025',3),(129,'CT502H','2025-2026',1);
/*!40000 ALTER TABLE `coursefollowacayear` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `maj_Code` varchar(8) DEFAULT NULL,
  `course_ID` int(11) NOT NULL AUTO_INCREMENT,
  `course_code` varchar(10) DEFAULT NULL,
  `course_name` varchar(255) NOT NULL,
  `course_credits` int(11) NOT NULL,
  PRIMARY KEY (`course_ID`),
  UNIQUE KEY `course_code` (`course_code`),
  KEY `maj_Code` (`maj_Code`),
  CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`maj_Code`) REFERENCES `majors` (`maj_Code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=443 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('7480201C',380,'FL009H','Kỹ năng thuyết trình (*)',2),('7480201C',381,'FL008H','Ngữ âm thực hành (*)',2),('7480201C',382,'FL007H','Ngữ pháp ứng dụng (*)',3),('7480201C',383,'FL001H','Nghe và Nói 1 (*)',3),('7480201C',384,'FL003H','Đọc hiểu 1 (*)',2),('7480201C',385,'FL005H','Viết 1 (*)',2),('7480201C',386,'TC005','Bóng chuyền 1 (*)',1),('7480201C',387,'CT054H','Lập trình căn bản A',4),('7480201C',388,'CT051H','Vi - Tích phân',4),('7480201C',389,'TN033H','Tin học căn bản (*)',1),('7480201C',390,'TN034H','Thực hành Tin học căn bản (*)',2),('7480201C',391,'FL004H','Đọc hiểu 2 (*)',2),('7480201C',392,'FL006H','Viết 2 (*)',2),('7480201C',393,'FL002H','Nghe và Nói 2 (*)',2),('7480201C',394,'CT056H','Kỹ năng thuyết trình',1),('7480201C',395,'QP012','Giáo dục quốc phòng và An ninh 3 (*)',2),('7480201C',396,'QP013','Giáo dục quốc phòng và An ninh 4 (*)',2),('7480201C',397,'QP011','Giáo dục quốc phòng và An ninh 2 (*)',2),('7480201C',398,'QP010','Giáo dục quốc phòng và An ninh 1 (*)',2),('7480201C',399,'CT111H','Kỹ năng học đại học',3),('7480201C',400,'CT103H','Nền tảng công nghệ thông tin',3),('7480201C',401,'CT102H','Cấu trúc dữ liệu',4),('7480201C',402,'CT057H','Kỹ năng làm việc nhóm',1),('7480201C',403,'CT053H','Xác suất thống kê',3),('7480201C',404,'CT052H','Đại số tuyến tính và hình học',3),('7480201C',405,'ML014','Triết học Mác - Lênin',3),('7480201C',406,'CT110H','Cơ sở dữ liệu',3),('7480201C',407,'CT107H','Nhập môn công nghệ phần mềm',3),('7480201C',408,'ML016','Kinh tế chính trị Mác - Lênin',2),('7480201C',409,'CT108H','Lập trình hướng đối tượng',3),('7480201C',410,'CT109H','Phân tích và thiết kế thuật toán',3),('7480201C',411,'CT104H','Nguyên lý hệ điều hành',3),('7480201C',412,'XH014','Văn bản và lưu trữ học đại cương',2),('7480201C',413,'ML018','Chủ nghĩa xã hội khoa học',2),('7480201C',414,'KL001','Pháp luật đại cương',2),('7480201C',415,'CT206H','Nguyên lý hệ quản trị cơ sở dữ liệu',3),('7480201C',416,'CT106H','Mạng máy tính',3),('7480201C',417,'CT101H','Toán cho khoa học máy tính',4),('7480201C',418,'TC006','Bóng chuyền 2 (*)',1),('7480201C',419,'CT208H','Hệ quản trị cơ sở dữ liệu Oracle',3),('7480201C',420,'CT203H','Quản lý dự án phần mềm',3),('7480201C',421,'CT216H','Niên luận cơ sở',3),('7480201C',422,'CT214H','Lập trình Web',3),('7480201C',423,'CT105H','Quản trị hệ thống',3),('7480201C',424,'ML019','Lịch sử Đảng Cộng sản Việt Nam',2),('7480201C',425,'CT112H','Phân tích và thiết kế hệ thống',3),('7480201C',426,'FL100H','Thi đánh giá năng lực tiếng Anh (*)',2),('7480201C',427,'ML021','Tư tưởng Hồ Chí Minh',2),('7480201C',428,'TC020','Bóng chuyền 3 (*)',1),('7480201C',429,'CT201H','An ninh máy tính',3),('7480201C',430,'CT213H','Phát triển phần mềm mã nguồn mở',3),('7480201C',431,'CT501H','Niên luận chuyên ngành',3),('7480201C',432,'CT308H','Thương mại điện tử',3),('7480201C',433,'CT209H','Quản trị mạng trên MS Windows',3),('7480201C',434,'CT313H','Công nghệ và dịch vụ Web',3),('7480201C',435,'CT301H','An ninh mạng',3),('7480201C',436,'CT310H','Phát triển ứng dụng chuyên nghiệp với .NET',3),('7480201C',437,'CT312H','Lập trình cho các thiết bị di động',3),('7480201C',438,'CT205H','Nguyên lý máy học',3),('7480201C',439,'CT202H','Tương tác người máy',3),('7480201C',440,'CT204H','Điện toán đám mây',3),('7480201C',441,'CT215H','Thực tập thực tế',2),('7480201C',442,'CT502H','Luận văn tốt nghiệp',10);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dayofweak`
--

DROP TABLE IF EXISTS `dayofweak`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dayofweak` (
  `DOW_ID` int(11) NOT NULL AUTO_INCREMENT,
  `DOW_day` varchar(50) NOT NULL,
  PRIMARY KEY (`DOW_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dayofweak`
--

LOCK TABLES `dayofweak` WRITE;
/*!40000 ALTER TABLE `dayofweak` DISABLE KEYS */;
INSERT INTO `dayofweak` VALUES (1,'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday'),(6,'Saturday'),(7,'Sunday');
/*!40000 ALTER TABLE `dayofweak` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-09-20 07:10:13.148361'),(2,'auth','0001_initial','2024-09-20 07:10:13.587146'),(3,'admin','0001_initial','2024-09-20 07:10:13.687463'),(4,'admin','0002_logentry_remove_auto_add','2024-09-20 07:10:13.695389'),(5,'admin','0003_logentry_add_action_flag_choices','2024-09-20 07:10:13.704998'),(6,'contenttypes','0002_remove_content_type_name','2024-09-20 07:10:13.768641'),(7,'auth','0002_alter_permission_name_max_length','2024-09-20 07:10:13.823156'),(8,'auth','0003_alter_user_email_max_length','2024-09-20 07:10:13.838158'),(9,'auth','0004_alter_user_username_opts','2024-09-20 07:10:13.852244'),(10,'auth','0005_alter_user_last_login_null','2024-09-20 07:10:13.899253'),(11,'auth','0006_require_contenttypes_0002','2024-09-20 07:10:13.903809'),(12,'auth','0007_alter_validators_add_error_messages','2024-09-20 07:10:13.911808'),(13,'auth','0008_alter_user_username_max_length','2024-09-20 07:10:13.930810'),(14,'auth','0009_alter_user_last_name_max_length','2024-09-20 07:10:13.950812'),(15,'auth','0010_alter_group_name_max_length','2024-09-20 07:10:13.967811'),(16,'auth','0011_update_proxy_permissions','2024-09-20 07:10:13.978820'),(17,'auth','0012_alter_user_first_name_max_length','2024-09-20 07:10:13.994817'),(18,'sessions','0001_initial','2024-09-20 07:10:14.019351');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('21tovignttksr253moruwkuo4cy47koj','.eJyNjj8LwkAMxb9KuVkhd-jSTbro4OYolJIGrnB_ILkbivjdvV51KCi4hOT9XpL3UFmIw-BJteoEAEbtqtRzdIt2CZI4Y4oshWDmLmYW6jGOC-5uBvR5Jei27Ap6s_L5EpowBdv4ewYgPTepNmOwq1vQRjdImrCYDZjDvpTjm5EnScSq1WWuZ_-6-iPzl8DPFwTQWFU:1sx5bF:ugnWefwJqx8qzG6J9HnfxOPmyfP_2MmgPgx8warckjk','2024-10-19 14:17:37.263827'),('2oeldu5fyvkeymcc34rkjqiaqmmx4usq','.eJxVi8EKwjAMQH9l9OwgKwriTXbRw8CDR2GUNlBhSyFJD0P8d9vJEC9JeO_lZbIgk5vRnMwZAKzZrWjkNFV2JVHOXhNLMT5znzILjtsLNfSk2MyPDIDd0uh6BIq1_qY-hZr2dwvdpeKp_xMDdIUKOvZxXMoqzILdt2UcfkZwRlGstvbBKW4hHFtYS3WapdAboyCpeX8AwcJGHw:1svsbR:v3yTl2by_wBt7_TZd0ZCJnHMmf-7zEjXFPepXEWO1VY','2024-10-16 06:12:49.035286'),('5vf985658vrzm1s49otyg10hyk4ilgpw','eyJ1c2VybmFtZSI6IkIyMTA1NjYxIiwidXNlcl9yb2xlIjoiU3R1ZGVudHMifQ:1sut6S:zUFhSZpwuS_cu4s80tyqY4mVJTWKEM2RnGZ2f3Dhhi0','2024-10-13 12:32:44.403311'),('an0jfiyu90km2zbudvsse5xiqb50dd8o','.eJyFjbEKAjEMhl_l6KyQFl3c5BYd3ByF48gFetCmkLSDiO9ur6fDTS4h_N-fLy9TlITHSOZkzgDgzK5Fg6SwZFfWLAVzEq0Ei_SpiNKAaVpwf3dgLyvBsGU3sJuT3xfueGbfxUcBIPvsclsm9mtb0acwap6xlh24w76O45dRJM0klTR3E__3vj8sZErY:1syUy7:Lp0xfddyWVRbEOwZTXYmc2Qt9MIOuKiMraVLWKVF_78','2024-10-23 11:35:03.532768'),('aub32ob2342j8lozvizoktbb97j9xq4t','.eJx1jj0LwkAMhv9KyayQO3TpJl10cHMUSkkDV2jvILkbivjfvX6IVHTJ1_MmeR-QlMU3A0MJJ0S0sJtHtYR-ml28RkkUg2gmlKQKSZRrCu2Eq5tFc14I9Vt2RbNZeX_xhe-8K4Z7QmQzFnEuWu8WtZILfaOxoyy2aA_7HI4r44E1skBpcv_HyU8byo2Qq8ecvs6u5HMaDDxf0F9ZFg:1swlB7:zrbePUu94g6qiNPEN2egGbEC7O0eGGua_Jng_y4YtRs','2024-10-18 16:29:17.169837'),('ems3ggdzg85sdambj84w6lkr3sct1h8n','.eJyFj7EKwyAQhl8l3NyCSpMhW5ulS6d2LATRAwOJgqdDKH33GiOUlJYu5_l_8vH7gEjorZwQWjgJzuqm4bDLae_duMTXEDXaQClW0XcuesJeOb2w7iYYP29IkR1tZQdrqukeGUM-VyEv2pr1tRq3pgvjKyBl3CgpDCqlgonDPo26MJyQAnpoebr_aPJVTCi9Mv2cjg9tIW815CLZ8f8vzxfSEmYx:1sySsm:efIdTYtNUwYl31Fo74UsN_UYFdMFjcx-qfhb5whLnVI','2024-10-23 09:21:24.784454'),('hfjneeayv390pzk6iw0yxwn8us9fvplw','.eJx1jj8LAjEMxb9K6ayQFl3c5BYd3ByF48gFetA_kLTDIX53ez0dDnQJ4f1e8t5TFyGOQyB90mcAsHrXpJ6TX7RrlMwFc2KpBAt3qbBQj2lccHe3YC4rQb9lNzCbk29KVHGKToVHASAzq9yWMbrVLeiSHyRPWM0W7GFfx_HDKJBk4kra7z9dfhR5vQH91UrM:1syZei:91_mN2rCJcD4rEmFt_C41YJCarurutx1A2P6ekDVMyM','2024-10-23 16:35:20.892214'),('mavybspe8wyb6zkzwx9jkrvmh87dusjj','.eJwdyUEKgEAIBdC7uO4Es-skIiQ1kApfhxbR3WvavnfTSIWLKTWSzbrT8hMjzmnrtJ4FqUB-qUCATTNlV84jLqdWGPq8GvYcHA:1svw9n:X154ZT-d5DZiDF5r4hnZQ-SGKq6Uh8DKRGZ24195oC8','2024-10-16 10:00:31.952904'),('mvdj8uic90htbr7lg5z7b58hjjo7p076','.eJxVjLsKwzAQBH_FqE7gTsQu3CVu0qRKyoAx0oEM0gl0UhFC_j3yo3GzLDPLflURSjwFUr26aYS261CdVjqm6Bf8zMUSZ6nYlDTEkoRGE-3ihpcGvB_Mfnblhmd2TXgXAMJPk9di2W1r449PD8BNiHHRT5JnU6kGfTnXaHdHgSRTUj3-_iSNPBU:1swhaH:6BmT68xaBiHL67SyDQRPhcuhNe4L3A98fkor9EVlpSU','2024-10-18 12:39:01.955632'),('qacs5m8hnezbiua03exhi17sssxrycoo','eyJ1c2VybmFtZSI6IjEiLCJ1c2VyX3JvbGUiOiJBZG1pbmlzdHJhdG9ycyJ9:1suUL7:3pMtsTCj3l5zyM4cHHL6jqW6grEJNrwM7Q-QTREFKTw','2024-10-12 10:06:13.741772'),('qb34zduvbac80mthz8ryj96ms45lcrwb','.eJxVzT0LwjAQgOG_EjIr5PolOJrFxUnBpVDa69kIaQL5cBH_u0nbpcvBPS_cfXn05Ew_Ez_zSwGibhrgh0U7Z3Xme4gjmeATY3TSRuepQzvmJh8llNdd2Y7JNgrxqszEzKTaCIQn9slGgo3LPqDKAkQ1e9KwHkG9f3ATsAaPyurehzcmLURRHdOot0Yz-UAuFeC_P2NOQ50:1svw2n:aB3KzYG1Dhopmbd-maCqyR2FGyRl_6c4stFKHslS4fY','2024-10-16 09:53:17.749885'),('qfyu5rawhl2032jo29rrwki0678f44r6','.eJyrViotTi3KS8xNVbJScjQwMDBS0gELxRfl54DEPPOKS4pKk0vyi4qBMsmlRc75pUXFqfEwLXkKeZl5GQq5MaUGBqmGlQolYEZKXoZSLQCSnR7i:1svsaq:D8VwauZ2DZz7WKvDP01N1jlqnkYsPb4kMk_kaHlWSFw','2024-10-16 06:12:12.554477'),('quc5npk45so8god9g2h2qscvzwbu7xib','.eJxVjbEKAjEMhl-ldFZoi3eDm3ZxuUlHoRxtoMI1haYdDvHdbU5BXJLwfX_4n7IRFJwTyKM8G62GcdRyt1FX8sL4WlsArNSxb8XmVgjc9-WEAh8YRbo3pUCvom5HwMjpT9TnwFF7M0pfGC_2T0yKGwnm4qNb--rMKHPY9zH8DEECqsBWy9cbkEU6fw:1svvSZ:JFd-UiE7wZHylg3u1P9ijWQc3WrdJFzII0JEm1yWPUM','2024-10-16 09:15:51.834714'),('rfv0lhmzrzvvjq74ad1ss4413m88783k','.eJxVjLsKwzAQBH_FqE7gTsQu3CVu0qRKyoAx0oEM0gl0UhFC_j3yo3GzLDPLflURSjwFUr26aYS261CdVjqm6Bf8zMUSZ6nYlDTEkoRGE-3ihpcGvB_Mfnblhmd2TXgXAMJPk9di2W1r449PD8BNiHHRT5JnU6kGfTnXaHdHgSRTUj3-_iSNPBU:1swhZL:WB-Sspp8DaP1VfbIqWXxmu6VHtsZEARThRWzv_SW0wY','2024-10-18 12:38:03.993797'),('sudtxo1os3ss1s5nk8inxjge3sr8qthc','.eJyNjkELwjAMhf_K6FkhK3rxJrvowduOwhhZoIOuhaQ9DPG_23XzUFHwkoT3JS_voaIQu34idVJnANBql6WOvV20q5PAEYNnSQQjNz6yUId-WHDTaqgvK0FbshvUxcn7i6vc6Ew13SMA1XMV8jA4s24LGm97CSOmZQ36sE_luDGaSAJxItk7G__l-yP118hCPaPp5tQ-ImykiPF8AZAlZyc:1sx5ZG:WgsPbp5qjNtrQn_Gb4w4ne0xKmLILykrTD1tKZZuz7c','2024-10-19 14:15:34.962424'),('tvg4f8vrt5zs92ohczien8etzjj4uycp','.eJx1jD0LwkAMhv9KyayQO3TpJl10cHMUSkkDV2jvILkbivjfvX6IVHTJx_skzwOSsvhmYCjhhIgWdnNUS-in7OI1SqIYRDOhJFVIoly_X3zhO--K4Z4Q2YxFnIfWu801hXa6rm4WzXkh1G_ZFc0ClFzoG40d5dSiPexzOa6MB9bIAqXJ-x_3T7FyI-TqMbcv7Uo-ajDwfAH0-1kW:1svsMO:MYMyZl3D9amqBzqDeBglpbfjlOxLV3b8-o-LXvTYWKU','2024-10-16 05:57:16.084643'),('udd0cvk2fbwef8twejvkg33ru37gqp6m','.eJyrViotTi3KS8xNVbJScjIyNDA1MzNU0gGLxhfl54CEg0tKU1LzSoqBwsmlRc75pUXFqfHJ-SkgOecQIwNDDxQZqGGOeQp5mXkZCrkxpQYGqYaVCiVgRkpeBkR1cg6qSb4Ghkq1APnlLmU:1suvg9:FoKC7rEMaaUflDD55jXHqLcTC50PX4v2izTNJnsB7Ks','2024-10-13 15:17:45.295192'),('uyhz3tdtku7x22raumikzbmqm8ygv6hy','.eJyFjTELwjAQhf9KyKxwCbaDm3ZxcdJRKCU5SCG5QC4ZRPzvpmmXTi7H4_se7z6yMCaaAsqzvGoFXd8reWh0TNEv-JGLRcpcsSlpiCUxjibaxQ1PDeq2M9vYhQTN5ER4FQBUb5FbsOTWtvH7pTuoVbBx0U-cZ1OpBn061tNtDgNyxlRNa7eF_w-_P6k0SiY:1syUJL:5dv_G7fHJC1itjD_ahCPjvp8ZNd08jc5HY8bpOdqdZg','2024-10-23 10:52:55.265318'),('vbnnc1xj3rzfzebpzen59iw1619mi3sq','.eJxVjTEPwiAQhf8KYdYEiO3QTbu46KKjSUPgIk3okQA3NMb_LqV16HJ597279z6cEkTUE_COX5QUTdtKfqh0iMEv-JHJAuZUsKHYB4oJBhPs4vVPJeR152xhZ2Q4omPTi4QAObNchUW3Xhu_T7oJuRrJuOB1yqMpVAl1OpbRbB5MkDJE3smy1_-t7j7WeI3M04skaIvMOJr_FN9ViVL__QECdk-7:1swk23:oKM8wAeZ6sISW9Jp2wfz-arhAIZILOjDn8jshG0AGqQ','2024-10-18 15:15:51.634057'),('vgxduy5idw40ss9dx588mgclrelc7u48','.eJw1y0sKg0AQBNCrDL2O0A4GJLvgyjsEZNAGhdgT-rMQ8e6OQnbFq6odXEk4rQQveCNihMdNg-TvZT2riY-WRUszunTZRWn4XzjwwnNYP45I9RbsDhPPZT0luzYRY1NhW-GzmFoy16K2_aiG4wSz0iji:1svsKI:6pBKf2vY1Qa0XkxEL1Q7E-dmq_UDjLlFyQP4LUshutw','2024-10-16 05:55:06.373999'),('wwogwx8irn6ozsftz94mt92k353vey5t','.eJyFjTELwjAQhf9KyKxwCbaDm3ZxcdJRKCU5SCG5QC4ZRPzvpmmXTi7H4_se7z6yMCaaAsqzvGoFXd8reWh0TNEv-JGLRcpcsSlpiCUxjibaxQ1PDeq2M9vYhQTN5ER4FQBUb5FbsOTWtvH7pTuoVbBx0U-cZ1OpBn061tNtDgNyxlRNa7eF_w-_P6k0SiY:1syT8G:OESGesBlwgNxhVMymgW3hBivzPbxw7KNg7NyYDc6FDY','2024-10-23 09:37:24.890366'),('xob2j4ife1tdfus1dxju385ovpm6g7ya','.eJyrViotTi3KS8xNVbJScjIyNDA1MzNU0gGLxhfl54CEg0tKU1LzSoqBwsmlRc75pUXFqfHJ-SkgOecQIwNDD4hMcg5WuVoAUYof0w:1srY2C:_gADqfegt6NEAORe6IvWS8GM9S8-Igou418xolFDcdw','2024-10-04 07:26:32.951513'),('zf35cbvk0p7wa9sfpb1xtdjf6y9046ze','.eJxVjTEKwzAMRa8SPDcgmwZKtpKlHbp1LATjCBxI7CLJQyi9e-00GbII8d7_0kclRgp2RtWqKwAYdVpRT3Eq7B5YKDmJxNm4RF1MxNjvlVCFMfhqfiUA1Esl6zIEn9ODlZIxYM41XGpoMmOxkjhTWd6oDyddHEq8exrQt79x09E9YKuw83GyLKPbH-TRbA5nZEFSrf7-AIUjRsc:1svrx0:SrKzmTR0be3qF3htVkdRCAZ6k7x13A5ua8RPjnw7e68','2024-10-16 05:31:02.637735'),('zip19i043ibwzkdq7hiw2pilbh7lsfhe','.eJxVi7EKAjEMQH-ldFZIy7m4SRcd3G48KEcvUOGaQtIOh_jvticiLkl47-WpqyDTnFCf9QUArD7syHNeO7uRFK6hZJZmQmWXKwv67wspelBUaaoAaDZV9mOh2OtPGvLSUzdaMNeOV_cn7mAaFZw5RL-11ZgFOxzbOP2MYEIp2K3Rrzf9EDsx:1sv8Ne:AVFDapYTVtwUDnFJNa-pG1LQi8yJE1BO7gwkTw6r6PY','2024-10-14 04:51:30.645452');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emotion`
--

DROP TABLE IF EXISTS `emotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emotion` (
  `emo_ID` int(11) NOT NULL AUTO_INCREMENT,
  `emo_fromCourse_ID` int(11) DEFAULT NULL,
  `emo_name` varchar(50) DEFAULT NULL,
  `emo_session_date` date DEFAULT NULL,
  `emo_time_status` time DEFAULT NULL,
  PRIMARY KEY (`emo_ID`),
  KEY `emo_fromCourse_ID` (`emo_fromCourse_ID`),
  CONSTRAINT `emotion_ibfk_1` FOREIGN KEY (`emo_fromCourse_ID`) REFERENCES `studying` (`clCourse_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emotion`
--

LOCK TABLES `emotion` WRITE;
/*!40000 ALTER TABLE `emotion` DISABLE KEYS */;
INSERT INTO `emotion` VALUES (1,213,'fear','2024-09-28','17:46:05'),(2,213,'angry','2024-09-28','17:46:17'),(3,213,'neutral','2024-09-28','17:46:25'),(4,213,'neutral','2024-09-28','17:46:33'),(5,213,'sad','2024-09-28','17:46:40'),(6,213,'neutral','2024-09-28','17:46:48'),(7,213,'neutral','2024-09-28','17:46:56'),(8,213,'neutral','2024-09-28','17:47:04'),(9,213,'neutral','2024-09-28','17:47:12'),(10,213,'neutral','2024-09-28','17:47:20'),(11,213,'neutral','2024-09-28','17:47:27'),(12,213,'neutral','2024-09-28','17:47:35'),(13,213,'neutral','2024-09-28','17:47:44'),(14,213,'neutral','2024-09-28','17:47:51'),(15,213,'neutral','2024-09-28','17:47:59'),(16,213,'neutral','2024-09-28','17:48:08'),(17,213,'surprise','2024-09-28','17:48:21'),(18,213,'neutral','2024-09-28','17:48:22'),(19,213,'neutral','2024-09-28','17:48:36'),(20,213,'neutral','2024-09-28','17:48:36'),(21,213,'sad','2024-10-01','20:10:03'),(22,213,'neutral','2024-10-01','20:10:03'),(23,213,'neutral','2024-10-01','20:10:17'),(24,213,'sad','2024-10-01','20:10:30'),(25,213,'sad','2024-10-01','20:10:31'),(26,213,'sad','2024-10-01','20:10:47'),(27,213,'sad','2024-10-01','20:10:47'),(28,213,'sad','2024-10-01','20:10:48'),(29,213,'neutral','2024-10-01','20:11:07'),(30,213,'sad','2024-10-01','20:11:07'),(31,213,'neutral','2024-10-01','20:11:24'),(32,213,'sad','2024-10-01','20:11:24'),(33,213,'fear','2024-10-01','20:11:25'),(34,213,'sad','2024-10-01','20:11:44'),(35,213,'sad','2024-10-01','20:11:45'),(36,213,'sad','2024-10-01','20:11:45'),(37,213,'sad','2024-10-01','20:12:07'),(38,213,'neutral','2024-10-01','20:12:07'),(39,213,'sad','2024-10-01','20:12:07'),(40,213,'sad','2024-10-01','20:12:29'),(41,213,'sad','2024-10-01','20:12:30'),(42,213,'sad','2024-10-01','20:12:30'),(43,213,'neutral','2024-10-01','20:12:51'),(44,213,'sad','2024-10-01','20:12:51'),(45,213,'sad','2024-10-01','20:12:52'),(46,213,'happy','2024-10-01','20:13:15'),(47,213,'sad','2024-10-01','20:13:15'),(48,213,'sad','2024-10-01','20:13:16'),(49,213,'neutral','2024-10-01','20:13:42'),(50,213,'sad','2024-10-01','20:13:42'),(51,213,'fear','2024-10-01','20:13:43'),(52,213,'sad','2024-10-01','20:14:07'),(53,213,'sad','2024-10-01','20:14:07'),(54,213,'fear','2024-10-01','20:14:07'),(55,213,'sad','2024-10-01','20:14:31'),(56,213,'sad','2024-10-01','20:14:31'),(57,213,'sad','2024-10-01','20:14:49'),(58,213,'happy','2024-10-01','20:14:50'),(59,213,'sad','2024-10-01','20:14:50'),(60,213,'angry','2024-10-01','20:15:13'),(61,213,'neutral','2024-10-01','20:15:13'),(62,213,'sad','2024-10-01','20:15:29'),(63,213,'angry','2024-10-01','20:15:38'),(64,213,'neutral','2024-10-01','20:15:48'),(65,213,'sad','2024-10-01','20:15:57'),(66,213,'sad','2024-10-01','20:16:06'),(67,213,'sad','2024-10-01','20:16:15'),(68,213,'neutral','2024-10-01','20:16:25'),(69,213,'happy','2024-10-01','20:16:33'),(70,213,'fear','2024-10-01','20:16:34'),(71,213,'neutral','2024-10-01','20:16:48'),(72,213,'neutral','2024-10-01','20:16:49'),(73,213,'happy','2024-10-01','20:17:03'),(74,213,'neutral','2024-10-01','20:17:04'),(75,213,'neutral','2024-10-01','20:17:17'),(76,213,'sad','2024-10-01','20:17:27'),(77,213,'fear','2024-10-01','20:17:27'),(78,213,'fear','2024-10-01','20:17:42'),(79,213,'fear','2024-10-01','20:17:42'),(80,213,'fear','2024-10-01','20:17:55'),(81,213,'neutral','2024-10-01','20:17:56'),(82,213,'surprise','2024-10-01','20:18:10'),(83,213,'fear','2024-10-01','20:18:10'),(84,213,'happy','2024-10-01','20:18:24'),(85,213,'fear','2024-10-01','20:18:24'),(86,213,'neutral','2024-10-01','20:18:39'),(87,213,'fear','2024-10-01','20:18:40'),(88,213,'neutral','2024-10-01','20:18:54'),(89,213,'neutral','2024-10-01','20:18:55'),(90,213,'sad','2024-10-01','20:19:14'),(91,213,'sad','2024-10-01','20:19:14'),(92,213,'sad','2024-10-01','20:19:32'),(93,213,'sad','2024-10-01','20:19:32'),(94,213,'sad','2024-10-01','20:19:46'),(95,213,'neutral','2024-10-01','20:19:46');
/*!40000 ALTER TABLE `emotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `ins_ID` int(11) NOT NULL AUTO_INCREMENT,
  `ins_instructorCode` varchar(8) NOT NULL,
  `ins_name` varchar(255) NOT NULL,
  `ins_academicRank` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ins_ID`),
  UNIQUE KEY `ins_instructorCode` (`ins_instructorCode`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES (1,'A0001','Pham Nguyen Khang','PhD'),(2,'A0002','Lam Nhut Khang','PhD'),(3,'A0003','Tran Cong An','PhD'),(4,'A0004','Do Thanh Nghi','PhD'),(5,'A0005','Pham The Phi','PhD'),(6,'A0006','Truong Minh Thai','PhD'),(7,'A0007','Thai Minh Tuan','PhD'),(8,'A0008','Pham Thi Ngoc Diem','PhD');
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `majors`
--

DROP TABLE IF EXISTS `majors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `majors` (
  `maj_Code` varchar(8) NOT NULL,
  `maj_name` varchar(255) NOT NULL,
  PRIMARY KEY (`maj_Code`),
  UNIQUE KEY `maj_Code` (`maj_Code`),
  UNIQUE KEY `maj_name` (`maj_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `majors`
--

LOCK TABLES `majors` WRITE;
/*!40000 ALTER TABLE `majors` DISABLE KEYS */;
INSERT INTO `majors` VALUES ('7480201C','Công Nghệ Thông Tin - CLC');
/*!40000 ALTER TABLE `majors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_ID` int(11) NOT NULL,
  `role_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Students'),(2,'Instructors'),(3,'Administrators');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `se_ID` int(11) NOT NULL,
  `se_semesterName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`se_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'Học Kỳ 1'),(2,'Học Kỳ 2'),(3,'Học Kỳ Hè');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `st_ID` int(11) NOT NULL AUTO_INCREMENT,
  `st_code` varchar(8) NOT NULL,
  `st_fullName` varchar(255) NOT NULL,
  `st_birthDay` date DEFAULT NULL,
  `st_phone` char(10) DEFAULT NULL,
  `st_email` varchar(255) DEFAULT NULL,
  `cl_className` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`st_ID`),
  UNIQUE KEY `st_code` (`st_code`),
  KEY `cl_className` (`cl_className`),
  CONSTRAINT `students_ibfk_1` FOREIGN KEY (`cl_className`) REFERENCES `class` (`cl_className`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'B2111952','Lê Xuân Thành',NULL,NULL,'thanhb2111952@student.ctu.edu.vn','DI21V7F1'),(2,'B2105679','Phan Thị Hồng Nguyên',NULL,NULL,'nguyenb2105679@student.ctu.edu.vn','DI21V7F1'),(3,'B2111995','Trần Trung Nguyễn',NULL,NULL,'nguyenb2111995@student.ctu.edu.vn','DI21V7F1'),(4,'B2111930','Lý Phương Khải',NULL,NULL,'khaib2111930@student.ctu.edu.vn','DI21V7F1'),(5,'B2112000','Nguyễn Duy Diễm Phụng',NULL,NULL,'phungb2112000@student.ctu.edu.vn','DI21V7F1'),(6,'B2111972','Nguyễn Trần Quang Bình',NULL,NULL,'binhb2111972@student.ctu.edu.vn','DI21V7F1'),(7,'B2111982','Kiều Văn Hoá',NULL,NULL,'hoab2111982@student.ctu.edu.vn','DI21V7F1'),(8,'B2111963','Hồ Kim Trọng',NULL,NULL,'trongb2111963@student.ctu.edu.vn','DI21V7F1'),(9,'B2111946','Trần Minh Quang',NULL,NULL,'quangb2111946@student.ctu.edu.vn','DI21V7F1'),(10,'B2111949','Ngô Thụy Thanh Tâm',NULL,NULL,'tamb2111949@student.ctu.edu.vn','DI21V7F1'),(11,'B2111922','Nguyễn Trường Dũng Em',NULL,NULL,'emb2111922@student.ctu.edu.vn','DI21V7F1'),(12,'B2105709','Khúc Bảo Minh',NULL,NULL,'minhb2105709@student.ctu.edu.vn','DI21V7F1'),(13,'B2105695','Lê Huy Anh',NULL,NULL,'anhb2105695@student.ctu.edu.vn','DI21V7F1'),(14,'B2111978','Kiều Hoàng Giang',NULL,NULL,'giangb2111978@student.ctu.edu.vn','DI21V7F1'),(15,'B2111975','Đỗ Thành Đạt',NULL,NULL,'datb2111975@student.ctu.edu.vn','DI21V7F1'),(16,'B2111935','Ngô Thành Lộc',NULL,NULL,'locb2111935@student.ctu.edu.vn','DI21V7F1'),(17,'B2111918','Dương Quốc Duy',NULL,NULL,'duyb2111918@student.ctu.edu.vn','DI21V7F1'),(18,'B2112004','Lê Thanh Tâm',NULL,NULL,'tamb2112004@student.ctu.edu.vn','DI21V7F1'),(19,'B2105661','Cao Tiến Anh','0000-00-00','0123456789','anhb2105661@student.ctu.edu.vn','DI21V7F1'),(20,'B2112010','Nguyễn Phú Thịnh',NULL,NULL,'thinhb2112010@student.ctu.edu.vn','DI21V7F1'),(21,'B2105684','Lê Anh Quân',NULL,NULL,'quanb2105684@student.ctu.edu.vn','DI21V7F1'),(22,'B2111955','Châu Đình Thông',NULL,NULL,'thongb2111955@student.ctu.edu.vn','DI21V7F1'),(23,'B2110011','Nguyễn Nhật Hào',NULL,NULL,'haob2110011@student.ctu.edu.vn','DI21V7F1'),(24,'B2111879','Đặng Thành Đạt',NULL,NULL,'datb2111879@student.ctu.edu.vn','DI21V7F1'),(25,'B2111992','Ngô Thanh Nam',NULL,NULL,'namb2111992@student.ctu.edu.vn','DI21V7F1'),(26,'B2112014','Nguyễn Phạm Anh Thư',NULL,NULL,'thub2112014@student.ctu.edu.vn','DI21V7F1'),(27,'B2105723','Danh Tấn Tới',NULL,NULL,'toib2105723@student.ctu.edu.vn','DI21V7F1'),(28,'B2111985','Trần Nguyễn Xuân Khánh',NULL,NULL,'khanhb2111985@student.ctu.edu.vn','DI21V7F1'),(29,'B2111988','Lê Cát Lam',NULL,NULL,'lamb2111988@student.ctu.edu.vn','DI21V7F1'),(30,'B2112021','Hà Nhựt Tuấn',NULL,NULL,'tuanb2112021@student.ctu.edu.vn','DI21V7F1'),(31,'B2105667','Lê Trung Huy',NULL,NULL,'huyb2105667@student.ctu.edu.vn','DI21V7F1'),(32,'B2111939','Nguyễn Yến Ngọc',NULL,NULL,'ngocb2111939@student.ctu.edu.vn','DI21V7F1'),(33,'B2111943','Lê Trần Đại Phát',NULL,NULL,'phatb2111943@student.ctu.edu.vn','DI21V7F1'),(34,'B2111959','Nguyễn Thị Hoài Thương',NULL,NULL,'thuongb2111959@student.ctu.edu.vn','DI21V7F1'),(35,'B2105662','Trần Duy Bảo Anh',NULL,NULL,'anhb2105662@student.ctu.edu.vn','DI21V7F2'),(36,'B2105668','Trương Gia Huy',NULL,NULL,'huyb2105668@student.ctu.edu.vn','DI21V7F2'),(37,'B2105681','Lê Tú Như',NULL,NULL,'nhub2105681@student.ctu.edu.vn','DI21V7F2'),(38,'B2105686','Kim Duy Thành',NULL,NULL,'thanhb2105686@student.ctu.edu.vn','DI21V7F2'),(39,'B2105696','Nguyễn Thanh Bình',NULL,NULL,'binhb2105696@student.ctu.edu.vn','DI21V7F2'),(40,'B2105727','Nguyễn Quang Vinh',NULL,NULL,'vinhb2105727@student.ctu.edu.vn','DI21V7F2'),(41,'B2110058','Hồ Chí Thanh',NULL,NULL,'thanhb2110058@student.ctu.edu.vn','DI21V7F2'),(42,'B2111885','Hà Quốc Huy',NULL,NULL,'huyb2111885@student.ctu.edu.vn','DI21V7F2'),(43,'B2111915','Nguyễn Hoàng Gia Bảo',NULL,NULL,'baob2111915@student.ctu.edu.vn','DI21V7F2'),(44,'B2111919','Hồ Đức Dũng',NULL,NULL,'dungb2111919@student.ctu.edu.vn','DI21V7F2'),(45,'B2111923','Lê Tào Quốc Hải',NULL,NULL,'haib2111923@student.ctu.edu.vn','DI21V7F2'),(46,'B2111927','Cao Minh Nhật Huy',NULL,NULL,'huyb2111927@student.ctu.edu.vn','DI21V7F2'),(47,'B2111936','Nguyễn Phước Minh',NULL,NULL,'minhb2111936@student.ctu.edu.vn','DI21V7F2'),(48,'B2111940','Trần Thị Hồng Nhan',NULL,NULL,'nhanb2111940@student.ctu.edu.vn','DI21V7F2'),(49,'B2111944','Phạm Hoàng Phúc',NULL,NULL,'phucb2111944@student.ctu.edu.vn','DI21V7F2'),(50,'B2111947','Trịnh Thanh Sang',NULL,NULL,'sangb2111947@student.ctu.edu.vn','DI21V7F2'),(51,'B2111950','Đinh Hồ Thanh Tân',NULL,NULL,'tanb2111950@student.ctu.edu.vn','DI21V7F2'),(52,'B2111953','Nguyễn Dương Ngọc Thiện',NULL,NULL,'thienb2111953@student.ctu.edu.vn','DI21V7F2'),(53,'B2111956','Lâm Yến Thu',NULL,NULL,'thub2111956@student.ctu.edu.vn','DI21V7F2'),(54,'B2111960','Lê Huy Toàn',NULL,NULL,'toanb2111960@student.ctu.edu.vn','DI21V7F2'),(55,'B2111964','Bùi Ngọc Trúc',NULL,NULL,'trucb2111964@student.ctu.edu.vn','DI21V7F2'),(56,'B2111967','Lưu Hoài Vũ',NULL,NULL,'vub2111967@student.ctu.edu.vn','DI21V7F2'),(57,'B2111970','Nguyễn Thiên Ân',NULL,NULL,'anb2111970@student.ctu.edu.vn','DI21V7F2'),(58,'B2111973','Trần Thị Cẩm Diền',NULL,NULL,'dienb2111973@student.ctu.edu.vn','DI21V7F2'),(59,'B2111976','Hoàng Tiến Đạt',NULL,NULL,'datb2111976@student.ctu.edu.vn','DI21V7F2'),(60,'B2111980','Huỳnh Ngọc Hậu',NULL,NULL,'haub2111980@student.ctu.edu.vn','DI21V7F2'),(61,'B2111983','Đặng Gia Huy',NULL,NULL,'huyb2111983@student.ctu.edu.vn','DI21V7F2'),(62,'B2111986','Nguyễn Gia Khiêm',NULL,NULL,'khiemb2111986@student.ctu.edu.vn','DI21V7F2'),(63,'B2111989','Đào Thị Khánh Linh','0000-00-00','0123455788','linhb2111989@student.ctu.edu.vn','DI21V7F2'),(64,'B2111993','Nguyễn Thị Kim Ngân',NULL,NULL,'nganb2111993@student.ctu.edu.vn','DI21V7F2'),(65,'B2111996','La Hoàng Nhân',NULL,NULL,'nhanb2111996@student.ctu.edu.vn','DI21V7F2'),(66,'B2112001','Phạm Nhật Quang',NULL,NULL,'quangb2112001@student.ctu.edu.vn','DI21V7F2'),(67,'B2112005','Nguyễn Nhựt Tâm',NULL,NULL,'tamb2112005@student.ctu.edu.vn','DI21V7F2'),(68,'B2112008','Nguyễn Hoàng Thắng',NULL,NULL,'thangb2112008@student.ctu.edu.vn','DI21V7F2'),(69,'B2112011','Phạm Thị Ngọc Thơ',NULL,NULL,'thob2112011@student.ctu.edu.vn','DI21V7F2'),(70,'B2112016','Võ Duy Toàn',NULL,NULL,'toanb2112016@student.ctu.edu.vn','DI21V7F2'),(71,'B2112019','Đặng Trí Trung',NULL,NULL,'trungb2112019@student.ctu.edu.vn','DI21V7F2'),(72,'B2112022','Nguyễn Trần Thanh Tú',NULL,NULL,'tub2112022@student.ctu.edu.vn','DI21V7F2'),(73,'B2105663','Tôn Thị Ngọc Châu',NULL,NULL,'chaub2105663@student.ctu.edu.vn','DI21V7F3'),(74,'B2105670','Dương Minh Khang',NULL,NULL,'khangb2105670@student.ctu.edu.vn','DI21V7F3'),(75,'B2105682','Lê Hoàng Phúc',NULL,NULL,'phucb2105682@student.ctu.edu.vn','DI21V7F3'),(76,'B2105688','Nguyễn Phương Thụy',NULL,NULL,'thuyb2105688@student.ctu.edu.vn','DI21V7F3'),(77,'B2105698','Lê Quốc Đạt',NULL,NULL,'datb2105698@student.ctu.edu.vn','DI21V7F3'),(78,'B2105718','Nguyễn Văn Quý',NULL,NULL,'quyb2105718@student.ctu.edu.vn','DI21V7F3'),(79,'B2108121','Nguyễn Duy Thanh',NULL,NULL,'thanhb2108121@student.ctu.edu.vn','DI21V7F3'),(80,'B2111807','Nguyễn Tấn Lộc',NULL,NULL,'locb2111807@student.ctu.edu.vn','DI21V7F3'),(81,'B2111886','Nguyễn Lê Gia Hưng',NULL,NULL,'hungb2111886@student.ctu.edu.vn','DI21V7F3'),(82,'B2111916','Võ Quốc Bằng',NULL,NULL,'bangb2111916@student.ctu.edu.vn','DI21V7F3'),(83,'B2111924','Nguyễn Huỳnh Bảo Hân',NULL,NULL,'hanb2111924@student.ctu.edu.vn','DI21V7F3'),(84,'B2111933','Trương Đặng Trúc Lâm',NULL,NULL,'lamb2111933@student.ctu.edu.vn','DI21V7F3'),(85,'B2111938','Nguyễn Huỳnh Ngọc Ngân',NULL,NULL,'nganb2111938@student.ctu.edu.vn','DI21V7F3'),(86,'B2111942','Ung Khánh Như',NULL,NULL,'nhub2111942@student.ctu.edu.vn','DI21V7F3'),(87,'B2111948','Võ Tấn Tài',NULL,NULL,'taib2111948@student.ctu.edu.vn','DI21V7F3'),(88,'B2111951','Vũ Trần Quốc Thái',NULL,NULL,'thaib2111951@student.ctu.edu.vn','DI21V7F3'),(89,'B2111957','Phan Trung Thuận',NULL,NULL,'thuanb2111957@student.ctu.edu.vn','DI21V7F3'),(90,'B2111961','Phan Thị Bích Trân',NULL,NULL,'tranb2111961@student.ctu.edu.vn','DI21V7F3'),(91,'B2111965','Trát Lâm Trường',NULL,NULL,'truongb2111965@student.ctu.edu.vn','DI21V7F3'),(92,'B2111971','Nguyễn Duy Bằng',NULL,NULL,'bangb2111971@student.ctu.edu.vn','DI21V7F3'),(93,'B2111974','Trần Quốc Duy',NULL,NULL,'duyb2111974@student.ctu.edu.vn','DI21V7F3'),(94,'B2111977','Lê Huỳnh Đẳng',NULL,NULL,'dangb2111977@student.ctu.edu.vn','DI21V7F3'),(95,'B2111981','Nguyễn Trương Thiện Hiếu',NULL,NULL,'hieub2111981@student.ctu.edu.vn','DI21V7F3'),(96,'B2111984','Đặng Hoàng Hưng',NULL,NULL,'hungb2111984@student.ctu.edu.vn','DI21V7F3'),(97,'B2111994','Ngô Bảo Ngọc',NULL,NULL,'ngocb2111994@student.ctu.edu.vn','DI21V7F3'),(98,'B2112002','Trần Văn Sang',NULL,NULL,'sangb2112002@student.ctu.edu.vn','DI21V7F3'),(99,'B2112006','Trần Thị Thanh Thanh',NULL,NULL,'thanhb2112006@student.ctu.edu.vn','DI21V7F3'),(100,'B2112009','Đỗ Huy Thịnh',NULL,NULL,'thinhb2112009@student.ctu.edu.vn','DI21V7F3'),(101,'B2112012','Nguyễn Văn Thuần',NULL,NULL,'thuanb2112012@student.ctu.edu.vn','DI21V7F3'),(102,'B2112017','Trần Hà Minh Triết',NULL,NULL,'trietb2112017@student.ctu.edu.vn','DI21V7F3'),(103,'B2112020','Trần Nhựt Trương',NULL,NULL,'truongb2112020@student.ctu.edu.vn','DI21V7F3'),(104,'B2105665','Lâm Nhật Hào',NULL,NULL,'haob2105665@student.ctu.edu.vn','DI21V7F4'),(105,'B2105689','Nguyễn Trung Tín',NULL,NULL,'tinb2105689@student.ctu.edu.vn','DI21V7F4'),(106,'B2105704','Đinh Hà Khang',NULL,NULL,'khangb2105704@student.ctu.edu.vn','DI21V7F4'),(107,'B2105721','Nguyễn Thái Thuận',NULL,NULL,'thuanb2105721@student.ctu.edu.vn','DI21V7F4'),(108,'B2109666','Tô Kiều Diễm Quỳnh',NULL,NULL,'quynhb2109666@student.ctu.edu.vn','DI21V7F4'),(109,'B2111862','Phạm Trần Anh Tài',NULL,NULL,'taib2111862@student.ctu.edu.vn','DI21V7F4'),(110,'B2111913','Nguyễn Phan Hồng An',NULL,NULL,'anb2111913@student.ctu.edu.vn','DI21V7F4'),(111,'B2111917','Phạm Công Danh',NULL,NULL,'danhb2111917@student.ctu.edu.vn','DI21V7F4'),(112,'B2111925','Hà Minh Hiếu',NULL,NULL,'hieub2111925@student.ctu.edu.vn','DI21V7F4'),(113,'B2111929','Trần Đình Khang',NULL,NULL,'khangb2111929@student.ctu.edu.vn','DI21V7F4'),(114,'B2111934','Nguyễn Gia Linh',NULL,NULL,'linhb2111934@student.ctu.edu.vn','DI21V7F4');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studying`
--

DROP TABLE IF EXISTS `studying`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studying` (
  `st_code` varchar(8) NOT NULL,
  `clCourse_ID` int(11) NOT NULL,
  PRIMARY KEY (`st_code`,`clCourse_ID`),
  KEY `clCourse_ID` (`clCourse_ID`),
  CONSTRAINT `studying_ibfk_1` FOREIGN KEY (`st_code`) REFERENCES `students` (`st_code`),
  CONSTRAINT `studying_ibfk_2` FOREIGN KEY (`clCourse_ID`) REFERENCES `classcourse` (`clCourse_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studying`
--

LOCK TABLES `studying` WRITE;
/*!40000 ALTER TABLE `studying` DISABLE KEYS */;
INSERT INTO `studying` VALUES ('B2105661',137),('B2105661',138),('B2105661',140),('B2105661',141),('B2105661',142),('B2105661',143),('B2105661',144),('B2105661',145),('B2105661',146),('B2105661',147),('B2105661',148),('B2105661',150),('B2105661',151),('B2105661',153),('B2105661',154),('B2105661',155),('B2105661',156),('B2105661',157),('B2105661',158),('B2105661',159),('B2105661',160),('B2105661',161),('B2105661',162),('B2105661',163),('B2105661',165),('B2105661',166),('B2105661',167),('B2105661',168),('B2105661',170),('B2105661',171),('B2105661',173),('B2105661',174),('B2105661',175),('B2105661',176),('B2105661',177),('B2105661',178),('B2105661',179),('B2105661',180),('B2105661',181),('B2105661',182),('B2105661',183),('B2105661',184),('B2105661',185),('B2105661',186),('B2105661',187),('B2105661',188),('B2105661',189),('B2105661',190),('B2105661',191),('B2105661',213),('B2105661',214),('B2105661',215),('B2105661',216),('B2105661',217),('B2105661',218),('B2105661',219),('B2105661',220),('B2105661',221),('B2105661',222),('B2105661',223),('B2105661',224),('B2105661',227),('B2105661',228),('B2105681',213),('B2105681',214),('B2105681',215),('B2105681',216),('B2105681',217),('B2105681',218),('B2105684',213),('B2105684',214),('B2105684',215),('B2105684',216),('B2105684',217),('B2105684',218),('B2105695',213),('B2105695',214),('B2105695',215),('B2105695',216),('B2105695',217),('B2105695',218),('B2110011',213),('B2110011',214),('B2110011',215),('B2110011',216),('B2110011',217),('B2110011',218),('B2110058',213),('B2110058',214),('B2110058',215),('B2110058',216),('B2110058',217),('B2110058',218),('B2111915',213),('B2111915',214),('B2111915',215),('B2111915',216),('B2111915',217),('B2111915',218),('B2111930',213),('B2111930',214),('B2111930',215),('B2111930',216),('B2111930',217),('B2111930',218),('B2111936',213),('B2111936',214),('B2111936',215),('B2111936',216),('B2111936',217),('B2111936',218),('B2111946',213),('B2111946',214),('B2111946',215),('B2111946',216),('B2111946',217),('B2111946',218),('B2111949',213),('B2111949',214),('B2111949',215),('B2111949',216),('B2111949',217),('B2111949',218),('B2111955',213),('B2111955',214),('B2111955',215),('B2111955',216),('B2111955',217),('B2111955',218),('B2111956',213),('B2111956',214),('B2111956',215),('B2111956',216),('B2111956',217),('B2111956',218),('B2111959',213),('B2111959',214),('B2111959',215),('B2111959',216),('B2111959',217),('B2111959',218),('B2111994',213),('B2111994',214),('B2111994',215),('B2111994',216),('B2111994',217),('B2111994',218),('B2111995',213),('B2111995',214),('B2111995',215),('B2111995',216),('B2111995',217),('B2111995',218),('B2111996',213),('B2111996',214),('B2111996',215),('B2111996',216),('B2111996',217),('B2111996',218),('B2112000',213),('B2112000',214),('B2112000',215),('B2112000',216),('B2112000',217),('B2112000',218),('B2112004',213),('B2112004',214),('B2112004',215),('B2112004',216),('B2112004',217),('B2112004',218),('B2112010',213),('B2112010',214),('B2112010',215),('B2112010',216),('B2112010',217),('B2112010',218),('B2112011',213),('B2112011',214),('B2112011',215),('B2112011',216),('B2112011',217),('B2112011',218);
/*!40000 ALTER TABLE `studying` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teaching`
--

DROP TABLE IF EXISTS `teaching`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teaching` (
  `teaching_ID` int(11) NOT NULL AUTO_INCREMENT,
  `cfa_ID` int(11) DEFAULT NULL,
  `ins_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`teaching_ID`),
  UNIQUE KEY `cfa_ID` (`cfa_ID`,`ins_ID`),
  KEY `fk_instructor_cfa` (`ins_ID`),
  CONSTRAINT `fk_cfa_instructor` FOREIGN KEY (`cfa_ID`) REFERENCES `coursefollowacayear` (`cfa_ID`),
  CONSTRAINT `fk_instructor_cfa` FOREIGN KEY (`ins_ID`) REFERENCES `instructor` (`ins_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teaching`
--

LOCK TABLES `teaching` WRITE;
/*!40000 ALTER TABLE `teaching` DISABLE KEYS */;
INSERT INTO `teaching` VALUES (69,67,1),(70,68,2),(71,69,3),(72,70,4),(73,71,5),(74,72,6),(75,73,7),(76,74,8),(77,75,1),(78,76,2),(79,77,3),(80,78,4),(81,79,5),(82,80,6),(83,81,7),(84,82,8),(85,83,1),(86,84,2),(87,85,3),(88,86,4),(89,87,5),(90,88,6),(91,89,7),(92,90,8),(93,91,1),(94,92,2),(95,93,3),(96,94,4),(97,95,5),(98,96,6),(99,97,7),(100,98,8),(101,99,1),(102,100,2),(103,101,3),(104,102,4),(105,103,5),(106,104,6),(107,105,7),(108,106,8),(109,107,1),(110,108,2),(111,109,3),(112,110,4),(113,111,5),(114,112,6),(115,113,7),(116,114,8),(117,115,1),(118,116,2),(119,117,2),(120,118,4),(121,119,5),(122,120,6),(123,121,2),(124,122,8),(125,123,1),(126,124,2),(127,125,3),(128,126,4),(129,127,5),(130,128,6),(131,129,7);
/*!40000 ALTER TABLE `teaching` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `tt_ID` int(11) NOT NULL AUTO_INCREMENT,
  `clCourse_ID` int(11) DEFAULT NULL,
  `tt_start` int(11) NOT NULL,
  `tt_classPeriod` int(11) DEFAULT NULL,
  `DOW_ID` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tt_ID`),
  KEY `room_id` (`room_id`),
  KEY `clCourse_ID` (`clCourse_ID`),
  KEY `DOW_ID` (`DOW_ID`),
  CONSTRAINT `timetable_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `classroom` (`room_id`),
  CONSTRAINT `timetable_ibfk_2` FOREIGN KEY (`clCourse_ID`) REFERENCES `classcourse` (`clCourse_ID`),
  CONSTRAINT `timetable_ibfk_3` FOREIGN KEY (`DOW_ID`) REFERENCES `dayofweak` (`DOW_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES (1,213,6,2,1,1),(2,213,6,2,2,2),(3,213,6,2,3,3),(4,213,6,2,4,4),(5,214,6,2,2,5),(6,214,6,2,1,6),(7,214,6,2,4,7),(8,214,6,2,3,8),(9,215,1,2,2,9),(10,215,1,2,1,10),(11,215,6,2,4,11),(12,215,6,2,3,12),(13,216,1,2,3,13),(14,216,1,2,4,14),(15,216,6,2,1,15),(16,216,6,2,2,16),(17,217,6,2,3,17),(18,217,6,2,4,18),(19,217,1,2,1,19),(20,217,1,2,2,20),(21,218,6,2,4,17),(22,218,6,2,3,18),(23,218,1,2,2,19),(24,218,1,2,1,20);
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `years`
--

DROP TABLE IF EXISTS `years`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `years` (
  `ay_schoolYear` varchar(255) NOT NULL,
  PRIMARY KEY (`ay_schoolYear`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `years`
--

LOCK TABLES `years` WRITE;
/*!40000 ALTER TABLE `years` DISABLE KEYS */;
INSERT INTO `years` VALUES ('2021-2022'),('2022-2023'),('2023-2024'),('2024-2025'),('2025-2026');
/*!40000 ALTER TABLE `years` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-11  8:17:14
