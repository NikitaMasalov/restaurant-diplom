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
-- Table structure for table `workpieces`
--

DROP TABLE IF EXISTS `workpieces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workpieces` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `expiration_date` datetime NOT NULL,
  `manufacturer` varchar(255) NOT NULL,
  `amount` decimal(6,3) NOT NULL,
  `min_amount` decimal(6,3) NOT NULL,
  `in_stock_amount` decimal(6,3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workpieces`
--

LOCK TABLES `workpieces` WRITE;
/*!40000 ALTER TABLE `workpieces` DISABLE KEYS */;
INSERT INTO `workpieces` VALUES (1,'Тесто','2025-06-15 00:00:00','Пекарня №1',300.000,5.000,-185.000),(2,'Ветчина','2025-05-20 00:00:00','Мясной комбинат',40.000,3.000,-92.000),(3,'Сыр','2025-06-01 00:00:00','Сыродел',-410.000,4.000,-188.000),(4,'Майонез','2025-07-10 00:00:00','Соусы и приправы',540.000,1.000,4.500),(5,'Кетчуп','2025-08-01 00:00:00','Соусы и приправы',600.000,1.000,4.000),(6,'Помидоры','2025-05-18 00:00:00','Овощебаза',170.000,2.000,-44.000),(7,'Огурцы','2025-05-17 00:00:00','Овощебаза',600.000,2.000,5.000),(8,'Кофе','2025-12-01 00:00:00','Кофейная компания',120.000,1.000,-17.500),(9,'Творог','2025-05-16 00:00:00','Молочный завод',100.000,1.000,-98.000);
/*!40000 ALTER TABLE `workpieces` ENABLE KEYS */;
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
