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




/*
-- 删除函数
DROP PROCEDURE add_user;
DROP PREPARE addUser;
 */