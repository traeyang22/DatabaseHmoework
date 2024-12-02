CREATE TABLE `store`(
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `store_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods`(
  `goods_id` int NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` DOUBLE(10, 2) NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY(`goods_id`),
  CONSTRAINT `fk_goods_store_id` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `user`(
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` ENUM('男', '女') NOT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods_order`(
  `goods_order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pay_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_consumption` DOUBLE(10, 2) DEFAULT NULL,
  PRIMARY KEY(`goods_order_id`),
  CONSTRAINT `fk_goods_order_user_id` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `order_details`(
  `order_details_id` int NOT NULL AUTO_INCREMENT,
  `goods_order_id` int NOT NULL,
  `goods_id` int NOT NULL,
  `price` DOUBLE(10, 2) NOT NULL,
  `quantity` int DEFAULT NULL,
  `order_status` ENUM('已付款', '已发货', '已送达','已取消') NOT NULL,
  `tracking_num` VARCHAR(50) DEFAULT NULL,
  PRIMARY KEY(`order_details_id`),
  CONSTRAINT `fk_order_details_goods_order_id` FOREIGN KEY (`goods_order_id`) REFERENCES `goods_order`(`goods_order_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_details_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `goods`(`goods_id`) ON DELETE CASCADE
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
INSERT INTO `goods` (`goods_name`, `category`, `price`, `store_id`) VALUES
('笔记本电脑', '电子产品', 9999.99, 1),
('智能手机', '电子产品', 6999.99, 1),
('耳机', '电子产品', 199.99, 1),
('T恤', '服装', 99.99, 2),
('牛仔裤', '服装', 199.99, 2),
('外套', '服装', 399.99, 2),
('苹果', '食品杂货', 4.99, 3),
('香蕉', '食品杂货', 2.99, 3),
('牛奶', '食品杂货', 8.99, 3),
('小说', '书籍', 49.99, 4),
('烹饪书', '书籍', 89.99, 4),
('词典', '书籍', 59.99, 4),
('搅拌机', '家居用品', 299.99, 5),
('咖啡机', '家居用品', 699.99, 5),
('吸尘器', '家居用品', 999.99, 5);

-- 插入订单信息
INSERT INTO `goods_order` (`user_id`, `pay_type`, `total_consumption`) VALUES
(1, '银行卡', 5999.98),
(2, '支付宝', 1999.95),
(3, '微信支付', 990.80),
(4, '银行卡', 2399.95),
(5, '支付宝', 1799.95),
(6, '微信支付', 2899.95),
(7, '银行卡', 2499.97),
(8, '支付宝', 1799.94),
(9, '微信支付', 2900.90),
(10, '银行卡', 2499.97);

-- 插入订单详细信息
INSERT INTO `order_details` (`goods_order_id`, `goods_id`, `price`, `quantity`, `order_status`, `tracking_num`) VALUES
(1, 1, 9999.99, 1, '已付款', ''),
(2, 4, 99.99, 2, '已发货', '91324857'),(2, 5, 199.99, 2, '已发货', '91324857'),
(3, 7, 4.99, 30, '已送达', '60219485'),(3, 8, 2.99, 20, '已送达', '60219485'),
(4, 1, 9999.99, 1, '已付款', ''),(4, 3, 199.99, 2, '已付款', ''),
(5, 5, 199.99, 3, '已发货', '27405816'),(5, 6, 399.99, 1, '已发货', '27405816'),
(6, 1, 9999.99, 1, '已送达', '75930241'),(6, 2, 6999.99, 1, '已送达', '75930241'),(6, 7, 4.99, 1, '已送达', '75930241'),
(7, 4, 99.99, 3, '已付款', ''),(7, 5, 199.99, 2, '已付款', ''),
(8, 1, 9999.99, 1, '已发货', '48620317'),(8, 10, 49.99, 2, '已发货', '48620317'),
(9, 7, 4.99, 50, '已送达', '35904128'),(9, 10, 49.99, 30, '已送达', '35904128'),
(10, 1, 9999.99, 2, '已付款', ''),(10, 3, 199.99, 3, '已付款', '');