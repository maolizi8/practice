/*
Navicat MySQL Data Transfer

Date: 2019-07-17 18:04:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_jk_jobs`
-- ----------------------------
DROP TABLE IF EXISTS `auto_jk_jobs`;

CREATE TABLE `auto_jk_jobs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jk_name` varchar(100) NOT NULL,
  `jk_desc` varchar(500) NOT NULL,
  `jk_server` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8;
