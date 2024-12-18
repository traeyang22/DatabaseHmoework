DELIMITER $$
-- 创建用户函数
-- 传入userName, gender, age参数
CREATE PROCEDURE add_user(
    IN userName VARCHAR(50),
    IN userGender ENUM('男', '女'),
    IN userAge INT
    -- OUT userID INT
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Add user failed. user name: ', userName, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @userName = userName;
    SET @userGender = userGender;
    SET @userAge = userAge;
    SET @userID = NULL;

    -- name为字符串，为防止sql注入，使用预处理语句
    PREPARE addUser FROM '
    INSERT INTO user (user_name, gender, age)
    VALUES (?,?,?);';

    -- 执行插入语句
    EXECUTE addUser USING @userName, @userGender, @userAge;
    -- 清理预处理语句
    DROP PREPARE addUser;

    COMMIT;

    -- 获取新用户ID
    SELECT LAST_INSERT_ID() INTO @userID;

    SELECT CONCAT('Add user successfully. user name: ', userName, ', user ID: ', @userID) AS result;
END$$
DELIMITER ;


DELIMITER $$
-- 修改用户的性别和年龄函数
-- 传入userID, userName, gender, age参数
CREATE PROCEDURE editUserInfo(
    IN userID INT,
    IN userName VARCHAR(50),
    IN userGender ENUM('男', '女'),
    IN userAge INT
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Edit user failed. user id: ', userID, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @userID = userID;

    -- 分别修改用户名、性别、年龄
    -- name为字符串，为防止sql注入，使用预处理语句
    IF userName IS NOT NULL THEN
        SET @userName = userName;

        PREPARE editUserName FROM '
        UPDATE user SET
        user_name = ?
        WHERE user_id = ?;
        ';

        EXECUTE editUserName USING @userName, @userID;
        DROP PREPARE editUserName;
    END IF;

    IF userGender IS NOT NULL THEN
        UPDATE user SET
        gender = userGender
        WHERE user_id = userID;
    END IF;

    IF userAge IS NOT NULL THEN
        UPDATE user SET
        age = userAge
        WHERE user_id = userID;
    END IF;

    COMMIT;

    SELECT CONCAT('Edit user successfully. user ID: ', userID,
                  ', user name: ', IFNULL(userName, '未更改'),
                  ', gender: ', IFNULL(userGender, '未更改'),
                  ', age: ', IFNULL(userAge, '未更改'), '.') AS result;
END$$
DELIMITER ;


DELIMITER $$
-- 创建商店函数
-- 传入storeName, storeType参数
CREATE PROCEDURE add_store(
    IN storeName varchar(50),
    IN storeType varchar(50)
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Add store failed. store name: ', storeName, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @storeName = storeName;
    SET @storeType = storeType;
    SET @storeID = NULL;

    -- 参数为字符串，为防止sql注入，使用预处理语句
    PREPARE addStore FROM '
    INSERT INTO store (store_name, store_type)
    VALUES (?,?);';

    -- 执行插入语句
    EXECUTE addStore USING @storeName, @storeType;
    -- 清理预处理语句
    DROP PREPARE addStore;

    COMMIT;

    -- 获取新用户ID
    SELECT LAST_INSERT_ID() INTO @storeID;

    SELECT CONCAT('Add store successfully. store name: ', storeName, ', store ID: ', @storeID) AS result;
END$$
DELIMITER ;


DELIMITER $$
-- 删除商店函数
-- 传入storeID参数
CREATE PROCEDURE del_store(
    IN storeID INT
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('delete store failed. store ide: ', storeID, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    DELETE FROM store WHERE store_id = storeID;
    DELETE FROM goods WHERE store_id = storeID;

    COMMIT;

    SELECT CONCAT('Delete store successfully.  store ID: ', storeID) AS result;
END$$
DELIMITER ;



DELIMITER $$
-- 修改商店名字、商店类型
-- 传入storeId, storeName, storeType参数
CREATE PROCEDURE editStoreInfo(
    IN storeId INT,
    IN storeName varchar(50),
    IN storeType varchar(50)
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Edit store failed. store id: ',storeId, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @storeId = storeId;

    -- 参数为字符串，为防止sql注入，使用预处理语句
    IF storeName IS NOT NULL THEN
        SET @storeName = storeName;

        PREPARE editStoreName FROM '
        UPDATE store SET
        store_name = ?
        WHERE store_id = ?;
        ';

        EXECUTE editStoreName USING @storeName, @storeId;
        DROP PREPARE editStoreName;
    END IF;

    IF storeType IS NOT NULL THEN
        SET @storeType = storeType;

        PREPARE editStoreType FROM '
        UPDATE store SET
        store_type = ?
        WHERE store_id = ?;
        ';

        EXECUTE editStoreType USING @storeType, @storeId;
        DROP PREPARE editStoreType;
    END IF;

    COMMIT;

    SELECT CONCAT('Edit store successfully. store ID: ', storeId,
                  ', store name: ', IFNULL(storeName, '未更改'),
                  ', store type: ', IFNULL(storeType, '未更改'), '.') AS result;
END$$
DELIMITER ;


DELIMITER $$
-- 创建商品函数
-- 传入goodName, goodType， goodPrice, storeId参数
CREATE PROCEDURE add_good(
  `goodName` varchar(50),
  `goodType` varchar(50),
  `goodPrice` DOUBLE(10, 2),
  `storeId` INT
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Add good failed. good name: ', goodName, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @goodName = goodName;
    SET @goodType = goodType;
    SET @goodPrice = goodPrice;
    SET @storeID = storeId;
    SET @goodID = NULL;

    -- 参数为字符串，为防止sql注入，使用预处理语句
    PREPARE addGood FROM '
    INSERT INTO goods (goods_name, category, price, store_id)
    VALUES (?,?,?,?);';

    -- 执行插入语句
    EXECUTE addGood USING @goodName, @goodType, @goodPrice, @storeID;
    -- 清理预处理语句
    DROP PREPARE addGood;

    COMMIT;

    -- 获取新用户ID
    SELECT LAST_INSERT_ID() INTO @goodID;

    SELECT CONCAT('Add good successfully. good name: ', goodName, ', good ID: ', @goodID) AS result;
END$$
DELIMITER ;

DELIMITER $$
-- 修改商品名字、商品类型、商品价格
-- 传入goodId, storeName, storeType， goodPrice参数
CREATE PROCEDURE edit_good_info(
    `goodId` INT,
    `goodName` varchar(50),
    `goodType` varchar(50),
    `goodPrice` DOUBLE(10, 2)
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('Edit good failed. good id: ',goodId, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @goodId = goodId;

    -- 参数为字符串，为防止sql注入，使用预处理语句
    IF goodName IS NOT NULL THEN
        SET @goodName = goodName;

        PREPARE editGoodName FROM '
        UPDATE goods SET
        goods_name = ?
        WHERE goods_id = ?;
        ';

        EXECUTE editGoodName USING @goodName, @goodId;
        DROP PREPARE editGoodName;
    END IF;

    IF goodType IS NOT NULL THEN
        SET @goodType = goodType;

        PREPARE editGoodType FROM '
        UPDATE goods SET
        category = ?
        WHERE goods_id = ?;
        ';

        EXECUTE editGoodType USING @goodType, @goodId;
        DROP PREPARE editGoodType;
    END IF;

    IF goodPrice IS NOT NULL THEN
        UPDATE goods SET
        price = goodPrice
        WHERE goods_id = goodId;
    END IF;

    COMMIT;

    SELECT CONCAT('Edit good successfully. good ID: ', goodId,
                  ', good name: ', IFNULL(goodName, '未更改'),
                  ', good type: ', IFNULL(goodType, '未更改'),
                  ', good price: ', IFNULL(goodPrice, '未更改'), '.') AS result;
END$$
DELIMITER ;



-- 订单类
DELIMITER $$
-- 创建订单详情函数
-- 传入orderId、goodId、goodNum参数
CREATE PROCEDURE add_order_good(
  IN `orderId` INT,
  IN `goodId` INT,
  IN `goodNum` INT
)

BEGIN
    SET @goodPrice = NULL;
    SET @goodStatus = '已付款';

    SELECT price INTO @goodPrice FROM goods WHERE goods_id = goodId;

    INSERT INTO order_details (goods_order_id, goods_id, price, quantity, order_status)
    VALUES (orderId, goodId, @goodPrice, goodNum, @goodStatus);

    SELECT CONCAT('Add good successfully.') AS result;
END$$
DELIMITER ;

DELIMITER $$
-- 删除订单函数
-- 传入OrderId参数
CREATE PROCEDURE del_order(
    `OrderId` INT
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- 回滚事务
        SELECT CONCAT('delete order failed. order id: ',OrderId, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    DELETE FROM order_details WHERE goods_order_id = OrderId;
    DELETE FROM goods_order WHERE goods_order_id = OrderId;

    COMMIT;

    SELECT CONCAT('delete order successfully. order ID: ', OrderId, '.') AS result;
END$$
DELIMITER ;


DELIMITER $$
-- 触发器。当订单详情添加数据时候，订单总价会自动更新
CREATE TRIGGER update_total_quantity_after_insert
AFTER INSERT ON order_details
FOR EACH ROW
BEGIN
    UPDATE goods_order
    SET total_consumption = total_consumption + NEW.price * NEW.quantity
    WHERE goods_order_id = NEW.goods_order_id;
END$$
DELIMITER ;


DELIMITER $$
-- 触发器。当订单状态更新为已取消或从已取消状态修改为其他状态时，订单总价会自动更新
CREATE TRIGGER update_total_quantity_after_status_update
AFTER UPDATE ON order_details
FOR EACH ROW
BEGIN
    -- 订单状态更新为已取消时候，订单总价减少
    IF NEW.order_status = '已取消' AND OLD.order_status <> '已取消' THEN
        UPDATE goods_order
        SET total_consumption = total_consumption - NEW.price * NEW.quantity
        WHERE goods_order_id = NEW.goods_order_id;
    END IF;

    -- 订单状态从已取消状态修改为其他状态时候，订单总价增加
    IF NEW.order_status <> '已取消' AND OLD.order_status = '已取消' THEN
        UPDATE goods_order
        SET total_consumption = total_consumption + NEW.price * NEW.quantity
        WHERE goods_order_id = NEW.goods_order_id;
    END IF;
END$$
DELIMITER ;


/*
-- 删除函数
DROP PROCEDURE add_user;

 */