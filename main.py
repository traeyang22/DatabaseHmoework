import mysql.connector


class Database:
    # 数据库类 连接数据库、获取数据库中的表名、字段信息
    def __init__(self, database_name):
        self.db = database_name  # 数据库名称
        # 连接数据库
        self.dbconn = mysql.connector.connect(
            host="",  # 数据库主机地址
            port="",  # 数据库端口号
            user="",  # 数据库用户名
            passwd="",  # 数据库密码
            database=self.db,
            auth_plugin="mysql_native_password"
        )
        # 创建游标
        self.cursor = self.dbconn.cursor()
        # 定义变量table_list和table_dict，分别存储数据库中的表名和字段信息
        self.table_list = self.updateTables()
        self.table_dict = {table[0]: [] for table in self.table_list}
        # table_dict={表名：[(字段名称，数据类型，是否允许为空，默认值，额外信息), (字段名称，数据类型，是否允许为空，默认值，额外信息),...]}
        self.updateColumns()

    def updateTables(self):
        # 更新数据库中的表名
        self.cursor.execute("SHOW TABLES")
        self.table_list = self.cursor.fetchall()
        return self.table_list

    def updateColumns(self):
        self.updateTables()
        # 更新数据库中表的字段信息
        for table in self.table_list:
            self.cursor.execute(f"SHOW COLUMNS FROM {table[0]}")
            columns = self.cursor.fetchall()
            self.table_dict[table[0]] = columns

    def __del__(self):
        # 关闭数据库连接
        if self.dbconn.is_connected():
            # self.cursor.close()
            self.dbconn.close()


class DianshangDatabase(Database):
    # 电商数据库类，继承自Database类
    def __init__(self, database_name="test"):
        # 调用父类的构造函数
        super(DianshangDatabase, self).__init__(database_name)
        # 创建sql函数
        # self.__addOrderFunc()

#     def __addOrderFunc(self):
#         # 创建一个sql函数，用于向订单表中添加订单信息
#         # 首先删除之前创建的add_order函数
#         self.cursor.execute("DROP PROCEDURE IF EXISTS add_order;")
#         # 该函数需要传入订单ID、商品ID、店铺ID、用户ID、支付方式作为参数，并更新顾客表中的销售额  默认订单状态为Pending 默认购买数量为1
#         # 成功执行该函数后，返回'Transaction completed successfully'
#         # 失败执行该函数后，返回'Transaction failed and rolled back. Customer ID: {customer_id} caused an error.'
#         sql = """
# CREATE PROCEDURE add_order(
#     IN orderID INT,
#     IN storeID INT,
#     IN goodID INT,
#     IN userID INT,
#     IN pay VARCHAR(100)
# )
# BEGIN
#     DECLARE EXIT HANDLER FOR SQLEXCEPTION
#     BEGIN
#         ROLLBACK;
#         SELECT CONCAT('Add order failed and rolled back. Customer ID: ', userID, ' caused an error.') AS result;
#     END;
#
#     START TRANSACTION;
#
#     INSERT INTO goods_order (order_id, store_id, goods_id, user_id, pay_type, order_status)
#     VALUES (orderID, storeID, goodID, userID, pay, 'Pending');
#
#     UPDATE goods
#     SET monthly_sales_volume = monthly_sales_volume + (price * 1)
#     WHERE store_id = storeID
#     AND goods_id = goodID;
#
#     COMMIT;
#
#     SELECT 'Add order successfully' AS result;
# END;"""
#         self.cursor.execute(sql)
#
    def addOrder(self, order):
        # 向订单表中添加订单信息
        if isinstance(order, tuple) and len(order) == 5:
            print(f"CALL add_order{order};")
            self.cursor.execute(f"CALL add_order{order};")
            return self.cursor.fetchone()
        return ("Error: Invalid order format.",)

    def changerOrderStatusFunc(self):
        # 创建一个sql函数，用于更新订单状态
        pass

    def __del__(self):
        # # 删掉add_order函数
        # self.cursor.execute("DROP PROCEDURE IF EXISTS add_order;")
        # 调用父类的析构函数
        super(DianshangDatabase, self).__del__()


if __name__ == '__main__':
    db = DianshangDatabase()
    data = (28, 1, 1, 1, 'alipay')
    print(db.addOrder(data))
    # db.cursor.execute("SELECT * FROM goods_order;")
    # print(db.cursor.fetchall())
    # db.updateColumns()
    # print(db.table_dict)
    # print(db.table_dict['customer'])
    # print(db.table_dict['customer_order'])
    # db.cursor.execute("DROP PROCEDURE IF EXISTS add_order;")
    # db.cursor.execute("DROP PROCEDURE IF EXISTS add_order;")
    # db.addOrderFunc()
    # print(db.addOrder(('Laptop', 1000.00, 1, 6)))
    # print(db.getTables())
    # print(db.getColumns("customer"))
