import mysql.connector
import subprocess
import time

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
        self.dbconn.start_transaction()
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

def auto_query(query_method_name):
    def decorator(method):
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            # # 备份数据库
            # self.backup()
            # 获取查询方法并调用
            query_method = getattr(self, query_method_name)
            query_method()
            return result
        return wrapper
    return decorator

class DianshangDatabase(Database):
    # 电商数据库类，继承自Database类
    # 这里主要实现电商数据库相关的操作，如添加订单、更新订单状态、完成订单等

    def __init__(self, database_name):
        super().__init__(database_name)
        # 定义变量user_dict，用于存储用户信息
        # {id: (name, sex, age)}
        self.user_dict = self.updataUserDict()
        # 定义变量store_dict，用于存储商店信息
        # {id: {'storeName': str,'storeType': str, 'goodsList': []}
        self.store_dict = self.updateShopInfo()
        # 定义变量order_dict，用于存储订单信息
        # {order_id: {'user_id': int, 'pay_type': str, 'total_consumption': float, 'goodsList': []}
        self.order_dict = self.updateOrder()

    def backup(self):
        # 获取当前时间并格式化为合法的文件名
        backup_file = time.strftime('%Y-%m-%d_%H-%M-%S') + '.sql'

        # 使用mysqldump命令进行备份
        command = f"mysqldump -u root -p --all-databases > {backup_file}"

        try:
            # 调用subprocess执行命令
            subprocess.run(command, shell=True, check=True)
            print(f"Backup completed successfully. File saved as {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error: Backup failed. {e}")

    def getPayType(self, id: int):
        # 获取用户的支付方式
        pay_dict = {1: "支付宝", 2: "微信支付", 3: "银行卡"}
        return pay_dict[id]

    # 订单相关操作，包括添加订单、获取订单状态、更新订单状态等
    @auto_query("updateOrder")
    def addOrder(self, user_id: int, pay_type: int, good_list: list[tuple]):
        # 向订单表中添加订单信息, 传入的good_list为[(商品id, 数量), (商品id, 数量),...]
        self.dbconn.commit()
        self.dbconn.start_transaction()
        try:
            sql = "INSERT INTO goods_order (user_id, pay_type, total_consumption) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (user_id, self.getPayType(pay_type), 0))
            order_id = self.cursor.lastrowid
            # print(f"add order: {order_id}")
            for good in good_list:
                self.cursor.callproc("add_order_good", [order_id, good[0], good[1]])
                res = self.cursor.stored_results()
                for r in res:
                    if "failed" in r.fetchone()[0]:
                        raise Exception("Failed to add good to order.")
            self.dbconn.commit()
            return order_id
        except:
            self.dbconn.rollback()
            print("Error: Failed to add order.")
            return None

    def getOrderStatus(self, num: int):
        # 获取订单状态
        status_dict = {1: '已付款', 2: '已发货', 3: '已送达', 4: '已取消'}
        return status_dict[num]

    @auto_query("updateOrder")
    def editOrderStatus(self, order: int, good: int, status: int, tracking_num: int=None):
        # 创建一个sql函数，用于更新订单状态
        if status not in [1, 2, 3, 4] or tracking_num is  None and status == 2:
            print("Error: Invalid status.")
            return False
        status = self.getOrderStatus(status)
        sql = "UPDATE order_details SET order_status=%s"
        sql += ", tracking_num=%s" if tracking_num is not None else ""
        sql += " WHERE goods_order_id=%s AND goods_id=%s"
        params = (status, tracking_num, order, good) if tracking_num is not None else (status, order, good)
        self.cursor.execute(sql, params)
        self.dbconn.commit()
        return True

    @auto_query("updateOrder")
    def delOrder(self, order: int):
        # 删除订单
        self.cursor.callproc("del_order", [order])
        res = self.cursor.stored_results()
        for r in res:
            r = r.fetchone()[0]
            print(r)
            if "successfully" in r:
                return True
        return False

    def updateOrder(self):
        # 创建一个sql函数，用于查询订单信息
        # 该函数为查询订单信息，并将结果存入字典，在py端进行处理后返回给用户
        self.cursor.execute("SELECT * FROM goods_order")
        res = self.cursor.fetchall()
        self.order_dict = {order[0]: {"user_id": order[1], "pay_type": order[2], "total_consumption": order[3], "goodsList": []} for order in res}
        self.updateOrderDetails()
        return self.order_dict

    def updateOrderDetails(self):
        # 更新订单详情表
        self.cursor.execute("SELECT * FROM order_details")
        res = self.cursor.fetchall()
        for detail in res:
            self.order_dict[detail[1]]["goodsList"].append((detail[2], detail[3], detail[4], detail[5], detail[6]))
        return self.order_dict

    def queryOrderInfo(self, order_id=None, user_id=None, pay_type=None, total_consumption=None, max_total_consumption=None, min_total_consumption=None):
        # 查询订单信息
        resDict = {}
        pay_type = self.getPayType(pay_type) if pay_type is not None else None
        if order_id or user_id or pay_type or total_consumption or max_total_consumption or min_total_consumption:
            self.updateOrder()
            for key, value in self.order_dict.items():
                if order_id is not None and key != order_id:
                    continue
                if user_id is not None and value["user_id"] != user_id:
                    continue
                if pay_type is not None and value["pay_type"] != pay_type:
                    continue
                if total_consumption is not None and value["total_consumption"] != total_consumption:
                    continue
                if max_total_consumption is not None and value["total_consumption"]  > max_total_consumption:
                    continue
                if min_total_consumption is not None and value["total_consumption"]  < min_total_consumption:
                    continue
                resDict[key] = value
        return resDict

    def queryOrderDetailInfo(self, order_id=None, good_id=None, order_status=None, tracking_num=None, price=None, max_price=None, min_price=None):
         # 查询订单详情信息
        resDict = {}
        if order_id or good_id or order_status or tracking_num or price or max_price or min_price:
            self.updateOrder()
            for key, value in self.order_dict.items():
                if order_id is not None and key != order_id:
                    continue
                for good in value["goodsList"]:
                    if good_id is not None and good[0] != good_id:
                        continue
                    if order_status is not None and good[3] != order_status:
                        continue
                    if tracking_num is not None and good[4] != tracking_num:
                        continue
                    if price is not None and good[1] != price:
                        continue
                    if max_price is not None and good[1] > max_price:
                        continue
                    if min_price is not None and good[1] < min_price:
                        continue
                    resDict[key] = {"order_id": key, "user_id": value["user_id"], "pay_type": value["pay_type"], "total_consumption": value["total_consumption"], "goodsList": [(good[0], good[1], good[2], good[3], good[4])] }
        return resDict


    # 商店相关操作，包括添加商店、更新商店信息、删除、查询商店信息等
    @auto_query("updateShopInfo")
    def addShop(self, shop: list[2]):
        # 向商店表中添加商店信息
        self.cursor.callproc("add_store", shop)
        res = self.cursor.stored_results()
        store_id =None
        for r in res:
            r = r.fetchone()[0]
            if "successfully" in r:
                store_id = r.split(" ")[-1]
        return store_id

    @auto_query("updateShopInfo")
    def delShop(self, shop: int):
        # 向商店表中删除商店信息
        self.cursor.callproc("del_store", [shop])
        res = self.cursor.stored_results()
        r = None
        for r in res:
            r = r.fetchone()[0]
        return r

    @auto_query("updateShopInfo")
    def editShopInfo(self, shop: int, name=None, shopType=None):
        # 创建一个sql函数，用于更新商店信息
        if name or shopType:
            self.cursor.callproc("editStoreInfo", [shop, name, shopType])
            res = self.cursor.stored_results()
            r = None
            for r in res:
                r = r.fetchone()[0]
            return r
        return "Nothing to update."

    def updateShopInfo(self):
        # 查询实现：查询所有商店信息存入字典，在py端进行处理后返回给用户
        # 该函数为更新商店字典
        self.cursor.execute("SELECT * FROM store")
        res = self.cursor.fetchall()
        # print(res)
        self.store_dict = {store[0]: {"storeName": store[1], "storeType": store[2], "goodsList": self.__updateGoodsInfo(int(store[0]))} for store in res}
        return self.store_dict

    def queryShopInfo(self, store_id=None, name=None, shopType=None):
        store_id = int(store_id) if store_id is not None else None
        # 查询商店信息
        resDict = {}
        if store_id or name or shopType:
            self.updateShopInfo()
            for key, value in self.store_dict.items():
                if store_id is not None and key != store_id:
                    continue
                if name is not None and value["storeName"] != name:
                    continue
                if shopType is not None and value["storeType"] != shopType:
                    continue
                resDict[key] = value
        return resDict

    # 商品相关操作，包括添加商品、更新商品信息、查询商品信息等
    @auto_query("updateShopInfo")
    def addGood(self, good: list[4]):
        # 向商品表中添加商品信息
        print(good)
        self.cursor.callproc("add_good", good)
        res = self.cursor.stored_results()
        good_id = None
        for r in res:
            r = r.fetchone()[0]
            print(r)
            if "successfully" in r:
                good_id = r.split(" ")[-1]
        return good_id

    @auto_query("updateShopInfo")
    def editGoodInfo(self, good: int, name=None, goodType=None, price=None):
        # 创建一个sql函数，用于更新商品信息
        if name or goodType or price:
            self.cursor.callproc("edit_good_info", [good, name, goodType, price])
            res = self.cursor.stored_results()
            r = None
            for r in res:
                r = r.fetchone()[0]
            return r
        return "Nothing to update."

    @auto_query("updateShopInfo")
    def delGood(self, good: int):
        # 向商品表中删除商品信息
        sql =f"DELETE FROM goods WHERE goods_id=%s;"
        self.cursor.execute(sql, (good,))
        self.dbconn.commit()
        print(f"delete good: {good}")


    def __updateGoodsInfo(self, storeId: int):
        # 查询商品信息
        sql = "SELECT goods_id, goods_name, category, price FROM goods WHERE store_id=%s"
        self.cursor.execute(sql, (storeId,))
        res = self.cursor.fetchall()
        return res

    def queryGoodInfo(self, good_id=None, name=None, category=None, price=None, store_id=None, max_price=None, min_price=None):
        good_id = int(good_id) if good_id is not None else None
        store_id = int(store_id) if store_id is not None else None
        price = float(price) if price is not None else None
        # 查询商品信息
        print(f"good_id: {good_id}, name: {name}, category: {category}, price: {price}, store_id: {store_id}, max_price: {max_price}, min_price: {min_price}")
        resDict = {}
        if store_id or good_id or name or category or price or max_price or min_price:
            self.updateShopInfo()
            for key, value in self.store_dict.items():
                for good in value["goodsList"]:
                    if store_id is not None and key != store_id:
                        continue
                    if good_id is not None and good[0] != good_id:
                        continue
                    if name is not None and good[1] != name:
                        continue
                    if category is not None and good[2] != category:
                        continue
                    if price is not None and good[3] != price:
                        continue
                    if max_price is not None and good[3] > max_price:
                        continue
                    if min_price is not None and good[3] < min_price:
                        continue
                    resDict[good[0]] = {"goodId": good[0], "goodName": good[1], "goodType": good[2], "price": good[3]}
        return resDict

    # 用户相关操作，包括添加用户、删除用户、更新用户信息、查询用户信息等
    @auto_query("updataUserDict")
    def addUser(self, user: list[3]):
        # 向用户表中添加用户信息
        self.cursor.callproc("add_user", user)
        res = self.cursor.stored_results()
        user_id = None
        for r in res:
            r = r.fetchone()[0]
            if "successfully" in r:
                user_id = r.split(" ")[-1]
        return user_id

    @auto_query("updataUserDict")
    def delUser(self, user: int):
        # 向用户表中删除用户信息
        sql =f"DELETE FROM user WHERE user_id=%s;"
        self.cursor.execute(sql, (user,))
        self.dbconn.commit()
        print(f"delete user: {user}")

    @auto_query("updataUserDict")
    def editUserInfo(self, user_id: int, name=None, gender=None, age=None):
        # 向用户表中更新用户信息
        if name or gender or age:
            self.cursor.callproc("editUserInfo", [user_id, name, gender, age])
            res = self.cursor.stored_results()
            r = None
            for r in res:
                r = r.fetchone()[0]
            return r
        return "Nothing to update."


    def updataUserDict(self):
        # 查询实现：查询所有用户信息存入字典，在py端进行处理后返回给用户
        # 该函数为更新用户字典
        self.cursor.execute("SELECT * FROM user")
        res = self.cursor.fetchall()
        self.user_dict = {user[0]: {"name": user[1], "sex": user[2], "age": user[3]} for user in res}
        return self.user_dict

    def queryUserInfo(self, user_id=None, name=None, gender=None, age=None):
        user_id = int(user_id) if user_id is not None else None
        age = int(age) if age is not None else None
        # 查询用户信息
        resDict = {}
        if user_id or name or gender or age:
            self.updataUserDict()
            for key, value in self.user_dict.items():
                if user_id is not None and key != user_id:
                    continue
                if name is not None and value["name"] != name:
                    continue
                if gender is not None and value["sex"] != gender:
                    continue
                if age is not None and value["age"] != age:
                    continue
                resDict[key] = value
        return resDict



