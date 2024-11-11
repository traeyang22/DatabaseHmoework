CREATE TABLE `store`(
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `store_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods`(
  `goods_id` int NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` float(10,2) DEFAULT NULL,
  `monthly_sales_volume` int NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY(`goods_id`),
  CONSTRAINT `fk_goods_store_id` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user`(
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `age` int DEFAULT '0',
  PRIMARY KEY(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods_order`(
  `order_id` int NOT NULL AUTO_INCREMENT,
  `store_id` int NOT NULL,
  `goods_id` int NOT NULL,
  `user_id` int NOT NULL,
  `pay_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_status` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tracking_num` int DEFAULT '0',
  PRIMARY KEY(`order_id`),
  CONSTRAINT `fk_goods_order_store_id` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_goods_order_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods`(`goods_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_goods_order_user_id` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入商家信息
INSERT INTO `store` (`store_name`, `store_type`) VALUES
('科技先锋', '电子产品'),
('潮流服饰', '服装'),
('新鲜果蔬', '食品杂货'),
('知行书店', '书籍'),
('家居优选', '家居用品');

-- 插入用户信息
INSERT INTO `user` (`user_name`, `gender`, `age`) VALUES
('小红', '女', 25),
('小明', '男', 30),
('小刚', '男', 35),
('小丽', '女', 28),
('小美', '女', 40),
('小强', '男', 33),
('小芳', '女', 27),
('小华', '男', 45),
('小玉', '女', 29),
('小杰', '男', 36);

-- 插入商品信息
INSERT INTO `goods` (`goods_name`, `price`, `monthly_sales_volume`, `store_id`) VALUES
('笔记本电脑', 9999.99, 50, 1),
('智能手机', 6999.99, 120, 1),
('耳机', 199.99, 80, 1),
('T恤', 99.99, 150, 2),
('牛仔裤', 199.99, 100, 2),
('外套', 399.99, 75, 2),
('苹果', 4.99, 200, 3),
('香蕉', 2.99, 180, 3),
('牛奶', 8.99, 160, 3),
('小说', 49.99, 45, 4),
('烹饪书', 89.99, 30, 4),
('词典', 59.99, 20, 4),
('搅拌机', 299.99, 60, 5),
('咖啡机', 699.99, 40, 5),
('吸尘器', 999.99, 25, 5);

-- 插入订单信息
INSERT INTO `goods_order` (`store_id`, `goods_id`, `user_id`, `pay_type`, `order_status`, `tracking_num`) VALUES
(1, 1, 1, '信用卡', '已发货', 38456123),
(1, 2, 2, '支付宝', '已送达', 48932567),
(1, 3, 3, '信用卡', '待处理', 23647895),
(2, 4, 4, '现金', '已取消', 79481526),
(2, 5, 5, '信用卡', '已发货', 51237894),
(2, 6, 6, '支付宝', '已送达', 64321789),
(3, 7, 7, '信用卡', '待处理', 92561483),
(3, 8, 8, '现金', '已发货', 23894657),
(3, 9, 9, '信用卡', '已送达', 14795326),
(4, 10, 10, '支付宝', '已取消', 53928741),
(4, 11, 1, '现金', '已发货', 87126345),
(4, 12, 2, '信用卡', '已送达', 62187459),
(5, 13, 3, '支付宝', '待处理', 78341265),
(5, 14, 4, '信用卡', '已发货', 93416782),
(5, 15, 5, '现金', '已送达', 42678359),
(1, 1, 6, '支付宝', '已取消', 78315462),
(1, 2, 7, '信用卡', '已发货', 32817654),
(1, 3, 8, '现金', '已送达', 49178325),
(2, 4, 9, '信用卡', '待处理', 67214389),
(2, 5, 10, '支付宝', '已取消', 28936147),
(3, 7, 1, '信用卡', '已发货', 57234896),
(3, 8, 2, '现金', '已送达', 98347615),
(4, 11, 3, '支付宝', '已取消', 13984752),
(5, 13, 4, '信用卡', '已发货', 42785613),
(5, 15, 5, '现金', '已送达', 35892471);
