import re
from pprint import pprint

from sqlclass import DianshangDatabase


# 用户名规则
def checkUsername(username):
    # 用户名需要满足 6-16 位，只能包含字母、数字、下划线
    match = r"^[\w_]{6,16}$"
    if not re.match(match, username):
        return False
    return True

if __name__ == '__main__':
    sql = DianshangDatabase("test")

    # # 添加用户
    # username = "test"
    # usergender = "男"
    # userage = 20
    # print(sql.addUser([username, usergender, userage, 1]))
    #
    # # 删除用户
    # sql.delUser(2)
    #
    # # 修改用户信息
    # print(sql.editUserInfo(3, name="test66"))
    # print(sql.store_dict)
    #
    # # 查询用户信息
    # # print(sql.queryUserInfo())
    # print(sql.queryUserInfo(gender="男"))
    #
    # print(sql.store_dict)
    # # breakpoint()
    # # 新增商店
    # print(sql.addShop(["潮流服饰", "潮流服饰"]))
    #
    # print(sql.store_dict)
    #
    # # 修改商店信息
    # print(sql.editShopInfo(6, "99999", "66666"))

    # print(sql.store_dict)
    # # 删除商店
    # sql.delShop(4)
    # print(sql.store_dict)

    # # 商品添加
    # sql.addGood(["6666", "9999", 6.66, 9])
    #
    # # 商品修改
    # sql.editGoodInfo(1, name="669966", goodType="1651")
    # print(sql.store_dict)
    #
    # # 商品删除
    # sql.delGood(1)
    #
    # # 商店查询
    # # print(sql.store_dict)
    # print(sql.queryShopInfo(shopType="家居用品"))

    # print(sql.store_dict)
    # # 商店商品查询
    # print(sql.queryGoodInfo(good_id=16))

    # # 订单添加
    # print(sql.addOrder(1, 1, [(3, 5), (2, 10), (4, 3)]))

    # # 订单修改
    # sql.editOrderStatus(9, 10, 4)
    #
    # # 订单查询
    # print(sql.queryOrder())

    print(sql.user_dict)
    print(sql.store_dict)
    pprint(sql.order_dict)