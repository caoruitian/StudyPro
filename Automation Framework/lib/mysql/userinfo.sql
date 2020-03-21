/*
Navicat MySQL Data Transfer

Source Server         : 虚拟机
Source Server Version : 50726
Source Host           : 192.168.1.104:3306
Source Database       : testwork

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2019-07-03 23:36:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `userinfo`
-- ----------------------------
DROP TABLE IF EXISTS `userinfo`;
CREATE TABLE `userinfo` (
  `id` int(6) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `nickname` varchar(16) DEFAULT NULL,
  `describe` varchar(16) DEFAULT NULL,
  `account` char(16) NOT NULL,
  `pwd` char(16) NOT NULL COMMENT '账号密码',
  PRIMARY KEY (`id`,`account`),
  UNIQUE KEY `account` (`account`) USING BTREE,
  UNIQUE KEY `nicheng` (`nickname`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of userinfo
-- ----------------------------
INSERT INTO `userinfo` VALUES ('000001', '阿斯顿', '啊大苏打', 'dafeimao', 'dafeimao');
INSERT INTO `userinfo` VALUES ('000002', '大肥猫', '大肥猫', 'qwerty', 'qwerty');
INSERT INTO `userinfo` VALUES ('000003', '本届世界杯', '来咯啊哥', 'tims', 'tims');
INSERT INTO `userinfo` VALUES ('000004', 'Vincy', '', 'Vincy', 'qinyayuan0209');
INSERT INTO `userinfo` VALUES ('000012', 'asd', 'asd', 'Crtims123', '123456');
INSERT INTO `userinfo` VALUES ('000013', 'fdsa', 'fsd', 'Crtims1234', '123456');
