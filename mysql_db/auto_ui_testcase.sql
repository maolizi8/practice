/*
Navicat MySQL Data Transfer

Date: 2019-07-17 09:40:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `auto_ui_testcase`
-- ----------------------------
DROP TABLE IF EXISTS `auto_ui_testcase`;
CREATE TABLE `auto_ui_testcase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `py_name` varchar(300) DEFAULT NULL COMMENT '用例在代码中的名字',
  `py_desc` varchar(255) NOT NULL COMMENT '用例功能描述',
  `py_module` varchar(255) NOT NULL COMMENT '用例在代码中模块名，以点号连接',
  `py_marks` varchar(255) DEFAULT NULL COMMENT 'pytest mark标记，多个以分号连接',
  `py_skip_reason` varchar(100) DEFAULT NULL,
  `py_file` varchar(255) DEFAULT NULL,
  `run_env` int(2) NOT NULL DEFAULT '0' COMMENT '0-测试环境，1-预发布环境，2-生产环境，3-其他工具类',
  `business_module` int(5) DEFAULT NULL COMMENT '所属模块，查看UI用例模块表',
  `collection` int(5) DEFAULT NULL COMMENT '所属集合，查看UI集合表',
  `platform` int(2) NOT NULL COMMENT '1-A，2-B',
  `tapd_id` varchar(10) DEFAULT NULL COMMENT 'tapd中用例id',
  `tapd_proj` varchar(10) DEFAULT NULL,
  `cart_order_oprs` int(2) DEFAULT '1' COMMENT '是否含购物车、订单操作，0-否，1-是',
  `is_parallel` int(2) DEFAULT '0' COMMENT '是否可并行运行，0-否，1-是',
  `estimate_time` float(10,2) DEFAULT NULL COMMENT '预估运行时间',
  `run_status` int(2) DEFAULT NULL COMMENT '当前运行状态',
  `update_version` bigint(14) DEFAULT NULL,
  `createtime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updatetime` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1395 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auto_ui_testcase
-- ----------------------------
INSERT INTO `auto_ui_testcase` VALUES ('1', 'prdenv_case/b2b_pc/quick_check/test_main_func.py :test_main_function2', '搜索、添加品进入购物车并删除', 'prdenv_case.b2b_pc.quick_check.test_main_func', 'prd_main', '', 'prdenv_case/b2b_pc/quick_check/test_main_func.py', '2', '0', '1', '1', '', '', '1', '0', null, null, '1563268707470', '2019-07-16 17:18:31', '2019-07-16 17:18:31');
INSERT INTO `auto_ui_testcase` VALUES ('2', 'prdenv_case/b2b_pc/special_case/test_search_with_keys.py :test_check_search_list_login', '登录状态搜索', 'prdenv_case.b2b_pc.special_case.test_search_with_keys', 'prd_b2bpc_serach_onlogin', '', 'prdenv_case/b2b_pc/special_case/test_search_with_keys.py', '2', '0', '1', '1', '', '', '1', '0', null, null, '1563268707470', '2019-07-16 17:18:31', '2019-07-16 17:18:31');'0', null, null, '1563270946351', '2019-07-16 17:55:52', '2019-07-16 17:55:52');
