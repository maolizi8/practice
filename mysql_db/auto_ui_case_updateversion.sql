/*
Navicat MySQL Data Transfer

Date: 2019-07-17 09:40:34
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_ui_case_updateversion`
-- ----------------------------
DROP TABLE IF EXISTS `auto_ui_case_updateversion`;
CREATE TABLE `auto_ui_case_updateversion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `update_version` bigint(14) NOT NULL,
  `proj_name` varchar(50) NOT NULL,
  `createtime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auto_ui_case_updateversion
-- ----------------------------
INSERT INTO `auto_ui_case_updateversion` VALUES ('1', '1563269181850', 'android_autotest', '2019-07-16 17:31:27', '2019-07-16 17:31:27');
INSERT INTO `auto_ui_case_updateversion` VALUES ('2', '1563268707470', 'webs_autotest', '2019-07-16 17:31:55', '2019-07-16 17:31:55');
