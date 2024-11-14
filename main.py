import mysql.connector

class Database:
    # 数据库类 连接数据库、获取数据库中的表名、字段信息
    def __init__(self, database_name):
        self.db = database_name  # 数据库名称
        # 连接数据库
        self.dbconn = mysql.connector.connect(
            host="127.0.0.1",  # 数据库主机地址
            port="3306",  # 数据库端口号
            user="root",  # 数据库用户名
            passwd="mysql",  # 数据库密码
            database=self.db,
        )
        # 创建游标
        self.cursor = self.dbconn.cursor()
        # 定义变量table_list和table_dict，分别存储数据库中的表名和字段信息
        self.table_list = self.updateTables()
        self.table_dict = {table[0]: [] for table in self.table_list}
        # table_dict={表名：[(字段名称，数据类型，是否允许为空，默认值，额外信息),...]}
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
            self.dbconn.close()

class DianshangDatabase(Database):
    # 电商数据库类，继承自Database类
    def __init__(self, database_name="test"):
        super(DianshangDatabase, self).__init__(database_name)

    # 增加数据功能
    def addUser(self, user_data):
        print("添加数据前：")
        self.queryData("user")  # 数据添加前查询
        self.cursor.execute("INSERT INTO user (user_name, gender, age) VALUES (%s, %s, %s)", user_data)
        self.dbconn.commit()
        print("用户添加成功！")
        print("添加数据后：")
        self.queryData("user")  # 数据添加后查询

    def addStore(self, store_data):
        print("添加数据前：")
        self.queryData("store")  # 数据添加前查询
        self.cursor.execute("INSERT INTO store (store_name, store_type) VALUES (%s, %s)", store_data)
        self.dbconn.commit()
        print("店铺添加成功！")
        print("添加数据后：")
        self.queryData("store")  # 数据添加后查询

    def addGoods(self, goods_data):
        print("添加数据前：")
        self.queryData("goods")  # 数据添加前查询
        self.cursor.execute("INSERT INTO goods (goods_name, category, price, monthly_sales_volume, store_id) VALUES (%s, %s, %s, %s, %s)", goods_data)
        self.dbconn.commit()
        print("商品添加成功！")
        print("添加数据后：")
        self.queryData("goods")  # 数据添加后查询

    def addOrder(self, order_data):
        print("添加数据前：")
        self.queryData("goods_order")  # 数据添加前查询
        self.cursor.execute("INSERT INTO goods_order (user_id, pay_type, total_consumption) VALUES (%s, %s, %s)", order_data)
        order_id = self.cursor.lastrowid
        self.dbconn.commit()
        print("订单添加成功！请继续添加订单详情。")
        print("添加数据后：")
        self.queryData("goods_order")  # 数据添加后查询
        return order_id

    def addOrderDetail(self, detail_data, order_id):
        print("添加数据前：")
        self.queryData("order_details")  # 数据添加前查询
        self.cursor.execute("INSERT INTO order_details (goods_order_id, store_id, goods_id, price, quantity, order_status, tracking_num) VALUES (%s, %s, %s, %s, %s, %s, %s)", detail_data)
        self.cursor.execute("UPDATE goods_order SET total_consumption = total_consumption + (%s * %s) WHERE goods_order_id = %s", (detail_data[3], detail_data[4], order_id))
        self.dbconn.commit()
        print("订单详情添加成功！订单总金额已更新。")
        print("添加数据后：")
        self.queryData("order_details")  # 数据添加后查询

    # 查询数据功能
    def queryData(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print(f"{table_name} 表中没有数据。")

    # 修改数据功能
    def updateData(self, table_name, update_sql, params):
        self.cursor.execute(update_sql, params)
        self.dbconn.commit()
        print(f"{table_name} 表数据更新成功。")

    # 删除数据功能
    def deleteData(self, table_name, delete_sql, params):
        self.cursor.execute(delete_sql, params)
        self.dbconn.commit()
        print(f"{table_name} 表数据删除成功。")

    def __del__(self):
        super(DianshangDatabase, self).__del__()

def main():
    db = DianshangDatabase()
    while True:
        print("\n请选择操作：")
        print("1. 查询数据")
        print("2. 增加数据")
        print("3. 删除数据")
        print("4. 修改数据")
        print("0. 退出")
        
        choice = input("请输入选择：")

        if choice == "1":
            print("请选择要查询的表：")
            print("1. 用户表")
            print("2. 店铺表")
            print("3. 商品表")
            print("4. 订单表")
            print("5. 订单详情表")
            
            # 使用数字输入选择对应的表名
            query_choice = input("请输入选择：")
            table_mapping = {
                "1": "user",
                "2": "store",
                "3": "goods",
                "4": "goods_order",
                "5": "order_details"
            }
            db.queryData(table_mapping.get(query_choice, "user"))

        elif choice == "2":
            print("请选择增加的类型：")
            print("1. 用户")
            print("2. 店铺")
            print("3. 商品")
            print("4. 订单")
            print("5. 订单详情")
            
            add_choice = input("请输入选择：")

            if add_choice == "1":
                user_data = (input("输入用户名："), input("输入性别（男/女）："), input("输入年龄："))
                db.addUser(user_data)
            elif add_choice == "2":
                store_data = (input("输入店铺名称："), input("输入店铺类型："))
                db.addStore(store_data)
            elif add_choice == "3":
                goods_data = (input("输入商品名称："), input("输入分类："), float(input("输入价格：")), int(input("输入月销量：")), int(input("输入店铺ID：")))
                db.addGoods(goods_data)
            elif add_choice == "4":
                order_data = (int(input("输入用户ID：")), input("输入支付类型："), 0.00)
                order_id = db.addOrder(order_data)
                while True:
                    detail_data = (order_id, int(input("输入店铺ID：")), int(input("输入商品ID：")), float(input("输入价格：")), int(input("输入数量：")), input("输入订单状态："), input("输入快递单号："))
                    db.addOrderDetail(detail_data, order_id)
                    if input("继续添加此订单的订单详情吗？(y/n): ").lower() != "y":
                        break
            elif add_choice == "5":
                order_id = int(input("输入所属订单ID："))
                detail_data = (order_id, int(input("输入店铺ID：")), int(input("输入商品ID：")), float(input("输入价格：")), int(input("输入数量：")), input("输入订单状态："), input("输入快递单号："))
                db.addOrderDetail(detail_data, order_id)

        elif choice == "3":
            table_name = input("请输入要删除数据的表名：")
            delete_sql = input("输入删除语句（例如：DELETE FROM 表名 WHERE 条件）：")
            params = tuple(input("输入参数，以逗号分隔：").split(","))
            db.deleteData(table_name, delete_sql, params)

        elif choice == "4":
            table_name = input("请输入要修改数据的表名：")
            update_sql = input("输入更新语句（例如：UPDATE 表名 SET 字段 = %s WHERE 条件）：")
            params = tuple(input("输入参数，以逗号分隔：").split(","))
            db.updateData(table_name, update_sql, params)

        elif choice == "0":
            print("退出程序")
            break
        else:
            print("无效选择，请重试！")

if __name__ == '__main__':
    main()
