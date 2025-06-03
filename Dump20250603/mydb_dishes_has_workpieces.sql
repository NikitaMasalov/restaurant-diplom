-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	9.3.0

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
-- Table structure for table `dishes_has_workpieces`
--

DROP TABLE IF EXISTS `dishes_has_workpieces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dishes_has_workpieces` (
  `dishes_id` int NOT NULL,
  `workpieces_id` int NOT NULL,
  `amount` decimal(6,3) NOT NULL,
  PRIMARY KEY (`dishes_id`,`workpieces_id`),
  KEY `fk_dishes_has_workpieces_workpieces1_idx` (`workpieces_id`),
  KEY `fk_dishes_has_workpieces_dishes1_idx` (`dishes_id`),
  CONSTRAINT `fk_dishes_has_workpieces_dishes1` FOREIGN KEY (`dishes_id`) REFERENCES `dishes` (`id`),
  CONSTRAINT `fk_dishes_has_workpieces_workpieces1` FOREIGN KEY (`workpieces_id`) REFERENCES `workpieces` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dishes_has_workpieces`
--

LOCK TABLES `dishes_has_workpieces` WRITE;
/*!40000 ALTER TABLE `dishes_has_workpieces` DISABLE KEYS */;
INSERT INTO `dishes_has_workpieces` VALUES (1,1,200.000),(1,2,100.000),(1,3,150.000),(1,6,50.000),(2,1,200.000),(2,2,120.000),(2,3,150.000),(2,6,80.000),(3,5,50.000),(4,1,200.000),(4,3,150.000),(4,6,100.000),(5,8,20.000),(6,1,100.000),(6,3,80.000),(7,8,20.000),(8,1,200.000),(8,3,150.000),(8,6,100.000);
/*!40000 ALTER TABLE `dishes_has_workpieces` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-03 10:32:55
