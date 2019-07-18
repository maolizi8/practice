/*
Navicat MySQL Data Transfer

Date: 2019-07-17 18:07:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `uitest_collect`
-- ----------------------------
DROP TABLE IF EXISTS `uitest_collect`;
CREATE TABLE `uitest_collect` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `htmlhead` varchar(50) NOT NULL,
  `jk_jobname` varchar(50) NOT NULL,
  `jk_buildid` varchar(50) NOT NULL,
  `is_end` int(2) NOT NULL DEFAULT '0' COMMENT '集合是否运行结束：0-未结束，1-已结束',
  `fpath` varchar(100) DEFAULT NULL,
  `tests_count` int(11) DEFAULT NULL,
  `fail_total` int(11) NOT NULL DEFAULT '0',
  `pass_total` int(11) NOT NULL DEFAULT '0',
  `error_total` int(11) NOT NULL DEFAULT '0',
  `rerun_total` int(11) NOT NULL DEFAULT '0',
  `run_total` int(11) NOT NULL DEFAULT '0',
  `skip_total` int(11) NOT NULL DEFAULT '0',
  `duration` float(20,4) DEFAULT '0.0000',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of uitest_collect
-- ----------------------------

