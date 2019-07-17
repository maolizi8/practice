/*
Navicat MySQL Data Transfer
Date: 2019-07-17 09:40:25
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_ui_businessmodule`
-- ----------------------------
DROP TABLE IF EXISTS `auto_ui_businessmodule`;
CREATE TABLE `auto_ui_businessmodule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '业务模块名称',
  `other_name` varchar(100) DEFAULT NULL,
  `platform` int(2) NOT NULL COMMENT '1-A，2-B',
  `collection` int(10) DEFAULT NULL,
  `sub_package` int(2) NOT NULL DEFAULT '0' COMMENT '是否属于子包：0-否，1-是',
  `py_package` varchar(255) DEFAULT NULL COMMENT '包，以点号连接',
  `py_project` int(2) DEFAULT NULL COMMENT '项目，查看ui项目表',
  `run_env` int(2) DEFAULT NULL COMMENT '0-测试环境，1-预发布环境，2-生产环境，3-其他工具类',
  `ui_sys` int(2) DEFAULT NULL COMMENT '0-web端，1-Android-APP端，2-IOS-APP端，3-http接口，4-dubbo',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auto_ui_businessmodule
-- ----------------------------
INSERT INTO `auto_ui_businessmodule` VALUES ('1', '首页', null, '1', '1', '0', null, null, null, null);
INSERT INTO `auto_ui_businessmodule` VALUES ('2', '进货单', null, '1', '1', '0', null, null, null, null);
INSERT INTO `auto_ui_businessmodule` VALUES ('3', '个人中心', null, '2', '12', '1', 'regressioncase.UserCenter', '4', '0', '1');
