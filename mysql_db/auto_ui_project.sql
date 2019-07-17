/*
Navicat MySQL Data Transfer

Source Server         : yyw-0345
Source Server Version : 50717
Source Host           : yyw-0345:3306
Source Database       : qateam

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2019-07-17 09:40:46
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_ui_project`
-- ----------------------------
DROP TABLE IF EXISTS `auto_ui_project`;
CREATE TABLE `auto_ui_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `repo_name` varchar(100) NOT NULL,
  `repo_path` varchar(255) DEFAULT NULL,
  `root_dir` varchar(255) DEFAULT NULL,
  `server_ip` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auto_ui_project
-- ----------------------------
INSERT INTO `auto_ui_project` VALUES ('1', 'webs_autotest', 'test-autotest', null, 'E:/test-autotest/webs_autotest', '');
INSERT INTO `auto_ui_project` VALUES ('2', 'android_autotest', 'test-autotest', null, 'E:/test-autotest/android_autotest', '');
INSERT INTO `auto_ui_project` VALUES ('3', 'ios_autotest', 'test-androidapp', null, 'E:/test-androidapp/ios_autotest', '');
