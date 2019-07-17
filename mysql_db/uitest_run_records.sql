/*
Navicat MySQL Data Transfer

Date: 2019-07-17 10:56:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `uitest_run_records`
-- ----------------------------
DROP TABLE IF EXISTS `uitest_run_records`;
CREATE TABLE `uitest_run_records` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `jk_jobname` varchar(100) NOT NULL,
  `jk_buildid` varchar(50) NOT NULL,
  `test_name` varchar(200) NOT NULL,
  `test_result` varchar(10) NOT NULL COMMENT '测试用例状态：0-未开始，1-进行中，2-成功，3-失败，4-跳过，5-重跑',
  `test_desc` varchar(300) DEFAULT NULL,
  `test_phase` varchar(10) DEFAULT NULL COMMENT '测试阶段：setup，call，teardown',
  `test_duration` float(15,4) DEFAULT NULL,
  `test_log` mediumtext,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `test_result` (`test_result`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of uitest_run_records
-- ----------------------------
