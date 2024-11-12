CREATE TABLE `store`(
  `store_id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `store_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods`(
  `goods_id` int NOT NULL AUTO_INCREMENT,
  `goods_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `category` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` DECIMAL(10, 2) DEFAULT NULL,
  `monthly_sales_volume` int NOT NULL,
  `store_id` int NOT NULL,
  PRIMARY KEY(`goods_id`),
  CONSTRAINT `fk_goods_store_id` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `user`(
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `gender` ENUM('男', '女') NOT NULL,
  `age` int DEFAULT NULL, 
  PRIMARY KEY(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `goods_order`(
  `goods_order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pay_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_status` ENUM('已付款', '已发货', '已送达') NOT NULL,
  `tracking_num` VARCHAR(50) DEFAULT NULL,
  `total_consumption` DECIMAL(10, 2) DEFAULT NULL,
  PRIMARY KEY(`goods_order_id`),
  CONSTRAINT `fk_goods_order_user_id` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `order_details`(
  `order_details_id` int NOT NULL AUTO_INCREMENT,
  `goods_order_id` int NOT NULL,
  `store_id` int NOT NULL,
  `goods_id` int NOT NULL,
  `price` DECIMAL(10, 2) DEFAULT NULL,
  `quantity` int DEFAULT NULL, 
  PRIMARY KEY(`order_details_id`),
  CONSTRAINT `fk_order_details_goods_order_id` FOREIGN KEY (`goods_order_id`) REFERENCES `goods_order`(`goods_order_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_order_details_store_id` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`) ON DELETE CASCADE,
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
INSERT INTO `goods` (`goods_name`, `category`, `price`, `monthly_sales_volume`, `store_id`) VALUES
('笔记本电脑', '电子产品', 9999.99, 50, 1),
('智能手机', '电子产品', 6999.99, 120, 1),
('耳机', '电子产品', 199.99, 80, 1),
('T恤', '服装', 99.99, 150, 2),
('牛仔裤', '服装', 199.99, 100, 2),
('外套', '服装', 399.99, 75, 2),
('苹果', '食品杂货', 4.99, 200, 3),
('香蕉', '食品杂货', 2.99, 180, 3),
('牛奶', '食品杂货', 8.99, 160, 3),
('小说', '书籍', 49.99, 45, 4),
('烹饪书', '书籍', 89.99, 30, 4),
('词典', '书籍', 59.99, 20, 4),
('搅拌机', '家居用品', 299.99, 60, 5),
('咖啡机', '家居用品', 699.99, 40, 5),
('吸尘器', '家居用品', 999.99, 25, 5);

-- 插入订单信息
INSERT INTO `goods_order` (`user_id`, `pay_type`, `order_status`, `tracking_num`, `total_consumption`) VALUES
(1, '信用卡', '已付款', '45857245', 1560.00),
(2, '支付宝', '已发货', '91324857', 980.50),
(3, '微信支付', '已送达', '60219485', 620.20),
(4, '信用卡', '已付款', '81390572', 330.10),
(5, '支付宝', '已发货', '27405816', 450.30),
(6, '微信支付', '已送达', '75930241', 750.75),
(7, '信用卡', '已付款', '16593827', 1200.00),
(8, '支付宝', '已发货', '48620317', 890.90),
(9, '微信支付', '已送达', '35904128', 640.20),
(10, '信用卡', '已付款', '29504738', 1050.10),
(11, '支付宝', '已发货', '48750291', 950.50),
(12, '微信支付', '已送达', '85037294', 300.30),
(13, '信用卡', '已付款', '90314752', 720.25),
(14, '支付宝', '已发货', '67520139', 1300.10),
(15, '微信支付', '已送达', '92058431', 420.90),
(16, '信用卡', '已付款', '34750862', 620.80),
(17, '支付宝', '已发货', '15873920', 780.00),
(18, '微信支付', '已送达', '97215084', 560.40),
(19, '信用卡', '已付款', '45720913', 1110.70),
(20, '支付宝', '已发货', '86572094', 670.60);


INSERT INTO `order_details` (`goods_order_id`, `store_id`, `goods_id`, `price`, `number`) VALUES
(1, 1, 1, 999.99, 2), (1, 1, 2, 199.99, 1),
(2, 2, 4, 99.99, 3), (2, 2, 5, 199.99, 2),
(3, 3, 7, 4.99, 10), (3, 3, 8, 2.99, 20), (3, 3, 9, 8.99, 5),
(4, 4, 10, 49.99, 2), (4, 4, 12, 59.99, 3),
(5, 5, 13, 299.99, 1), (5, 5, 14, 699.99, 1),
(6, 1, 1, 999.99, 1), (6, 1, 3, 199.99, 4),
(7, 2, 5, 199.99, 3), (7, 2, 6, 399.99, 1),
(8, 3, 7, 4.99, 30), (8, 3, 9, 8.99, 5),
(9, 4, 10, 49.99, 4), (9, 4, 11, 89.99, 1),
(10, 5, 13, 299.99, 2), (10, 5, 15, 999.99, 1),
(11, 1, 2, 199.99, 5), (11, 1, 3, 199.99, 1),
(12, 2, 5, 199.99, 2), (12, 2, 6, 399.99, 1),
(13, 3, 7, 4.99, 15), (13, 3, 8, 2.99, 25),
(14, 4, 11, 89.99, 3), (14, 4, 12, 59.99, 2),
(15, 5, 13, 299.99, 1), (15, 5, 15, 999.99, 1),
(16, 1, 1, 999.99, 2), (16, 1, 2, 199.99, 1),
(17, 2, 4, 99.99, 4), (17, 2, 5, 199.99, 2),
(18, 3, 8, 2.99, 30), (18, 3, 9, 8.99, 10),
(19, 4, 10, 49.99, 2), (19, 4, 12, 59.99, 4),
(20, 5, 13, 299.99, 1), (20, 5, 15, 999.99, 1);
