/*
Navicat MySQL Data Transfer

Date: 2019-07-17 11:02:08
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `uitest_run_records_errors`
-- ----------------------------
DROP TABLE IF EXISTS `uitest_run_records_errors`;
CREATE TABLE `uitest_run_records_errors` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `jk_jobname` varchar(100) NOT NULL,
  `jk_buildid` varchar(50) NOT NULL,
  `test_name` varchar(200) NOT NULL,
  `test_path` varchar(200) DEFAULT NULL,
  `test_result` varchar(10) DEFAULT NULL COMMENT '测试用例状态：0-未开始，1-进行中，2-成功，3-失败，4-跳过，5-重跑',
  `test_desc` varchar(300) DEFAULT NULL,
  `test_phase` varchar(10) DEFAULT NULL COMMENT '测试阶段：setup，call，teardown',
  `test_duration` varchar(100) DEFAULT NULL,
  `test_log` mediumtext,
  `error_png` mediumtext COMMENT 'base64的图片',
  `error_link` varchar(600) DEFAULT NULL,
  `error_html` mediumtext,
  `error_driverlog` mediumtext,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `test_result` (`test_result`),
  KEY `errortestquery` (`test_name`,`jk_buildid`,`jk_jobname`,`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12578 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of uitest_run_records_errors
-- ----------------------------
