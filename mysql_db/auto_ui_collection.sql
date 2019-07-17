/*
Navicat MySQL Data Transfer

Source Server         : yyw-0345
Source Server Version : 50717
Source Host           : yyw-0345:3306
Source Database       : qateam

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-07-17 09:40:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_ui_collection`
-- ----------------------------
DROP TABLE IF EXISTS `auto_ui_collection`;
CREATE TABLE `auto_ui_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(50) DEFAULT NULL,
  `py_path` varchar(255) DEFAULT NULL COMMENT '相对于项目的路径',
  `py_package` varchar(255) NOT NULL COMMENT '包，以点号连接',
  `py_project` int(2) NOT NULL COMMENT '项目，查看ui项目表',
  `sub_package` int(2) NOT NULL DEFAULT '0' COMMENT '包内含子包，0-无，1-有',
  `run_env` int(2) NOT NULL DEFAULT '0' COMMENT '0-测试环境，1-预发布环境，2-生产环境，3-其他工具类',
  `platform` int(2) DEFAULT NULL COMMENT '1-A,2-B',
  `ui_sys` int(2) NOT NULL DEFAULT '0' COMMENT '0-web端，1-Android-APP端，2-IOS-APP端，3-http接口，4-dubbo',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auto_ui_collection
-- ----------------------------
INSERT INTO `auto_ui_collection` VALUES ('1', 'PC端', '', null, 'prdenv_case.b2b_pc', '1', '0', '2', '1', '0');
INSERT INTO `auto_ui_collection` VALUES ('2', 'H5端', null, null, 'prdenv_case.b2b_h5', '1', '0', '2', '1', '0');
INSERT INTO `auto_ui_collection` VALUES ('3', 'Android', null, null, 'prdenv_case', '2', '0', '2', '1', '1');
INSERT INTO `auto_ui_collection` VALUES ('4', 'IOS', null, null, 'prdenv_case.b2c_pc', '3', '0', '2', '2', '2');
