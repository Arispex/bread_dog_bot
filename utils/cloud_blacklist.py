import config
import requests


def detect(qq: str | int | list):
    """
    检测QQ是否在云黑名单中
    :param qq: QQ number.
    :return: 检测成功返回[True, 在云黑中的QQ] 否则返回[False, 失败原因]
    """
    if isinstance(qq, str):
        qq = [qq]
    if isinstance(qq, int):
        qq = [str(qq)]
    if not isinstance(qq, list):
        return [False, "参数错误"]
    if len(qq) == 0:
        return [False, "参数错误"]
    for i in qq:
        if not isinstance(i, str):
            return [False, "参数错误"]
    url = config.CloudBlacklist.url + "/blacklist/"
    token = config.CloudBlacklist.token
    params = {
        "token": token,
        "qq": qq
    }
    r = requests.get(url, params=params)
    blacklist = []
    if r.status_code == 200:
        for i in r.json()["data"]:
            for j in qq:
                if i[0] == j:
                    blacklist.append(j)
        return [True, blacklist]

    elif r.status_code == 403:
        return [False, r.json()["msg"]]
    elif r.status_code == 429:
        return [False, "请求过于频繁，请稍等五秒后再试"]
    else:
        return [False, "无法连接至服务器"]


def add(qq: str, group_id: str, reason: str):
    """
    将QQ加入云黑名单
    :param qq: QQ number.
    :return: 成功返回[True, "成功加入云黑"] 否则返回[False, 失败原因]
    :param group_id: QQ群号
    :param reason: 原因
    """
    if not isinstance(qq, str):
        return [False, "参数错误"]
    url = config.CloudBlacklist.url + "/blacklist/add/"
    token = config.CloudBlacklist.token
    params = {
        "token": token,
        "QQ": qq,
        "groupID": group_id,
        "reason": reason
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return [True, "成功加入云黑"]
    elif r.status_code == 403:
        return [False, r.json()["msg"]]
    elif r.status_code == 429:
        return [False, "请求过于频繁，请稍等五秒后再试"]
    else:
        return [False, "无法连接至服务器"]


def delete(qq: str):
    """
    将QQ从云黑名单中移除
    :param qq: QQ number.
    :return: 成功返回[True, "成功移除云黑"] 否则返回[False, 失败原因]
    """
    if not isinstance(qq, str):
        return [False, "参数错误"]
    url = config.CloudBlacklist.url + "/blacklist/delete/"
    token = config.CloudBlacklist.token
    params = {
        "token": token,
        "QQ": qq
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        return [True, "成功移除云黑"]
    elif r.status_code == 403:
        return [False, r.json()["msg"]]
    elif r.status_code == 429:
        return [False, "请求过于频繁，请稍等五秒后再试"]
    else:
        return [False, "无法连接至服务器"]


def query(qq: str):
    """
    查询QQ是否在云黑名单中
    :param qq: QQ number.
    :return: 检测成功返回[True, 在云黑中的QQ] 否则返回[False, 失败原因]
    """
    if not isinstance(qq, str):
        return [False, "参数错误"]
    url = config.CloudBlacklist.url + "/blacklist/"
    token = config.CloudBlacklist.token
    params = {
        "token": token,
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        for i in r.json()["data"]:
            if i[0] == qq:
                return [True, i]
        return [False, "未找到该QQ"]
    elif r.status_code == 403:
        return [False, r.json()["msg"]]
    elif r.status_code == 429:
        return [False, "请求过于频繁，请稍等五秒后再试"]
    else:
        return [False, "无法连接至服务器"]

