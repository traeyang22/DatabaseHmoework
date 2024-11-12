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

    def addOrder(self, order):
        # 向订单表中添加订单信息
        if isinstance(order, tuple) and len(order) == 5:
            print(f"CALL add_order{order};")
            self.cursor.execute(f"CALL add_order{order};")
            return self.cursor.fetchone()
        return ("Error: Invalid order format.",)

    def editOrderStatusFunc(self, order):
        # 创建一个sql函数，用于更新订单发货状态
        if isinstance(order, tuple) and len(order) == 2:
            print(f"CALL edit_order{order};")
            self.cursor.execute(f"CALL edit_order{order};")
            return self.cursor.fetchone()
        return ("Error: Invalid order format.",)

    def finishOrderFunc(self, orderID):
        # 创建一个sql函数，用于更新订单完成状态
        if isinstance(orderID, int):
            print(f"CALL finish_order({orderID});")
            self.cursor.execute(f"CALL finish_order({orderID});")
            return self.cursor.fetchone()
        return ("Error: Invalid order format.",)

    def __del__(self):
        # # 删掉add_order函数
        # self.cursor.execute("DROP PROCEDURE IF EXISTS add_order;")
        # 调用父类的析构函数
        super(DianshangDatabase, self).__del__()


if __name__ == '__main__':
    db = DianshangDatabase()
    # data = (100, 1, 1, 1, 'alipay')
    # print(db.addOrder(data))
    # data = (101, 164513)
    # print(db.editOrderStatusFunc(data))
    # data = 100
    # print(db.finishOrderFunc(data))
