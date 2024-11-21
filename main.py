import re

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
    # print(sql.addUser((username, usergender, userage)))

    # # 删除用户
    # sql.delUser(2)

    # # 修改用户信息
    # print(sql.editUserInfo(3, name="test66"))

    # # 查询用户信息
    # # print(sql.queryUserInfo())
    # print(sql.queryUserInfo(gender="男"))
