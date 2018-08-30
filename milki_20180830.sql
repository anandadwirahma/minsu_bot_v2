/*
 Navicat Premium Data Transfer

 Source Server         : heroku-milki
 Source Server Type    : MySQL
 Source Server Version : 50556
 Source Host           : us-cdbr-iron-east-04.cleardb.net:3306
 Source Schema         : heroku_a23c62e0062b156

 Target Server Type    : MySQL
 Target Server Version : 50556
 File Encoding         : 65001

 Date: 30/08/2018 16:09:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `user` varchar(225) NOT NULL,
  `password` varchar(225) NOT NULL,
  `name` varchar(225) NOT NULL,
  `rule` varchar(20) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of admin
-- ----------------------------
BEGIN;
INSERT INTO `admin` VALUES (1, 'admin1', '0192023a7bbd73250516f069df18b500', 'Admin 1', '1', '', '');
INSERT INTO `admin` VALUES (12, 'fifi', 'cfc723a39d137f8428d8eeec9cebd384', 'Firdha Imamah', '1', '', '');
INSERT INTO `admin` VALUES (22, 'andre', 'dd573120e473c889140e34e817895495', 'Yusuf Andre', '1', '', '');
INSERT INTO `admin` VALUES (32, 'currier1', '1fac525b858485a6578ba926eac3c640', 'Currier 1', '2', '08134578914567', 'idle');
INSERT INTO `admin` VALUES (42, 'currier2', '1fac525b858485a6578ba926eac3c640', 'Currier 2', '2', '08346714567', 'idle');
INSERT INTO `admin` VALUES (52, 'currier3', '1fac525b858485a6578ba926eac3c640', 'Currier 3', '2', '08244467814', 'idle');
INSERT INTO `admin` VALUES (62, 'ika', 'f76523aea736f0d986763b43fbc686e1', 'Martha Ika Riyana', '1', '', '');
COMMIT;

-- ----------------------------
-- Table structure for barang
-- ----------------------------
DROP TABLE IF EXISTS `barang`;
CREATE TABLE `barang` (
  `id_brg` varchar(20) NOT NULL,
  `rasa` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `url_img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_brg`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of barang
-- ----------------------------
BEGIN;
INSERT INTO `barang` VALUES ('6jKAAn', 'Bublegum', 'Milshake rasa bublegum yang dapat mengocok mulutmu', 'https://milki.herokuapp.com/assets/img/milkshake_bublegum.png');
INSERT INTO `barang` VALUES ('7d0AOC', 'Bublegum', 'Olahan susu sapi segar dengan rasa bublegum yang lembut dan nikmat', 'https://milki.herokuapp.com/assets/img/250ml_bublegum.png');
INSERT INTO `barang` VALUES ('7mnAJO', 'Coklat', 'Olahan susu sapi coklat segar', 'https://milki.herokuapp.com/assets/img/chocolate.jpg');
INSERT INTO `barang` VALUES ('Bfw597', 'Vanilla', 'Olahan susu sapi segar dengan rasa vanilla yang maniis', 'https://milki.herokuapp.com/assets/img/250ml_vanilla.png');
INSERT INTO `barang` VALUES ('gf0yfu', 'Vanilla', 'Milshake rasa vanilla yang sangat smooth', 'https://milki.herokuapp.com/assets/img/milkshake_vanilla.png');
INSERT INTO `barang` VALUES ('IS3xGh', 'Strawberry', 'Milshake rasa strawberry yang dapat manis dan lembut', 'https://milki.herokuapp.com/assets/img/milkshake_strawberry.png');
INSERT INTO `barang` VALUES ('jG0RI9', 'Cappucino', 'kategori milkshake rasa cappucino', 'https://milki.herokuapp.com/assets/img/chocolate.jpg');
INSERT INTO `barang` VALUES ('lNDLOY', 'Moccha', 'Milkshake segar rasa mocha', 'https://milki.herokuapp.com/assets/img/chocolate.jpg');
INSERT INTO `barang` VALUES ('mkw16J', 'Taro', 'Milshake rasa taro yang lembut dan manis', 'https://milki.herokuapp.com/assets/img/milkshake_taro.png');
INSERT INTO `barang` VALUES ('Nt5fsh', 'Strawberry', 'Olahan susu sapi segar dengan rasa strawberry nikmat', 'https://milki.herokuapp.com/assets/img/250ml_strawberry.png');
INSERT INTO `barang` VALUES ('OvZIbP', 'Vanilla', 'Olahan susu sapi segar rasa vanilla', 'https://milki.herokuapp.com/assets/img/strawberry.jpg');
INSERT INTO `barang` VALUES ('TWFZej', 'Taro', 'Olahan susu sapi segar dengan rasa taro manis', 'https://milki.herokuapp.com/assets/img/250ml_taro.png');
COMMIT;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id_cat` int(20) NOT NULL AUTO_INCREMENT,
  `category` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `url_img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_cat`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of category
-- ----------------------------
BEGIN;
INSERT INTO `category` VALUES (1, 'Minsu', 'kategori susu sapi segar', 'https://milki.herokuapp.com/assets/img/cat_minsu.png');
INSERT INTO `category` VALUES (2, 'Milkshake', 'Kategori olahan susu milkhsake', 'https://milki.herokuapp.com/assets/img/cat_milkshake.png');
COMMIT;

-- ----------------------------
-- Table structure for chart_shop
-- ----------------------------
DROP TABLE IF EXISTS `chart_shop`;
CREATE TABLE `chart_shop` (
  `msisdn` varchar(255) DEFAULT NULL,
  `id_brg` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of chart_shop
-- ----------------------------
BEGIN;
INSERT INTO `chart_shop` VALUES ('Ua612f756b68df55b75bbb1fef726f512', '6');
INSERT INTO `chart_shop` VALUES ('U27afff1d2099b1b11fa81e8f7aa17ef9', '1');
INSERT INTO `chart_shop` VALUES ('U3485d512ea56b027be635c72924f03b1', '1');
INSERT INTO `chart_shop` VALUES ('U3485d512ea56b027be635c72924f03b1', '1');
INSERT INTO `chart_shop` VALUES ('U3485d512ea56b027be635c72924f03b1', '2');
INSERT INTO `chart_shop` VALUES ('U6097f19983034aa9f02806f83ef8b29e', '1');
INSERT INTO `chart_shop` VALUES ('Ubd3760052db6ec2cf33b5a98cee36de1', '1');
COMMIT;

-- ----------------------------
-- Table structure for detail_barang
-- ----------------------------
DROP TABLE IF EXISTS `detail_barang`;
CREATE TABLE `detail_barang` (
  `id_detail_brg` varchar(20) NOT NULL,
  `id_brg` varchar(20) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `stock` varchar(20) DEFAULT NULL,
  `harga` varchar(20) DEFAULT NULL,
  `id_cat` int(20) DEFAULT NULL,
  PRIMARY KEY (`id_detail_brg`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of detail_barang
-- ----------------------------
BEGIN;
INSERT INTO `detail_barang` VALUES ('4oiI9F', '6jKAAn', 'Medium', '18', '12000', 2);
INSERT INTO `detail_barang` VALUES ('6l0Pj1', 'IS3xGh', 'Large', '20', '15000', 2);
INSERT INTO `detail_barang` VALUES ('aEaKvj', 'mkw16J', 'Large', '20', '15000', 2);
INSERT INTO `detail_barang` VALUES ('av04BJ', 'Nt5fsh', '250 ML', '11', '15000', 1);
INSERT INTO `detail_barang` VALUES ('AzglQJ', 'TWFZej', '250 ML', '20', '15000', 1);
INSERT INTO `detail_barang` VALUES ('b8DNTn', 'gf0yfu', 'Large', '20', '15000', 2);
INSERT INTO `detail_barang` VALUES ('bqkpiz', '6jKAAn', 'Small', '20', '8000', 2);
INSERT INTO `detail_barang` VALUES ('ELCRrW', 'Bfw597', '120 ML', '19', '10000', 1);
INSERT INTO `detail_barang` VALUES ('JOZX6U', '7d0AOC', '250 ML', '20', '15000', 1);
INSERT INTO `detail_barang` VALUES ('krT65v', 'gf0yfu', 'Small', '20', '8000', 2);
INSERT INTO `detail_barang` VALUES ('lncmgJ', 'IS3xGh', 'Small', '20', '8000', 2);
INSERT INTO `detail_barang` VALUES ('oD16Gj', 'mkw16J', 'Small', '20', '8000', 2);
INSERT INTO `detail_barang` VALUES ('P7U4Kv', 'TWFZej', '120 ML', '20', '10000', 1);
INSERT INTO `detail_barang` VALUES ('pf4sy3', 'gf0yfu', 'Medium', '20', '12000', 2);
INSERT INTO `detail_barang` VALUES ('Q7aSwm', '6jKAAn', 'Large', '20', '15000', 2);
INSERT INTO `detail_barang` VALUES ('QjKoA7', 'IS3xGh', 'Medium', '20', '12000', 2);
INSERT INTO `detail_barang` VALUES ('rVL95r', 'Nt5fsh', '120 ML', '20', '10000', 1);
INSERT INTO `detail_barang` VALUES ('suuBoQ', 'Bfw597', '250 ML', '20', '15000', 1);
INSERT INTO `detail_barang` VALUES ('t0OwoD', '7d0AOC', '120 ML', '14', '10000', 1);
INSERT INTO `detail_barang` VALUES ('xAUIoe', 'mkw16J', 'Medium', '20', '12000', 2);
COMMIT;

-- ----------------------------
-- Table structure for detail_order
-- ----------------------------
DROP TABLE IF EXISTS `detail_order`;
CREATE TABLE `detail_order` (
  `id_order` varchar(20) DEFAULT NULL,
  `id_brg` varchar(20) DEFAULT NULL,
  `qty` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of detail_order
-- ----------------------------
BEGIN;
INSERT INTO `detail_order` VALUES ('OTTVUWAX', 'ELCRrW', '1');
INSERT INTO `detail_order` VALUES ('OTTVUWAX', 'av04BJ', '1');
INSERT INTO `detail_order` VALUES ('4P1BJIJ5', '4oiI9F', '2');
INSERT INTO `detail_order` VALUES ('4P1BJIJ5', 't0OwoD', '6');
INSERT INTO `detail_order` VALUES ('U6MZY8W9', 'av04BJ', '5');
COMMIT;

-- ----------------------------
-- Table structure for order
-- ----------------------------
DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id_order` varchar(20) NOT NULL,
  `nama` varchar(225) DEFAULT NULL,
  `tgl` datetime DEFAULT NULL,
  `lokasi` varchar(225) DEFAULT NULL,
  `status_payment` varchar(10) DEFAULT NULL,
  `harga` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `lineid` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id_order`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of order
-- ----------------------------
BEGIN;
INSERT INTO `order` VALUES ('4P1BJIJ5', 'H', '2018-08-30 13:16:05', 'Jl. Prof. DR. Satrio No.Kav 6, RT.4/RW.4, Kuningan, Karet Kuningan, Kecamatan Setiabudi, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12940, Indonesia', '3', '84000', 'Sasa@gmail.com', '8', 'Uf92435651e778366363b14f14a616a67');
INSERT INTO `order` VALUES ('OTTVUWAX', 'Ananda', '2018-08-30 02:26:19', 'Jl. Tebet Dalam 3A, Tebet Bar., Tebet, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12810, Indonesia', '5', '25000', 'anandadwi20@gmail.com', '83878718914', 'U6097f19983034aa9f02806f83ef8b29e');
INSERT INTO `order` VALUES ('U6MZY8W9', 'Bangbul', '2018-08-30 13:35:36', 'Jl. Dogol No.8, RT.11/RW.4, Kuningan, Karet Kuningan, Kecamatan Setiabudi, Kota Jakarta Selatan, Daerah Khusus Ibukota Jakarta 12940, Indonesia', 'expired', '75000', 'Nsjsk@gmail.com', '837489293843', 'Ubd3760052db6ec2cf33b5a98cee36de1');
COMMIT;

-- ----------------------------
-- Table structure for shipping
-- ----------------------------
DROP TABLE IF EXISTS `shipping`;
CREATE TABLE `shipping` (
  `id_shipping` varchar(20) NOT NULL,
  `id_currier` varchar(20) NOT NULL,
  `id_order` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `receiver` varchar(255) NOT NULL,
  `receivedate` datetime NOT NULL,
  PRIMARY KEY (`id_shipping`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shipping
-- ----------------------------
BEGIN;
INSERT INTO `shipping` VALUES ('15002', '32', 'OTTVUWAX', 'done', '2018-08-30 02:27:43', 'fifi', '2018-08-30 02:28:08');
COMMIT;

-- ----------------------------
-- Table structure for tracker
-- ----------------------------
DROP TABLE IF EXISTS `tracker`;
CREATE TABLE `tracker` (
  `id_order` varchar(20) NOT NULL,
  `datetime` datetime NOT NULL,
  `status` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id_order`,`status`,`description`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of tracker
-- ----------------------------
BEGIN;
INSERT INTO `tracker` VALUES ('4P1BJIJ5', '2018-08-30 13:22:02', 'capture', 'credit_card');
INSERT INTO `tracker` VALUES ('4P1BJIJ5', '2018-08-30 13:16:06', 'waiting payment', '');
INSERT INTO `tracker` VALUES ('OTTVUWAX', '2018-08-30 02:27:11', 'capture', 'credit_card');
INSERT INTO `tracker` VALUES ('OTTVUWAX', '2018-08-30 02:28:38', 'delivered', '');
INSERT INTO `tracker` VALUES ('OTTVUWAX', '2018-08-30 02:27:43', 'on delivery', '32');
INSERT INTO `tracker` VALUES ('OTTVUWAX', '2018-08-30 02:26:20', 'waiting payment', '');
INSERT INTO `tracker` VALUES ('U6MZY8W9', '2018-08-30 13:35:37', 'waiting payment', '');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
