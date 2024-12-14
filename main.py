import re
import os
import tkinter as tk
from tkinter import ttk, mainloop,messagebox
from pprint import pprint
import subprocess
import time

from sqlclass import DianshangDatabase


# 用户名规则
def checkUsername(username):
    # 用户名需要满足 6-16 位，只能包含字母、数字、下划线
    match = r"^[\w_]{6,16}$"
    if not re.match(match, username):
        return False
    return True

# 创建菜单栏
def createMenu():
    # 菜单栏
    menuTables = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="数据表", menu=menuTables)
    menuTables.add_command(label="用户表", command=lambda: showData(sql.user_dict, ["id", "name", "gender", "age"], True))
    menuTables.add_command(label="商店表", command=lambda: showData(sql.store_dict, ["id", "name", "shopType"], True))
    # menuTables.add_command(label="商店表", command=lambda: showData(sql.store_dict, ["id", "name", "shopType", "goodsList"], True))
    menuTables.add_command(label="商品表", command=lambda: showData(sql.store_dict, ["shopId", "goodId", "name", "goodType", "price"], False))
    menuTables.add_command(label="订单表", command=lambda: showData(sql.order_dict, ["id", "userId", "p+ay", "total"], True))
    menuTables.add_command(label="订单详情表", command=lambda: showData(sql.order_dict, ["orderId", "goodId","price", "number", "status", "trackingNumber"], False))

    # menuQuery = tk.Menu(top, tearoff=0, font=("Arial", 10))
    # top.add_cascade(label="查询", menu=menuQuery)
    # menuQuery.add_command(label="用户信息", command=test)
    # menuQuery.add_command(label="订单信息", command=test)
    # menuQuery.add_command(label="商店及商品信息", command=test)

    menuUser = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="用户管理", menu=menuUser)
    menuUser.add_command(label="添加用户", command=lambda: userInput(1))
    menuUser.add_command(label="删除用户", command=lambda: userInput(2))
    menuUser.add_command(label="修改用户信息", command=lambda: userInput(3))
    menuUser.add_command(label="查询用户信息", command=lambda: userInput(4))

    menuShop = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="商店管理", menu=menuShop)
    menuShop.add_command(label="添加商店", command=lambda: shopInput(1))
    menuShop.add_command(label="删除商店", command=lambda: shopInput(2))
    menuShop.add_command(label="修改商店信息", command=lambda: shopInput(3))
    menuShop.add_command(label="查询商店信息", command=lambda: shopInput(4))

    menuGood = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="商品管理", menu=menuGood)
    menuGood.add_command(label="添加商品", command=lambda: goodInput(1))
    menuGood.add_command(label="删除商品", command=lambda: goodInput(2))
    menuGood.add_command(label="修改商品信息", command=lambda: goodInput(3))
    menuGood.add_command(label="查询商品信息", command=lambda: goodInput(4))

    menuOrder = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="订单管理", menu=menuOrder)
    menuOrder.add_command(label="添加订单", command=lambda: orderInput(1))
    menuOrder.add_command(label="删除订单", command=lambda: orderInput(2))
    menuOrder.add_command(label="订单详情状态更新", command=lambda: orderInput(3))
    menuOrder.add_command(label="查询订单信息", command=lambda: orderInput(4))
    menuOrder.add_command(label="查询订单详情信息", command=lambda: orderInput(5))

    menubackup = tk.Menu(top, tearoff=0, font=("Arial", 10))
    top.add_cascade(label="备份", menu=menubackup)
    menubackup.add_command(label="备份数据库", command=backup)
    menubackup.add_command(label="退出", command=root.quit)

def adjust_column_widths(tree):
    l = 0
    lList = []

    # 遍历每一列
    for col in tree['columns']:
        max_len = len(col)  # 初始值为列标题长度

        # 计算每列中最大项的长度
        for item in tree.get_children(''):
            cell_value = tree.item(item)['values'][tree['columns'].index(col)]
            if isinstance(cell_value, str):
                max_len = max(max_len, len(cell_value))

        # 设置列宽（加上一些额外的空间）
        extra_space = 20
        lList.append((max_len + extra_space) * 8)
        l += lList[-1]
        tree.column(col, width=lList[-1])  # 每个字符大约占用8像素

    l = (1500 - l) // len(tree['columns'])

    # 增加宽度使其能够固定总宽
    for c in range(len(tree['columns'])):
        tree.column(tree['columns'][c], width=lList[c] + l)

def backup():
    db_user = "root"  # 替换为你的用户名
    db_password = "mysql"  # 替换为你的密码
    db_name = "test"  # 替换为你的数据库名
    backup_file = time.strftime('%Y-%m-%d_%H-%M-%S') + '.sql'  # 备份文件路径

    command = f"mysqldump -u{db_user} -p{db_password} {db_name} > {backup_file}"

    try:
        # 执行备份命令
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("成功", f"备份成功！文件保存为 {os.path.abspath(backup_file)}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("错误", f"备份失败！错误信息：{e}")

def showData(data: dict, key: list, isSelf=True):
    # 清理之前的表格内容
    for widget in frame_left.winfo_children():
        widget.destroy()

    # 数据展示区
    tree = ttk.Treeview(frame_left, columns=key, show="headings", height=20)
    ttk.Style().configure("Treeview", font=("Arial", 15), rowheight=30)

    # 表头
    for col in key:
        tree.heading(col, text=col.title())
        tree.column(col, anchor=tk.CENTER)

    # 表格内容
    if isSelf:
        for key, value in data.items():
            # row_data = [key] + [value[k] for k in value if k != "goodsList"]
            row_data = [key] + [value[k] for k in value]
            tree.insert('', 'end', values=row_data)
    else:
        for key, value in data.items():
            for good in value["goodsList"]:
                row_data = [key] + [*good]
                tree.insert('', 'end', values=row_data)

    # 调整列宽
    adjust_column_widths(tree)

    # 将表格放置在窗口中
    tree.place(x=0, y=0, width=frame_left.winfo_width(), height=600)  # 设置高度为600像素

def userInput(s=0):
    inputWindow = tk.Toplevel(root)
    inputWindow.geometry("300x400")
    inputWindow.title("用户管理")

    if s != 2:
        # 用户名输入框
        username_label = tk.Label(inputWindow, text="用户名：")
        username_label.pack(side="top", padx=10, pady=10)
        username_entry = tk.Entry(inputWindow)
        username_entry.pack(side="top", padx=10, pady=10)
        # 性别选择框
        gender_label = tk.Label(inputWindow, text="性别：")
        gender_label.pack(side="top", padx=10, pady=10)
        gender_var = tk.StringVar()
        if s != 1:
            gender_var.set("None")
            gender_menu = tk.OptionMenu(inputWindow, gender_var, "男", "女", "None")
        else:
            gender_var.set("男")
            gender_menu = tk.OptionMenu(inputWindow, gender_var, "男", "女")
        gender_menu.pack(side="top", padx=10, pady=10)
        # 年龄输入框
        age_label = tk.Label(inputWindow, text="年龄：")
        age_label.pack(side="top", padx=10, pady=10)
        age_entry = tk.Entry(inputWindow)
        age_entry.pack(side="top", padx=10, pady=10)
    if s != 1:
        # id
        id_label = tk.Label(inputWindow, text="id：")
        id_label.pack(side="top", padx=10, pady=10)
        id_entry = tk.Entry(inputWindow)
        id_entry.pack(side="top", padx=10, pady=10)

    # 确定按钮
    def addUser():
        username = username_entry.get()
        gender = gender_var.get()
        age = age_entry.get()
        if username and gender and age:
            sql.addUser([username, gender, age])
            inputWindow.destroy()
            showData(sql.user_dict, ["id", "name", "gender", "age"], True)

    def delUser():
        userId = int(id_entry.get())
        sql.delUser(userId)
        inputWindow.destroy()
        showData(sql.user_dict, ["id", "name", "gender", "age"], True)

    def editUser():
        userId = int(id_entry.get())
        name = username_entry.get() if username_entry.get() else None
        gender = gender_var.get()
        age = age_entry.get() if age_entry.get() else None
        sql.editUserInfo(userId, name=name, gender=gender, age=age)
        inputWindow.destroy()
        showData(sql.user_dict, ["id", "name", "gender", "age"], True)

    def queryUser():
        userId = int(id_entry.get()) if id_entry.get() else None
        name = username_entry.get() if username_entry.get() else None
        gender = gender_var.get() if gender_var.get() != "None" else None
        age = age_entry.get() if age_entry.get() else None
        result = sql.queryUserInfo(user_id=userId, name=name, gender=gender, age=age)
        showData(result, ["id", "name", "gender", "age"], True)

    fun_dict = {
        1: addUser,
        2: delUser,
        3: editUser,
        4: queryUser
    }
    add_button = tk.Button(inputWindow, text="确定", command=fun_dict[s])
    add_button.pack(side="bottom", padx=10, pady=10)

def shopInput(s):
    inputWindow = tk.Toplevel(root)
    inputWindow.geometry("300x400")
    inputWindow.title("商店管理")

    if s != 2:
        # 商店名称输入框
        name_label = tk.Label(inputWindow, text="商店名称：")
        name_label.pack(side="top", padx=10, pady=10)
        name_entry = tk.Entry(inputWindow)
        name_entry.pack(side="top", padx=10, pady=10)

        # 商店类型选择框
        type_label = tk.Label(inputWindow, text="商店类型：")
        type_label.pack(side="top", padx=10, pady=10)
        type_var = tk.StringVar()
        if s != 1:
            type_var.set("None")
            type_menu = tk.OptionMenu(inputWindow, type_var, "家居用品", "服装鞋包", "美妆护肤", "数码产品", "母婴用品",
                                      "图书音像", "运动户外", "其他", "None")
        else:
            type_var.set("家居用品")
            type_menu = tk.OptionMenu(inputWindow, type_var, "家居用品", "服装鞋包", "美妆护肤", "数码产品", "母婴用品",
                                      "图书音像", "运动户外", "其他")
        type_menu.pack(side="top", padx=10, pady=10)

    if s != 1:
        id_label = tk.Label(inputWindow, text="id：")
        id_label.pack(side="top", padx=10, pady=10)
        id_entry = tk.Entry(inputWindow)
        id_entry.pack(side="top", padx=10, pady=10)

    # 确定按钮
    def addShop():
        name = name_entry.get()
        shopType = type_var.get()
        if name and shopType:
            sql.addShop([name, shopType])
            inputWindow.destroy()
            showData(sql.store_dict, ["id", "name", "shopType"], True)

    def delShop():
        shopId = int(id_entry.get())
        sql.delShop(shopId)
        inputWindow.destroy()
        showData(sql.store_dict, ["id", "name", "shopType"], True)

    def editShop():
        shopId = int(id_entry.get())
        name = name_entry.get() if name_entry.get() else None
        shopType = type_var.get() if type_var.get() != "None" else None
        sql.editShopInfo(shopId, name=name, shopType=shopType)
        inputWindow.destroy()
        showData(sql.store_dict, ["id", "name", "shopType"], True)

    def queryShop():
        shopId = int(id_entry.get()) if id_entry.get() else None
        name = name_entry.get() if name_entry.get() else None
        shopType = type_var.get() if type_var.get() != "None" else None
        result = sql.queryShopInfo(store_id=shopId, name=name, shopType=shopType)
        showData(result, ["id", "name", "shopType"], True)

    fun_dict = {
        1: addShop,
        2: delShop,
        3: editShop,
        4: queryShop
    }
    add_button = tk.Button(inputWindow, text="确定", command=fun_dict[s])
    add_button.pack(side="bottom", padx=10, pady=10)

def goodInput(s):
    inputWindow = tk.Toplevel(root)
    inputWindow.geometry("300x500")  # 设置窗口大小
    inputWindow.title("商品管理")

    if s != 2:
        # 商品名称输入框
        name_label = tk.Label(inputWindow, text="商品名称：")
        name_label.pack(side="top", padx=10, pady=10)
        name_entry = tk.Entry(inputWindow)
        name_entry.pack(side="top", padx=10, pady=10)

        # 商店类型选择框
        type_label = tk.Label(inputWindow, text="商品类型：")
        type_label.pack(side="top", padx=10, pady=10)
        type_var = tk.StringVar()
        if s != 1:
            type_var.set("None")
            type_menu = tk.OptionMenu(inputWindow, type_var, "电子产品", "服装", "食品杂货", "书籍", "家居用品", "None")
        else:
            type_var.set("手机")
            type_menu = tk.OptionMenu(inputWindow, type_var, "电子产品", "服装", "食品杂货", "书籍", "家居用品")
        type_menu.pack(side="top", padx=10, pady=10)

        # 商品价格输入框
        price_label = tk.Label(inputWindow, text="商品价格：")
        price_label.pack(side="top", padx=10, pady=10)
        price_entry = tk.Entry(inputWindow)
        price_entry.pack(side="top", padx=10, pady=10)

        # 商店id
        store_label = tk.Label(inputWindow, text="商店id：")
        store_label.pack(side="top", padx=10, pady=10)
        store_entry = tk.Entry(inputWindow)
        store_entry.pack(side="top", padx=10, pady=10)

    if s != 1:
        id_label = tk.Label(inputWindow, text="id：")
        id_label.pack(side="top", padx=10, pady=10)
        id_entry = tk.Entry(inputWindow)
        id_entry.pack(side="top", padx=10, pady=10)

    def addGood():   # 添加商品
        name = name_entry.get()
        goodType = type_var.get()
        storeId = int(store_entry.get())
        price = float(price_entry.get())
        if name and goodType and storeId:
            sql.addGood([name, goodType, price, storeId])
            inputWindow.destroy()
            showData(sql.store_dict, ["shopId", "goodId", "name", "goodType", "price"], False)

    def delGood():
        goodId = int(id_entry.get())
        sql.delGood(goodId)
        inputWindow.destroy()
        showData(sql.store_dict, ["shopId", "goodId", "name", "goodType", "price"], False)

    def editGood():
        goodId = int(id_entry.get())
        name = name_entry.get() if name_entry.get() else None
        goodType = type_var.get() if type_var.get() != "None" else None
        sql.editGoodInfo(goodId, name=name, goodType=goodType)
        inputWindow.destroy()
        showData(sql.store_dict, ["shopId", "goodId", "name", "goodType", "price"], False)

    def queryGood():
        goodId = int(id_entry.get()) if id_entry.get() else None
        name = name_entry.get() if name_entry.get() else None
        goodType = type_var.get() if type_var.get() != "None" else None
        storeId = int(store_entry.get()) if store_entry.get() else None
        if price_entry.get() and "-" in price_entry.get():
            price = price_entry.get().split("-")
            minprice = float(price[0])
            maxprice = float(price[1])
            result = sql.queryGoodInfo(good_id=goodId, name=name, category=goodType, min_price=minprice, max_price=maxprice, store_id=storeId)
        else:
            price = float(price_entry.get()) if price_entry.get() else None
            result = sql.queryGoodInfo(good_id=goodId, name=name, category=goodType, price=price, store_id=storeId)
        showData(result, ["shopId", "goodId", "name", "goodType", "price"], True)

    fun_dict = {
        1: addGood,
        2: delGood,
        3: editGood,
        4: queryGood
    }
    add_button = tk.Button(inputWindow, text="确定", command=fun_dict[s])
    add_button.pack(side="bottom", padx=10, pady=10)

def orderInput(s):
    h = 400 if s != 2 else 200
    h = 500 if s == 5 else h
    w = 400
    goods_data = []
    inputWindow = tk.Toplevel(root)
    inputWindow.geometry(f"{w}x{h}")  # 设置窗口大小
    inputWindow.title("订单管理")


    if s != 1:
        # order_id输入框
        oid_label = tk.Label(inputWindow, text="订单id：")
        oid_label.pack(side="top", padx=10, pady=10)
        oid_entry = tk.Entry(inputWindow)
        oid_entry.pack(side="top", padx=10, pady=10)

    if s == 1 or s == 4:
        # user_id输入框
        user_label = tk.Label(inputWindow, text="用户id：")
        user_label.pack(side="top", padx=10, pady=10)
        user_entry = tk.Entry(inputWindow)
        user_entry.pack(side="top", padx=10, pady=10)

        pay_dict = {
            "支付宝": 1,
            "微信支付": 2,
            "银行卡": 3
        }

        # 支付方式选择框
        type_label = tk.Label(inputWindow, text="商品类型：")
        type_label.pack(side="top", padx=10, pady=10)
        type_var = tk.StringVar()
        if s == 1:
            type_var.set("微信支付")
            type_menu = tk.OptionMenu(inputWindow, type_var, "银行卡", "微信支付", "支付宝")
        else:
            type_var.set("None")
            type_menu = tk.OptionMenu(inputWindow, type_var, "银行卡", "微信支付", "支付宝", "None")
        type_menu.pack(side="top", padx=10, pady=10)

        if s == 1:
            def add_good():
                nonlocal h, w, goods_data
                if h > 900:
                    return
                good_frame = tk.Frame(goods_frame)
                good_frame.pack(side="top", padx=10, pady=10)
                goodID_label = tk.Label(good_frame, text="商品id")
                goodID_label.pack(side="left", padx=10, pady=10)
                goodID_entry = tk.Entry(good_frame, width=10)
                goodID_entry.pack(side="left", padx=10, pady=10)
                goodNum_label = tk.Label(good_frame, text="商品数量")
                goodNum_label.pack(side="left", padx=10, pady=10)
                goodNum_entry = tk.Entry(good_frame, width=10)
                goodNum_entry.pack(side="left", padx=10, pady=10)
                inputWindow.geometry(f"{w}x{h}")

                # 将输入框存储到列表中
                goods_data.append((goodID_entry, goodNum_entry))
                h += 60

            # 多个商品id及其数量输入框
            goods_frame = tk.Frame(inputWindow)
            goods_frame.pack(side="top", padx=10, pady=10)

            add_button = tk.Button(goods_frame, text="添加商品输入", command=add_good)
            add_button.pack(side="bottom", padx=10, pady=10)



    if s == 3 or s == 5:
        status_dict = {"已付款": 1, "已发货": 2, "已送达": 3, "已取消": 4}
        # 商品id
        gid_label = tk.Label(inputWindow, text="商品id：")
        gid_label.pack(side="top", padx=10, pady=10)
        gid_entry = tk.Entry(inputWindow)
        gid_entry.pack(side="top", padx=10, pady=10)

        state_label = tk.Label(inputWindow, text="商品状态：")
        state_label.pack(side="top", padx=10, pady=10)
        state_var = tk.StringVar()
        if s == 3:
            state_var.set("已付款")
            state_menu = tk.OptionMenu(inputWindow, state_var, "已付款", "已发货", "已送达", "已取消")
        else:
            state_var.set("None")
            state_menu = tk.OptionMenu(inputWindow, state_var, "已付款", "已发货", "已送达", "已取消", "None")
        state_menu.pack(side="top", padx=10, pady=10)

        tracking_num_label = tk.Label(inputWindow, text="快递单号：")
        tracking_num_label.pack(side="top", padx=10, pady=10)
        tracking_num_entry = tk.Entry(inputWindow)
        tracking_num_entry.pack(side="top", padx=10, pady=10)

    if s == 5 or s == 4:
        plabel = tk.Label(inputWindow, text="价格：")
        plabel.pack(side="top", padx=10, pady=10)
        pentry = tk.Entry(inputWindow)
        pentry.pack(side="top", padx=10, pady=10)

    def addOrder():
        # 收集所有商品的 ID 和数量
        goods_info = []
        user = int(user_entry.get())
        pay = pay_dict[type_var.get()]
        for goodID_entry, goodNum_entry in goods_data:
            goodID = goodID_entry.get()
            goodNum = goodNum_entry.get()
            if goodID and goodNum:
                goods_info.append((int(goodID), int(goodNum)))
        sql.addOrder(user, pay, goods_info)
        showData(sql.order_dict, ["orderId", "userId", "payType", "status"], True)

    def delOrder():
        orderId = int(oid_entry.get())
        sql.delOrder(orderId)
        showData(sql.order_dict, ["orderId", "userId", "payType", "status"], True)

    def editOrder():
        order = int(oid_entry.get())
        good = int(gid_entry.get())
        state = status_dict[state_var.get()]
        tracking_num = int(tracking_num_entry.get()) if state == 2 else None
        sql.editOrderStatus(order, good, state, tracking_num)
        showData(sql.order_dict, ["orderId", "goodId","price", "number", "status", "trackingNumber"], False)

    def queryOrder():
        orderId = int(oid_entry.get()) if oid_entry.get() else None
        user = int(user_entry.get()) if user_entry.get() else None
        pay = pay_dict[type_var.get()] if type_var.get() != "None" else None
        if pentry.get() and "-" in pentry.get():
            total = pentry.get().split("-")
            min_total = float(total[0])
            max_total = float(total[1])
            res = sql.queryOrderInfo(order_id=orderId, user_id=user, pay_type=pay, max_total_consumption=max_total, min_total_consumption=min_total)
        elif pentry.get():
            total = float(pentry.get())
            res = sql.queryOrderInfo(order_id=orderId, user_id=user, pay_type=pay, total_consumption=total)
        else:
            res = sql.queryOrderInfo(order_id=orderId, user_id=user, pay_type=pay)
        showData(res, ["orderId", "userId", "payType", "total"], True)

    def queryOrderDetail():
        orderId = int(oid_entry.get()) if oid_entry.get() else None
        good = int(gid_entry.get()) if gid_entry.get() else None
        state = status_dict[state_var.get()] if state_var.get() != "None" else None
        tracking_num = tracking_num_entry.get() if tracking_num_entry.get() else None
        if pentry.get() and "-" in pentry.get():
            price = pentry.get().split("-")
            min_price = float(price[0])
            max_price = float(price[1])
            res = sql.queryOrderDetailInfo(order_id=orderId, good_id=good, order_status=state, tracking_num=tracking_num, max_price=max_price, min_price=min_price)
        elif pentry.get():
            price = float(pentry.get())
            res = sql.queryOrderDetailInfo(order_id=orderId, good_id=good, order_status=state, tracking_num=tracking_num, price=price)
        else:
            res = sql.queryOrderDetailInfo(order_id=orderId, good_id=good, order_status=state, tracking_num=tracking_num)
        showData(res, ["orderId", "goodId", "price", "number", "status", "trackingNumber"], False)

    fun_dict = {
        1: addOrder,
        2: delOrder,
        3: editOrder,
        4: queryOrder,
        5: queryOrderDetail
    }

    button = tk.Button(inputWindow, text="确定", command=fun_dict[s])
    button.pack(side="bottom", padx=10, pady=10)

if __name__ == '__main__':
    sql = DianshangDatabase("test")

    root = tk.Tk()
    root.geometry("1500x800")
    root.title("电商数据库")

    # 菜单栏
    top =tk.Menu(root)
    createMenu()
    root.config(menu=top)

    # 创建一个框架，用于存放表格，靠左显示
    frame_left = tk.Frame(root, width=1500, height=600)
    frame_left.pack(side='left', anchor='n', padx=10, pady=10)

    # # 创建一个右侧的框架
    # frame_right = tk.Frame(root, width=300, height=600, bg='gray')
    # frame_right.pack(side='right', anchor='n', padx=10, pady=10)

    root.mainloop()

    # print(sql.queryOrderInfo(user_id=1))
    # print(sql.queryOrderDetailInfo(good_id=1))

    # sql.delOrder(17)
    # # 订单添加
    # print(sql.addOrder(1, 1, []))

    # # 订单修改
    # sql.editOrderStatus(9, 10, 4)
    #
    # # 订单查询
    # print(sql.queryOrder())

    # print(sql.user_dict)
    # print(sql.store_dict)
    # pprint(sql.order_dict)

