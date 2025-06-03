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
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `status` enum('в ожидании','готов','завершён','отказ') NOT NULL,
  `client_id` int DEFAULT NULL,
  `employee_id` int NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Sales_client1_idx` (`client_id`),
  KEY `fk_Sales_employee1_idx` (`employee_id`),
  CONSTRAINT `fk_Sales_client1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `fk_Sales_employee1` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'2025-05-14 12:30:00','завершён',1,2,1050.00),(2,'2025-05-14 13:15:00','готов',2,2,620.00),(3,'2025-05-14 14:00:00','готов',NULL,3,140.00),(4,'2025-05-14 14:30:00','отказ',3,2,0.00),(5,'2025-05-14 15:45:00','завершён',4,2,390.00),(6,'2025-05-15 21:09:50','готов',NULL,6,810.00),(7,'2025-05-20 15:16:14','завершён',3,6,270.00),(8,'2025-05-20 15:17:29','завершён',3,6,900.00),(9,'2025-05-23 14:49:36','завершён',NULL,6,790.00),(10,'2025-05-23 14:50:01','завершён',NULL,6,890.00),(11,'2025-05-23 14:55:02','завершён',NULL,6,420.00),(12,'2025-05-23 17:01:32','готов',NULL,6,750.00),(16,'2025-05-24 11:51:25','завершён',NULL,6,440.00),(17,'2025-05-24 11:55:43','готов',NULL,6,610.00),(18,'2025-05-24 11:55:53','готов',NULL,6,630.00),(19,'2025-05-28 11:16:43','завершён',NULL,6,620.00),(20,'2025-05-28 11:16:55','завершён',NULL,6,490.00),(21,'2025-05-28 11:17:10','завершён',NULL,6,870.00);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-03 10:32:54
