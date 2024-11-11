DELIMITER $$
-- 创建订单 传入订单ID、商品ID、店铺ID、用户ID、支付方式作为参数，并更新顾客表中的销售额  默认订单状态为Pending 默认购买数量为1
CREATE PROCEDURE add_order(
    IN orderID INT,
    IN storeID INT,
    IN goodID INT,
    IN userID INT,
    IN pay VARCHAR(100)
)

BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT CONCAT('Add order failed and rolled back. Customer ID: ', userID, ' caused an error.') AS result;
    END;

    START TRANSACTION;

    SET @orderStatus = 'Pending';
    SEt @orderID = orderID;
    SET @storeID = storeID;
    SET @goodID = goodID;
    SET @userID = userID;
    SET @payType = pay;

    -- 创建订单的预编译语句
    PREPARE addOrder FROM '
    INSERT INTO goods_order (order_id, store_id, goods_id, user_id, pay_type, order_status)
    VALUES (?, ?, ?, ?, ?, ?);';

    -- 更新顾客表中的销售预编译语句
    PREPARE updateCustomerSales FROM '
    UPDATE goods
    SET monthly_sales_volume = monthly_sales_volume + (price * 1)
    WHERE store_id = ?
    AND goods_id = ?;';

    -- 插入订单数据
    EXECUTE addOrder USING @orderID, @storeID, @goodID, @userID, @payType, @orderStatus;

    -- 更新顾客表中的销售额
    EXECUTE updateCustomerSales USING @storeID, @goodID;

    -- 释放预编译语句
    DROP PREPARE addOrder;
    DROP PREPARE updateCustomerSales;

    COMMIT;

    SELECT 'Add order successfully' AS result;

END$$
DELIMITER ;


/*
-- 删除函数
# DROP PROCEDURE add_order;
 */