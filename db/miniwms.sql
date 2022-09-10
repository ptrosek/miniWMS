CREATE DATABASE  IF NOT EXISTS `miniwms` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `miniwms`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: miniwms
-- ------------------------------------------------------
-- Server version	8.0.30-0ubuntu0.22.04.1

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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idcategory_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `good_type`
--

DROP TABLE IF EXISTS `good_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `good_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `ean` bigint DEFAULT NULL,
  `size` varchar(100) DEFAULT NULL,
  `weight` varchar(100) DEFAULT NULL,
  `package_type_gt` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idgood_type_UNIQUE` (`id`),
  KEY `good_type-package_idx` (`package_type_gt`),
  CONSTRAINT `good_type-package` FOREIGN KEY (`package_type_gt`) REFERENCES `package_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `good_type`
--

LOCK TABLES `good_type` WRITE;
/*!40000 ALTER TABLE `good_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `good_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `issue`
--

DROP TABLE IF EXISTS `issue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `issue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `customer` int DEFAULT NULL,
  `user_executing` int DEFAULT NULL,
  `user_approving` int DEFAULT NULL,
  `position_is` int DEFAULT NULL,
  `time_info` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` varchar(1000) DEFAULT NULL,
  `departure` datetime DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `is-user_idx` (`user_executing`),
  KEY `is-pos_idx` (`position_is`),
  KEY `is-org_idx` (`customer`),
  KEY `is-user2_idx` (`user_approving`),
  CONSTRAINT `is-org` FOREIGN KEY (`customer`) REFERENCES `outside_org` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `is-pos` FOREIGN KEY (`position_is`) REFERENCES `position` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `is-user` FOREIGN KEY (`user_executing`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `is-user2` FOREIGN KEY (`user_approving`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `issue`
--

LOCK TABLES `issue` WRITE;
/*!40000 ALTER TABLE `issue` DISABLE KEYS */;
/*!40000 ALTER TABLE `issue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `move`
--

DROP TABLE IF EXISTS `move`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `move` (
  `id` int NOT NULL AUTO_INCREMENT,
  `end_pos` int DEFAULT NULL,
  `user_approving` int DEFAULT NULL,
  `time_info` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` varchar(1000) DEFAULT NULL,
  `user_executing` int DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `moveusera_idx` (`user_approving`),
  KEY `moveusere_idx` (`user_executing`),
  KEY `moveendpos_idx` (`end_pos`),
  CONSTRAINT `moveendpos` FOREIGN KEY (`end_pos`) REFERENCES `position` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `moveusera` FOREIGN KEY (`user_approving`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `moveusere` FOREIGN KEY (`user_executing`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `move`
--

LOCK TABLES `move` WRITE;
/*!40000 ALTER TABLE `move` DISABLE KEYS */;
/*!40000 ALTER TABLE `move` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `move__record`
--

DROP TABLE IF EXISTS `move__record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `move__record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `move_id` int NOT NULL,
  `record_id` int NOT NULL,
  `start_pos` int NOT NULL,
  `end_pos` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `mrposs_idx` (`start_pos`),
  KEY `mrpose_idx` (`end_pos`),
  KEY `mrrecord_idx` (`record_id`),
  KEY `mrmove_idx` (`move_id`),
  CONSTRAINT `mrmove` FOREIGN KEY (`move_id`) REFERENCES `move` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `mrpose` FOREIGN KEY (`end_pos`) REFERENCES `position` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `mrposs` FOREIGN KEY (`start_pos`) REFERENCES `position` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `mrrecord` FOREIGN KEY (`record_id`) REFERENCES `record` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `move__record`
--

LOCK TABLES `move__record` WRITE;
/*!40000 ALTER TABLE `move__record` DISABLE KEYS */;
/*!40000 ALTER TABLE `move__record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation`
--

DROP TABLE IF EXISTS `operation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ops_type` int NOT NULL,
  `user_executing` int NOT NULL,
  `comment` varchar(1000) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_approving` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ops-type_idx` (`ops_type`),
  KEY `ops-user_idx` (`user_executing`),
  KEY `userappr-ops_idx` (`user_approving`),
  CONSTRAINT `ops-type` FOREIGN KEY (`ops_type`) REFERENCES `operation_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ops-user` FOREIGN KEY (`user_executing`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `userappr-ops` FOREIGN KEY (`user_approving`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation`
--

LOCK TABLES `operation` WRITE;
/*!40000 ALTER TABLE `operation` DISABLE KEYS */;
/*!40000 ALTER TABLE `operation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `operation_type`
--

DROP TABLE IF EXISTS `operation_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `operation_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `operation_link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idoperation_type_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `operation_type`
--

LOCK TABLES `operation_type` WRITE;
/*!40000 ALTER TABLE `operation_type` DISABLE KEYS */;
INSERT INTO `operation_type` VALUES (1,'login','record user login','/login'),(2,'logout','record user logout','/logout'),(3,'receipt creation','record manager creating receipt','/receipt'),(4,'other actions usage','record admin creating something using other actions tab','/'),(5,'position move creation','record action of moving a record beetwen positions','/move'),(6,'stock issue creation','record manager creating stock issue','/issue'),(7,'lookup','user looking up something','/lookup'),(8,'receipt handling','record user handling a receipt of goods','/hand'),(9,'issue handling','record user handling a issue of goods','/hand'),(10,'move handling','record user handling a move of goods','/hand');
/*!40000 ALTER TABLE `operation_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outside_org`
--

DROP TABLE IF EXISTS `outside_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `outside_org` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `bank_info` varchar(255) DEFAULT NULL,
  `addres` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outside_org`
--

LOCK TABLES `outside_org` WRITE;
/*!40000 ALTER TABLE `outside_org` DISABLE KEYS */;
/*!40000 ALTER TABLE `outside_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `package_type`
--

DROP TABLE IF EXISTS `package_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `package_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `package_type`
--

LOCK TABLES `package_type` WRITE;
/*!40000 ALTER TABLE `package_type` DISABLE KEYS */;
INSERT INTO `package_type` VALUES (1,'standard box'),(2,'pallet'),(3,'envelope'),(4,'rigid box'),(5,'loose');
/*!40000 ALTER TABLE `package_type` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `package_type` WRITE;
/*!40000 ALTER TABLE `package_type` DISABLE KEYS */;
/*!40000 ALTER TABLE `package_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `position` (
  `id` int NOT NULL AUTO_INCREMENT,
  `row` int NOT NULL,
  `column` int NOT NULL,
  `cell` int DEFAULT NULL,
  `warehouse_pos` int DEFAULT NULL,
  `zone` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `position-warehouse_idx` (`warehouse_pos`), 
  CONSTRAINT `position-warehouse` FOREIGN KEY (`warehouse_pos`) REFERENCES `warehouse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `position`
--

LOCK TABLES `position` WRITE;
/*!40000 ALTER TABLE `position` DISABLE KEYS */;
/*!40000 ALTER TABLE `position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier` int DEFAULT NULL,
  `user_executing` int DEFAULT NULL,
  `user_approving` int DEFAULT NULL,
  `position_re` int DEFAULT NULL,
  `time_info` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comment` varchar(1000) DEFAULT NULL,
  `arrival` datetime DEFAULT NULL,
  `completed` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `re-user_idx` (`user_executing`),
  KEY `re-pos_idx` (`position_re`),
  KEY `re-org_idx` (`supplier`),
  KEY `re-user2_idx` (`user_approving`),
  CONSTRAINT `re-org` FOREIGN KEY (`supplier`) REFERENCES `outside_org` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `re-pos` FOREIGN KEY (`position_re`) REFERENCES `position` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `re-user` FOREIGN KEY (`user_executing`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `re-user2` FOREIGN KEY (`user_approving`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record` (
  `id` int NOT NULL AUTO_INCREMENT,
  `comment` varchar(1000) DEFAULT NULL,
  `type` int NOT NULL,
  `receipt_rec` int NOT NULL,
  `issue_rec` int DEFAULT NULL,
  `current_position` int NOT NULL,
  `last_update` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `record-type_idx` (`type`),
  KEY `record-issue_idx` (`issue_rec`),
  KEY `record-recepit_idx` (`receipt_rec`),
  KEY `position_idx` (`current_position`),
  CONSTRAINT `position` FOREIGN KEY (`current_position`) REFERENCES `position` (`id`),
  CONSTRAINT `record-issue` FOREIGN KEY (`issue_rec`) REFERENCES `issue` (`id`),
  CONSTRAINT `record-recepit` FOREIGN KEY (`receipt_rec`) REFERENCES `receipt` (`id`),
  CONSTRAINT `record-type` FOREIGN KEY (`type`) REFERENCES `good_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record_ops`
--

DROP TABLE IF EXISTS `record_ops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `record_ops` (
  `id` int NOT NULL AUTO_INCREMENT,
  `record_id` int NOT NULL,
  `ops_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ops_idx` (`ops_id`),
  KEY `record_idx` (`record_id`),
  CONSTRAINT `ops` FOREIGN KEY (`ops_id`) REFERENCES `operation` (`id`),
  CONSTRAINT `record` FOREIGN KEY (`record_id`) REFERENCES `record` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record_ops`
--

LOCK TABLES `record_ops` WRITE;
/*!40000 ALTER TABLE `record_ops` DISABLE KEYS */;
/*!40000 ALTER TABLE `record_ops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `type__category`
--

DROP TABLE IF EXISTS `type__category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `type__category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoryid` int NOT NULL,
  `type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category-middle_idx` (`categoryid`),
  KEY `type-middle_idx` (`type_id`),
  CONSTRAINT `category-middle` FOREIGN KEY (`categoryid`) REFERENCES `category` (`id`),
  CONSTRAINT `type-middle` FOREIGN KEY (`type_id`) REFERENCES `good_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `type__category`
--

LOCK TABLES `type__category` WRITE;
/*!40000 ALTER TABLE `type__category` DISABLE KEYS */;
/*!40000 ALTER TABLE `type__category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `hash` varchar(1000) NOT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (0,'admin','pbkdf2:sha256:260000$OWEXGUTM$c353aff7df74c1ba73ba924e1f4b547bafdc362e72b58b83a30766202c7f418e',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user__user_type`
--

DROP TABLE IF EXISTS `user__user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user__user_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_idx` (`user_id`),
  KEY `type_idx` (`type_id`),
  CONSTRAINT `type` FOREIGN KEY (`type_id`) REFERENCES `user_type` (`id`),
  CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user__user_type`
--

LOCK TABLES `user__user_type` WRITE;
/*!40000 ALTER TABLE `user__user_type` DISABLE KEYS */;
INSERT INTO `user__user_type` VALUES (0,0,1),(1,0,2),(2,0,3);
/*!40000 ALTER TABLE `user__user_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_type`
--

DROP TABLE IF EXISTS `user_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_type`
--

LOCK TABLES `user_type` WRITE;
/*!40000 ALTER TABLE `user_type` DISABLE KEYS */;
INSERT INTO `user_type` VALUES (1,'administrator'),(2,'manager'),(3,'worker');
/*!40000 ALTER TABLE `user_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse`
--

DROP TABLE IF EXISTS `warehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `addres` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `size` varchar(255) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse`
--

LOCK TABLES `warehouse` WRITE;
/*!40000 ALTER TABLE `warehouse` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `warehouse__category`
--

DROP TABLE IF EXISTS `warehouse__category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `warehouse__category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idwarehouse` int DEFAULT NULL,
  `idcategory` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `warehouse-cat_idx` (`idwarehouse`),
  KEY `cat-warehouse_idx` (`idcategory`),
  CONSTRAINT `cat-warehouse` FOREIGN KEY (`idcategory`) REFERENCES `category` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `warehouse-cat` FOREIGN KEY (`idwarehouse`) REFERENCES `warehouse` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `warehouse__category`
--

LOCK TABLES `warehouse__category` WRITE;
/*!40000 ALTER TABLE `warehouse__category` DISABLE KEYS */;
/*!40000 ALTER TABLE `warehouse__category` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-10 17:07:01
