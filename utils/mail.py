import random

import utils.whitelist
import utils.server
import utils.RESTAPI
import models.player
import models.server


def get(qq: str):
    """
    获取指定QQ的邮箱信息
    :param qq: 玩家QQ
    :return: 获取结果 成功返回[True, 邮箱信息(list)] 失败返回[False, 错误信息]
    """
    result, player_info = utils.whitelist.GetInfo.by_qq(qq)
    if result:
        player_mail = player_info[5]
        if not player_mail:  # 判断邮箱是否为空
            player_mail = []
        else:
            player_mail = player_mail.split(',')
            player_mail = map(lambda x: [x.split(":")[0], x.split(":")[1]], player_mail)
            player_mail = list(player_mail)
        return True, player_mail
    else:
        return False, player_info


def add(qq: str, item_id: int, item_num: int):
    """
    增加指定QQ的邮箱物品
    :param qq: 玩家QQ
    :param item_id: 增加的物品的ID
    :param item_num: 增加的物品的数量
    :return: 增加结果 成功返回[True, None] 失败返回[False, 错误信息]
    """
    if item_id > 5124 or item_id < 1:  # 判断物品id是否合法
        return False, "物品ID超出范围(1-5124)"
    if item_num > 999 or item_num < 1:  # 判断物品数量是否合法
        return False, "物品数量超出范围(1-999)"
    result, player_mail = get(qq)
    if result:
        if len(player_mail) >= 36:  # 判断邮箱是否已满
            return False, "邮箱已满，请先领取部分物品"
        player_mail.append([str(item_id), str(item_num)])
        player_mail = map(lambda x: ":".join(x), player_mail)
        player_mail = ",".join(player_mail)
        utils.server.execute_sql("update whitelist set mail = '%s' where qq = '%s'" % (player_mail, qq))
        return True, None
    else:
        return False, player_mail


def sub(qq: str, item_id: int, item_num: int):
    """
    删除指定QQ的邮箱中的指定物品
    :param qq: 玩家QQ
    :param item_id: 删除的物品的ID
    :param item_num: 删除的物品的数量
    :return: 删除结果 成功返回[True, None] 失败返回[False, 错误信息]
    """
    result, player_mail = get(qq)
    if result:
        reason = "邮箱中没有该物品"  # 防止邮箱为空时出现错误(无返回值)
        for i in range(len(player_mail)):
            reason = "邮箱中没有该物品"
            if player_mail[i][0] == str(item_id):  # 是否有该物品
                reason = "物品数量不足，目前拥有%s个" % player_mail[i][1]
                if int(player_mail[i][1]) >= item_num:  # 数量是否大于等于扣除的数量
                    if int(player_mail[i][1]) == item_num:  # 数量是否等于扣除的数量
                        player_mail.pop(i)  # 删除该物品
                    else:
                        player_mail[i] = [player_mail[i][0], str(int(player_mail[i][1]) - item_num)]

                    player_mail = map(lambda x: ":".join(x), player_mail)
                    player_mail = ",".join(player_mail)
                    utils.server.execute_sql("update whitelist set mail = '%s' where qq = '%s'" % (player_mail, qq))
                    return True, None
        return False, reason
    else:
        return False, player_mail


def empty(qq: str, item_sn: int):
    """
    清空指定QQ的指定序号的格子
    :param qq: 玩家QQ
    :param item_sn: 指定清空的邮件(物品)
    :return: 清空结果 成功返回[True, None] 失败返回[False, 错误信息]
    """
    result, player_mail = get(qq)
    if result:
        if item_sn > 36 or item_sn < 1:  # 判断序号是否合法
            return False, "序号超出范围(1-36)"
        if len(player_mail) >= item_sn:  # 判断序号是否超出邮箱的长度
            player_mail.pop(item_sn - 1)
            player_mail = map(lambda x: ":".join(x), player_mail)
            player_mail = ",".join(player_mail)
            utils.server.execute_sql("update whitelist set mail = '%s' where qq = '%s'" % (player_mail, qq))
            return True, None
        else:
            return False, f"不存在序号为{item_sn}的物品"
    else:
        return False, player_mail


def pick_up(qq: str, item_sn: int, ip: str, port: str, token: str):
    """
    领取指定邮件
    :param qq: 玩家QQ
    :param item_sn: 物品(邮件)序号
    :param ip: 服务器ip
    :param port: 服务器端口
    :param token: 服务器token
    :return: 领取结果 成功返回[True, None] 失败返回[False, 错误信息]
    """
    result, player_mail = get(qq)
    if result:
        if item_sn > 36 or item_sn < 1:  # 判断序号是否合法
            return False, "序号超出范围(1-36)"
        if len(player_mail) >= item_sn:  # 判断序号是否拥有该序号的物品
            item_id = player_mail[item_sn - 1][0]
            item_num = player_mail[item_sn - 1][1]

            player = models.player.Player(qq)
            conn = models.server.Connect(ip, port, token)

            result, reason = conn.give(player.name, item_id, item_num)

            if result:
                empty(qq, item_sn)
                return True, None
            else:
                reason = "您还没有上线" if reason == "玩家不存在" else reason
                return False, reason
        else:
            return False, f"不存在序号为{item_sn}的物品"
    else:
        return False, player_mail


def recycle(qq: str, item_sn: int):
    """
    回收指定邮件
    :param qq: 玩家QQ
    :param item_sn: 回收的邮件(物品)编号
    :return: 回收结果 成功返回[True, 获得金币] 失败返回[False, 错误信息]
    """
    result, player_mail = get(qq)
    if result:
        if item_sn > 36 or item_sn < 1:  # 判断序号是否合法
            return False, "序号超出范围(1-36)"
        if len(player_mail) >= item_sn:  # 判断序号是否拥有该序号的物品
            item_id = player_mail[item_sn - 1][0]
            item_num = player_mail[item_sn - 1][1]
            result, reason = empty(qq, item_sn)
            if result:
                player = models.player.Player(qq)
                money = random.randint(1, int(item_num) // 5)
                player.add_money(money)
                return True, money
            else:
                return False, reason
        else:
            return False, f"不存在序号为{item_sn}的物品"
    else:
        return False, player_mail
