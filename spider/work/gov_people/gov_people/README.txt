

mysql�������:
CREATE TABLE `gov_leaders` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `department` varchar(200) DEFAULT NULL COMMENT '��������',
  `position` varchar(100) DEFAULT NULL COMMENT '��ְ',
  `name` varchar(50) NOT NULL,
  `province` varchar(50) DEFAULT NULL COMMENT 'ʡ',
  `city` varchar(50) DEFAULT NULL COMMENT '��',
  `people_url` varchar(200) DEFAULT NULL COMMENT '������ҳ',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '����ʱ��',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

