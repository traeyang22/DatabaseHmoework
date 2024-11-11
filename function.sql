-- DROP PROCEDURE IF EXISTS add_order;

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

    INSERT INTO goods_order (order_id, store_id, goods_id, user_id, pay_type, order_status)
    VALUES (orderID, storeID, goodID, userID, pay, 'Pending');

    UPDATE goods
    SET monthly_sales_volume = monthly_sales_volume + (price * 1)
    WHERE store_id = storeID
    AND goods_id = goodID;

    COMMIT;

    SELECT 'Add order successfully' AS result;

END$$
DELIMITER ;