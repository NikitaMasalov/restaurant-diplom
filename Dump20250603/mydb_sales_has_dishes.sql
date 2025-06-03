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
-- Table structure for table `sales_has_dishes`
--

DROP TABLE IF EXISTS `sales_has_dishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_has_dishes` (
  `sales_id` int NOT NULL,
  `dishes_id` int NOT NULL,
  PRIMARY KEY (`sales_id`,`dishes_id`),
  KEY `fk_Sales_has_Dishes_Dishes1_idx` (`dishes_id`),
  KEY `fk_Sales_has_Dishes_Sales1_idx` (`sales_id`),
  CONSTRAINT `fk_Sales_has_Dishes_Dishes1` FOREIGN KEY (`dishes_id`) REFERENCES `dishes` (`id`),
  CONSTRAINT `fk_Sales_has_Dishes_Sales1` FOREIGN KEY (`sales_id`) REFERENCES `sales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_has_dishes`
--

LOCK TABLES `sales_has_dishes` WRITE;
/*!40000 ALTER TABLE `sales_has_dishes` DISABLE KEYS */;
INSERT INTO `sales_has_dishes` VALUES (1,1),(1,2),(1,3),(2,4),(2,5),(2,6),(3,7),(5,8),(6,9),(6,10),(6,11),(7,12),(7,13),(7,14),(8,15),(8,16),(8,17),(8,18),(9,19),(9,20),(9,21),(10,22),(10,23),(11,24),(11,25),(12,26),(12,27),(12,28),(16,39),(16,40),(17,41),(17,42),(18,43),(18,44),(18,45),(18,46),(19,47),(19,48),(20,49),(20,50),(20,51),(21,52),(21,53),(21,54),(21,55);
/*!40000 ALTER TABLE `sales_has_dishes` ENABLE KEYS */;
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
