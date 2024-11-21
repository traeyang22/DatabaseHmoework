import mysql.connector

class Database:
    # 数据库类
    # 这里主要实现数据库的基本操作 如连接数据库、获取数据库中的表名、字段信息

    def __init__(self, database_name):
        self.db = database_name  # 数据库名称
        # 连接数据库
        self.dbconn = None  # 初始化dbconn变量，防止无法连接时候执行__del__方法报错
        try:
            self.dbconn = mysql.connector.connect(
                host="192.168.196.153",  # 数据库主机地址
                port="3306",  # 数据库端口号
                user="root",  # 数据库用户名
                passwd="123456",  # 数据库密码
                database=self.db,
                # auth_plugin="mysql_native_password"
            )
        except:
            print("Error: Failed to connect to database.")
            exit()
        print("Connected to database.")

        # 创建游标
        self.cursor = self.dbconn.cursor()
        # 定义变量table_list和table_dict，分别存储数据库中的表名和字段信息
        self.table_list = self.updateTables()
        self.table_dict = {table[0]: [] for table in self.table_list}
        # table_dict={表名：[(字段名称1，数据类型，是否允许为空，默认值，额外信息), (字段名称2，数据类型，是否允许为空，默认值，额外信息),...]}
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
        # if self.dbconn.is_connected():
        #     # self.cursor.close()
        if self.dbconn is not None:
            self.dbconn.close()

class DianshangDatabase(Database):
    # 电商数据库类，继承自Database类
    # 这里主要实现电商数据库相关的操作，如添加订单、更新订单状态、完成订单等

    def __init__(self, database_name):
        super().__init__(database_name)
        # 定义变量user_dict，用于存储用户信息
        # {id: {'storeName': str, 'storeType': str, 'goodsList': []}
        self.user_dict = self.queryUserInfo()
        self.store_dict = self.queryShopInfo()

    # 订单相关操作，包括添加订单、更新订单状态、完成订单、查询订单、退单等
    def addOrder(self, order):
        # 向订单表中添加订单信息
        pass

    def editOrderStatusFunc(self, order):
        # 创建一个sql函数，用于更新订单发货状态
        pass

    def finishOrderFunc(self, orderID: int):
        # 创建一个sql函数，用于更新订单完成状态
        pass

    def queryOrderFunc(self, orderID):
        # 创建一个sql函数，用于查询订单信息
        pass

    def refundOrderFunc(self, orderID):
        # 创建一个sql函数，用于退单
        pass


    # 商店相关操作，包括添加商店、更新商店信息、删除、查询商店信息等
    def addShop(self, shop: tuple[2]):
        # 向商店表中添加商店信息
        sql = "CALL add_store(%s, %s)"
        self.cursor.execute(sql, shop)
        res = self.cursor.fetchone()
        print(res)
        store_id = res[0].split(" ")[-1]
        return store_id

    def delShop(self, shop: int):
        # 向商店表中删除商店信息
        sql =f"DELETE FROM store WHERE store_id=%s;"
        self.cursor.execute(sql, (shop,))
        self.dbconn.commit()
        print(f"delete shop: {shop}")

    def editShopInfo(self, shop: int, name=None, shopType=None):
        # 创建一个sql函数，用于更新商店信息
        if name or shopType:
            sql = "CALL editStoreInfo(%s, %s, %s)"
            self.cursor.execute(sql, (shop, name, shopType))
            res = self.cursor.fetchone()
            # print(res)
            return res[0]
        return "Nothing to update."

    def queryShopInfo(self):
        # 查询实现：查询所有商店信息存入字典，在py端进行处理后返回给用户
        # 该函数为更新商店字典
        self.cursor.execute("SELECT * FROM store")
        res = self.cursor.fetchall()
        # print(res)
        self.store_dict = {store[0]: {"storeName": store[1], "storeType": store[2], "goodsList": self.__queryGoodsInfo(int(store[0]))} for store in res}
        return self.store_dict

    # 商品相关操作，包括添加商品、更新商品信息、查询商品信息等
    def addGood(self, good: tuple[4]):
        # 向商品表中添加商品信息
        sql = "CALL add_good(%s, %s, %s, %s)"
        self.cursor.execute(sql, good)
        res = self.cursor.fetchone()
        print(res)
        good_id = res[0].split(" ")[-1]
        return good_id

    def editGoodInfo(self, good: int, name=None, goodType=None, price=None):
        # 创建一个sql函数，用于更新商品信息
        if name or goodType or price:
            sql = "CALL edit_good_info(%s, %s, %s, %s)"
            self.cursor.execute(sql, (good, name, goodType, price))
            res = self.cursor.fetchone()
            print(res)
            return res[0]
        return "Nothing to update."

    def delGood(self, good: int):
        # 向商品表中删除商品信息
        sql =f"DELETE FROM goods WHERE goods_id=%s;"
        self.cursor.execute(sql, (good,))
        self.dbconn.commit()
        print(f"delete good: {good}")


    def __queryGoodsInfo(self, storeId: int):
        # 查询商品信息
        sql = "SELECT goods_id, goods_name, category, price FROM goods WHERE store_id=%s"
        self.cursor.execute(sql, (storeId,))
        res = self.cursor.fetchall()
        return res


    # 用户相关操作，包括添加用户、删除用户、更新用户信息、查询用户信息等
    def addUser(self, user: tuple[3]):
        # 向用户表中添加用户信息
        sql = "CALL add_user(%s, %s, %s)"
        self.cursor.execute(sql, user)
        res = self.cursor.fetchone()
        print(res)
        user_id = res[0].split(" ")[-1]
        return user_id

    def delUser(self, user: int):
        # 向用户表中删除用户信息
        sql =f"DELETE FROM user WHERE user_id=%s;"
        self.cursor.execute(sql, (user,))
        self.dbconn.commit()
        print(f"delete user: {user}")


    def editUserInfo(self, user_id: int, name=None, gender=None, age=None):
        # 向用户表中更新用户信息
        if name or gender or age:
            sql=f"CALL editUserInfo(%s, %s, %s, %s)"
            self.cursor.execute(sql, (user_id, name, gender, age))
            res = self.cursor.fetchone()
            # print(res)
            return res[0]
        return "Nothing to update."


    def __updataUserDict(self):
        # 查询实现：查询所有用户信息存入字典，在py端进行处理后返回给用户
        # 该函数为更新用户字典
        self.cursor.execute("SELECT * FROM user")
        res = self.cursor.fetchall()
        self.user_dict = {user[0]: user[1:] for user in res}
        return self.user_dict

    def queryUserInfo(self, user_id=None, name=None, gender=None, age=None):
        # 查询用户信息
        resList = []
        if user_id or name or gender or age:
            self.__updataUserDict()
            for key, value in self.user_dict.items():
                if user_id is not None and key != user_id:
                    continue
                if name is not None and value[0] != name:
                    continue
                if gender is not None and value[1] != gender:
                    continue
                if age is not None and value[2] != age:
                    continue
                resList.append((key,) + value)
        return resList



