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
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `points` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `number_UNIQUE` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Иванов Иван','+79161234567',150),(2,'Петрова Анна','+79269876543',75),(3,'Сидоров Алексей','+79031112233',205),(4,'Кузнецова Елена','+79507778899',50),(5,'Васильев Дмитрий','+79995554433',300);
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dishes`
--

DROP TABLE IF EXISTS `dishes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dishes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `menu_id` int NOT NULL,
  `recipe_id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `status` enum('в ожидании','готовиться','готово') NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Dishes_menu1_idx` (`menu_id`),
  KEY `fk_Dishes_recipe1_idx` (`recipe_id`),
  CONSTRAINT `fk_Dishes_menu1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`id`),
  CONSTRAINT `fk_Dishes_recipe1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dishes`
--

LOCK TABLES `dishes` WRITE;
/*!40000 ALTER TABLE `dishes` DISABLE KEYS */;
INSERT INTO `dishes` VALUES (1,1,1,'Пепперони','готово','2025-05-14 12:20:00','2025-05-14 12:25:00',450.00),(2,3,3,'Карбонара','готово','2025-05-14 12:20:00','2025-05-14 12:30:00',480.00),(3,4,4,'Картофель фри','готово','2025-05-14 12:25:00','2025-05-14 12:28:00',150.00),(4,2,2,'Маргарита','готово','2025-05-14 13:10:00','2025-05-14 13:15:00',390.00),(5,6,6,'Капучино','готово','2025-05-14 13:12:00','2025-05-14 13:14:00',120.00),(6,5,5,'Сырные палочки','готово','2025-05-14 13:13:00','2025-05-14 13:16:00',180.00),(7,7,7,'Латте','готово','2025-05-14 13:55:00','2025-05-20 23:22:05',140.00),(8,2,2,'Маргарита','готово','2025-05-14 15:40:00','2025-05-14 15:45:00',390.00),(9,1,1,'Пепперони','готово','2025-05-15 21:09:50','2025-05-20 17:15:09',450.00),(10,7,7,'Латте','готово','2025-05-15 21:09:50','2025-05-20 23:22:06',140.00),(11,8,8,'Чизкейк','готово','2025-05-15 21:09:50','2025-05-20 23:22:06',220.00),(12,7,7,'Латте','готово','2025-05-20 15:16:14','2025-05-20 17:17:54',140.00),(13,4,4,'Картофель фри','готово','2025-05-20 15:16:14','2025-05-20 23:22:06',150.00),(14,5,5,'Сырные палочки','готово','2025-05-20 15:16:14','2025-05-20 23:22:07',180.00),(15,4,4,'Картофель фри','готово','2025-05-20 15:17:29','2025-05-20 17:17:14',150.00),(16,8,8,'Чизкейк','готово','2025-05-20 15:17:29','2025-05-20 17:17:14',220.00),(17,7,7,'Латте','готово','2025-05-20 15:17:29','2025-05-20 17:17:15',140.00),(18,2,2,'Маргарита','готово','2025-05-20 15:17:29','2025-05-20 17:17:15',390.00),(19,8,8,'Чизкейк','готово','2025-05-23 14:49:36','2025-05-23 14:50:38',220.00),(20,2,2,'Маргарита','готово','2025-05-23 14:49:36','2025-05-23 14:52:25',390.00),(21,5,5,'Сырные палочки','готово','2025-05-23 14:49:36','2025-05-23 14:52:47',180.00),(22,4,4,'Картофель фри','готово','2025-05-23 14:50:01','2025-05-23 14:52:49',150.00),(23,7,7,'Латте','готово','2025-05-23 14:50:01','2025-05-23 14:52:58',140.00),(24,4,4,'Картофель фри','готово','2025-05-23 14:55:02','2025-05-23 14:58:01',150.00),(25,6,6,'Капучино','готово','2025-05-23 14:55:02','2025-05-23 14:58:12',120.00),(26,1,1,'Пепперони','готово','2025-05-23 17:01:32','2025-05-23 17:03:51',450.00),(27,4,4,'Картофель фри','готово','2025-05-23 17:01:32','2025-05-23 17:03:57',150.00),(28,4,4,'Картофель фри','готово','2025-05-23 17:01:32','2025-05-23 17:04:14',150.00),(39,8,8,'Чизкейк','готово','2025-05-24 11:51:25','2025-05-24 11:56:36',220.00),(40,8,8,'Чизкейк','готово','2025-05-24 11:51:25','2025-05-24 11:56:37',220.00),(41,8,8,'Чизкейк','готово','2025-05-24 11:55:43','2025-05-24 11:56:38',220.00),(42,2,2,'Маргарита','готово','2025-05-24 11:55:43','2025-05-24 11:59:49',390.00),(43,6,6,'Капучино','готово','2025-05-24 11:55:53','2025-05-24 11:59:49',120.00),(44,5,5,'Сырные палочки','готово','2025-05-24 11:55:53','2025-05-24 11:59:49',180.00),(45,5,5,'Сырные палочки','готово','2025-05-24 11:55:53','2025-05-24 11:59:49',180.00),(46,4,4,'Картофель фри','готово','2025-05-24 11:55:53','2025-05-24 11:59:50',150.00),(47,7,7,'Латте','готово','2025-05-28 11:16:43','2025-05-28 11:18:14',140.00),(48,3,3,'Карбонара','готово','2025-05-28 11:16:43','2025-05-28 11:19:24',480.00),(49,8,8,'Чизкейк','готово','2025-05-28 11:16:55','2025-05-28 11:19:24',220.00),(50,6,6,'Капучино','готово','2025-05-28 11:16:55','2025-05-28 11:18:15',120.00),(51,4,4,'Картофель фри','готово','2025-05-28 11:16:55','2025-05-28 11:19:25',150.00),(52,1,1,'Пепперони','готово','2025-05-28 11:17:10','2025-05-28 11:19:25',450.00),(53,4,4,'Картофель фри','готово','2025-05-28 11:17:10','2025-05-28 11:19:25',150.00),(54,4,4,'Картофель фри','готово','2025-05-28 11:17:10','2025-05-28 11:19:26',150.00),(55,6,6,'Капучино','готово','2025-05-28 11:17:10','2025-05-28 11:18:16',120.00),(56,8,8,'Чизкейк','готово','2025-06-05 21:01:29','2025-06-05 21:03:45',220.00),(57,3,3,'Карбонара','готово','2025-06-05 21:01:29','2025-06-05 21:04:23',480.00),(58,5,5,'Сырные палочки','готово','2025-06-05 21:01:29','2025-06-05 21:04:23',180.00),(59,7,7,'Латте','готово','2025-06-05 21:01:46','2025-06-05 21:02:39',140.00),(60,4,4,'Картофель фри','готово','2025-06-05 21:01:46','2025-06-05 21:04:24',150.00),(61,4,4,'Картофель фри','готово','2025-06-05 21:01:46','2025-06-05 21:02:40',150.00),(62,1,1,'Пепперони','готово','2025-06-05 21:02:00','2025-06-05 21:03:55',450.00),(63,6,6,'Капучино','готово','2025-06-05 21:02:00','2025-06-05 21:02:41',120.00),(64,7,7,'Латте','готово','2025-06-05 21:07:31','2025-06-05 21:08:09',140.00),(65,7,7,'Латте','готово','2025-06-05 21:07:31','2025-06-05 21:08:10',140.00),(66,7,7,'Латте','готово','2025-06-08 19:12:09','2025-06-08 19:17:56',140.00),(67,1,1,'Пепперони','готово','2025-06-09 00:40:44','2025-06-09 00:46:48',450.00),(68,8,8,'Чизкейк','готово','2025-06-09 00:40:44','2025-06-09 00:46:48',220.00),(69,7,7,'Латте','готово','2025-06-09 00:40:44','2025-06-09 00:41:17',140.00),(70,7,7,'Латте','готово','2025-06-09 00:40:54','2025-06-09 00:41:18',140.00),(71,5,5,'Сырные палочки','готово','2025-06-09 00:40:54','2025-06-09 00:46:48',180.00),(72,4,4,'Картофель фри','готово','2025-06-09 00:40:54','2025-06-09 00:46:48',150.00);
/*!40000 ALTER TABLE `dishes` ENABLE KEYS */;
UNLOCK TABLES;

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

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `position` varchar(45) NOT NULL,
  `password_cash` varchar(255) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `number_UNIQUE` (`phone`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Смирнов Александр','+79051234567','Повар','c4ca4238a0b923820dcc509a6f75849b',1),(2,'Ковалева Мария','+79162345678','Кассир','c4ca4238a0b923820dcc509a6f75849b',1),(3,'Николаев Сергей','+79263456789','Кассир','c4ca4238a0b923820dcc509a6f75849b',1),(4,'Федорова Ольга','+79364567890','Менеджер','c4ca4238a0b923820dcc509a6f75849b',1),(5,'Дмитриев Андрей','+79465678901','Повар','c4ca4238a0b923820dcc509a6f75849b',1),(6,'1','+79234524245','Менеджер','c4ca4238a0b923820dcc509a6f75849b',1),(8,'Анисджон','+7905423452','Кассир','202cb962ac59075b964b07152d234b70',0),(9,'Кассир','+78923424433','Кассир','c4ca4238a0b923820dcc509a6f75849b',1),(10,'Повар','+89342424242','Повар','c4ca4238a0b923820dcc509a6f75849b',1);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text NOT NULL,
  `category` varchar(255) NOT NULL,
  `stop_list` tinyint NOT NULL,
  `recipe_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_menu_recipe1_idx` (`recipe_id`),
  CONSTRAINT `fk_menu_recipe1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'Пепперони',450.00,'Пицца с колбасой пепперони и сыром','Пицца',0,1),(2,'Маргарита',390.00,'Классическая пицца с томатами и сыром','Пицца',0,2),(3,'Карбонара',480.00,'Пицца с ветчиной, яйцом и сыром','Пицца',0,3),(4,'Картофель фри',150.00,'Хрустящий картофель фри с соусом','Закуски',0,4),(5,'Сырные палочки',180.00,'Хрустящие палочки из сырного теста','Закуски',0,5),(6,'Капучино',120.00,'Классический капучино','Напитки',0,6),(7,'Латте',140.00,'Кофе с молоком','Напитки',0,7),(8,'Чизкейк',220.00,'Классический чизкейк','Десерты',0,8),(9,'Тирамису',240.00,'Итальянский десерт с кофе','Десерты',1,9);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe`
--

DROP TABLE IF EXISTS `recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `weight` decimal(6,3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe`
--

LOCK TABLES `recipe` WRITE;
/*!40000 ALTER TABLE `recipe` DISABLE KEYS */;
INSERT INTO `recipe` VALUES (1,'Рецепт Пепперони',500.000),(2,'Рецепт Маргариты',450.000),(3,'Рецепт Карбонары',550.000),(4,'Рецепт картофеля фри',200.000),(5,'Рецепт сырных палочек',180.000),(6,'Рецепт капучино',180.000),(7,'Рецепт латте',200.000),(8,'Рецепт чизкейка',150.000),(9,'Рецепт тирамису',160.000);
/*!40000 ALTER TABLE `recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_has_workpieces`
--

DROP TABLE IF EXISTS `recipe_has_workpieces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_has_workpieces` (
  `recipe_id` int NOT NULL,
  `workpieces_id` int NOT NULL,
  `amount` decimal(6,3) NOT NULL,
  PRIMARY KEY (`recipe_id`,`workpieces_id`),
  KEY `fk_recipe_has_workpieces_workpieces1_idx` (`workpieces_id`),
  KEY `fk_recipe_has_workpieces_recipe1_idx` (`recipe_id`),
  CONSTRAINT `fk_recipe_has_workpieces_recipe1` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`),
  CONSTRAINT `fk_recipe_has_workpieces_workpieces1` FOREIGN KEY (`workpieces_id`) REFERENCES `workpieces` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_has_workpieces`
--

LOCK TABLES `recipe_has_workpieces` WRITE;
/*!40000 ALTER TABLE `recipe_has_workpieces` DISABLE KEYS */;
INSERT INTO `recipe_has_workpieces` VALUES (1,1,200.000),(1,2,100.000),(1,3,150.000),(1,6,50.000),(2,1,200.000),(2,3,150.000),(2,6,100.000),(3,1,200.000),(3,2,120.000),(3,3,150.000),(3,6,80.000),(4,5,50.000),(5,1,100.000),(5,3,80.000),(6,8,20.000),(7,8,20.000),(8,3,50.000),(8,9,100.000),(9,3,40.000),(9,8,30.000),(9,9,90.000);
/*!40000 ALTER TABLE `recipe_has_workpieces` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'2025-05-14 12:30:00','завершён',1,2,1050.00),(2,'2025-05-14 13:15:00','готов',2,2,620.00),(3,'2025-05-14 14:00:00','готов',NULL,3,140.00),(4,'2025-05-14 14:30:00','отказ',3,2,0.00),(5,'2025-05-14 15:45:00','завершён',4,2,390.00),(6,'2025-05-15 21:09:50','готов',NULL,6,810.00),(7,'2025-05-20 15:16:14','завершён',3,6,270.00),(8,'2025-05-20 15:17:29','завершён',3,6,900.00),(9,'2025-05-23 14:49:36','завершён',NULL,6,790.00),(10,'2025-05-23 14:50:01','завершён',NULL,6,890.00),(11,'2025-05-23 14:55:02','завершён',NULL,6,420.00),(12,'2025-05-23 17:01:32','готов',NULL,6,750.00),(16,'2025-05-24 11:51:25','завершён',NULL,6,440.00),(17,'2025-05-24 11:55:43','готов',NULL,6,610.00),(18,'2025-05-24 11:55:53','готов',NULL,6,630.00),(19,'2025-05-28 11:16:43','завершён',NULL,6,620.00),(20,'2025-05-28 11:16:55','завершён',NULL,6,490.00),(21,'2025-05-28 11:17:10','завершён',NULL,6,870.00),(22,'2025-06-05 21:01:29','завершён',NULL,6,880.00),(23,'2025-06-05 21:01:46','завершён',NULL,6,440.00),(24,'2025-06-05 21:02:00','завершён',NULL,6,570.00),(25,'2025-06-05 21:07:31','завершён',NULL,6,280.00),(26,'2025-06-08 19:12:09','завершён',NULL,6,140.00),(27,'2025-06-09 00:40:44','завершён',NULL,6,810.00),(28,'2025-06-09 00:40:54','завершён',NULL,6,470.00);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `sales_has_dishes` VALUES (1,1),(1,2),(1,3),(2,4),(2,5),(2,6),(3,7),(5,8),(6,9),(6,10),(6,11),(7,12),(7,13),(7,14),(8,15),(8,16),(8,17),(8,18),(9,19),(9,20),(9,21),(10,22),(10,23),(11,24),(11,25),(12,26),(12,27),(12,28),(16,39),(16,40),(17,41),(17,42),(18,43),(18,44),(18,45),(18,46),(19,47),(19,48),(20,49),(20,50),(20,51),(21,52),(21,53),(21,54),(21,55),(22,56),(22,57),(22,58),(23,59),(23,60),(23,61),(24,62),(24,63),(25,64),(25,65),(26,66),(27,67),(27,68),(27,69),(28,70),(28,71),(28,72);
/*!40000 ALTER TABLE `sales_has_dishes` ENABLE KEYS */;
UNLOCK TABLES;

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
INSERT INTO `workpieces` VALUES (1,'Тесто','2025-06-15 00:00:00','Пекарня №1',400.000,5.000,-185.000),(2,'Ветчина','2025-05-20 00:00:00','Мясной комбинат',15.000,3.000,-92.000),(3,'Сыр','2025-06-01 00:00:00','Сыродел',300.000,4.000,-188.000),(4,'Майонез','2025-07-10 00:00:00','Соусы и приправы',540.000,1.000,4.500),(5,'Кетчуп','2025-08-01 00:00:00','Соусы и приправы',450.000,1.000,4.000),(6,'Помидоры','2025-05-18 00:00:00','Овощебаза',100.000,2.000,-44.000),(7,'Огурцы','2025-05-17 00:00:00','Овощебаза',600.000,2.000,5.000),(8,'Кофе','2025-12-01 00:00:00','Кофейная компания',100.000,1.000,-17.500),(9,'Творог','2025-05-16 00:00:00','Молочный завод',-100.000,1.000,-98.000);
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

-- Dump completed on 2025-06-09  1:37:31
