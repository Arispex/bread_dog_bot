import json


def get() -> list:
    """
    获取管理员列表
    :return: 管理员列表(list)
    """
    try:
        with open("admins.json", "r") as f:
            return json.load(f)
    except:
        with open("admins.json", "w") as f:
            f.write("[]")
            return []


def add(qq: str):
    """
    添加管理员
    :param qq: QQ号
    :return: 添加结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    admins = get()
    if qq in admins:
        return False, "已经是管理员了"
    else:
        with open("admins.json", "r") as f:
            admins = json.load(f)
        admins.append(qq)
        with open("admins.json", "w") as f:
            json.dump(admins, f)
        return True, None


def delete(qq: str):
    """
    删除管理员
    :param qq:QQ号
    :return: 删除结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    admins = get()
    if qq not in admins:
        return False, "不是管理员"
    else:
        with open("admins.json", "r") as f:
            admins = json.load(f)
        admins.remove(qq)
        with open("admins.json", "w") as f:
            json.dump(admins, f)
        return True, None


def reset():
    """
    清空管理员列表
    :return: 清空结果 成功返回True 失败返回False(貌似这玩意儿不会失败？
    """
    with open("admins.json", "w") as f:
        f.write("[]")
        return True
