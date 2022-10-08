import json
import sqlite3

import config
import utils.server
import models.prize_pool
import random
import models.player
import models.server


class GetInfo:
    @staticmethod
    def all():
        """
        获取所有奖池信息
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from prize_pool")
        if result:
            return True, sql_return_result
        else:
            return False, sql_return_result

    @staticmethod
    def by_id(id: int):
        """
        以ID获取奖池信息
        :param id: 奖池ID
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from prize_pool where ID = '%s'" % id)
        if result:
            if not sql_return_result:
                return False, "不存在此奖池"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_name(name: str):
        """
        以名称获取奖池信息
        :param name: 奖池名称
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from prize_pool where name = '%s'" % name)
        if result:
            if not sql_return_result:
                return False, "不存在此奖池"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result


def add(name: str, price: int, progress: str, progress_server: int):
    """
    添加奖池
    :param name: 奖池名称
    :param price: 单次抽奖价格
    :param progress: 进度限制
    :param progress_server: 进度限制服务器
    """
    result, prize_pool_info = GetInfo.by_name(name)
    progress_dict = {"史莱姆王": "King Slime", "克苏鲁之眼": "Eye of Cthulhu",
                     "世界吞噬者/克苏鲁之脑": "Eater of Worlds / Brain of Cthulhu", "蜂后": "Queen Bee",
                     "骷髅王": "Skeletron",
                     "巨鹿": "Deerclops", "血肉之墙": "Wall of Flesh", "史莱姆女王": "Queen Slime",
                     "双子魔眼": "The Twins",
                     "毁灭者": "The Destroyer", "机械骷髅王": "Skeletron Prime", "世纪之花": "Plantera",
                     "石巨人": "Golem",
                     "猪龙鱼公爵": "Duke Fishron", "光之女皇": "Empress of Light", "拜月教邪教徒": "Lunatic Cultist",
                     "月亮领主": "Moon Lord", "无": "None"}
    if progress in progress_dict.keys():
        if result:
            return False, "已经存在同名奖池"
        else:
            if price < 0:
                return False, "价格超出范围(>0)"
            result, server_info = utils.server.GetInfo.by_id(progress_server)
            if result:
                result, sql_return_result = utils.server.execute_sql(
                    "insert into prize_pool (Name, Price, Progress, ProgressServer) values ('%s', '%s', '%s', '%s')" % (
                        name, price, progress_dict[progress], progress_server))
                if result:
                    result, prize_pool_info_list = GetInfo.all()
                    num = 1
                    for i in prize_pool_info_list:
                        utils.server.execute_sql("update prize_pool set ID = '%s' where Name = '%s'" % (num, i[1]))
                        num += 1
                    utils.server.execute_sql(
                        "update sqlite_sequence set seq = '%s' where name = '%s'" % (
                            len(prize_pool_info_list), "prize_pool"))
                    return True, None
                else:
                    return False, sql_return_result
            else:
                return False, server_info
    else:
        return False, f"未知的进度：{progress}"


def delete(name: str):
    """
    删除奖池
    :param name: 奖池名称
    """
    result, prize_pool = GetInfo.by_name(name)
    if result:
        result, sql_return_result = utils.server.execute_sql("delete from prize_pool where Name = '%s'" % name)
        if result:
            result, prize_pool_list = GetInfo.all()
            num = 1
            for i in prize_pool_list:
                utils.server.execute_sql("update prize_pool set ID = '%s' where Name = '%s'" % (num, i[1]))
                num += 1
            utils.server.execute_sql(
                "update sqlite_sequence set seq = '%s' where name = '%s'" % (len(prize_pool_list), "prize_pool"))
            return True, None
        else:
            return False, sql_return_result
    else:
        return False, prize_pool


def add_item(prize_pool_id: int, item_id: int, item_max_amount: int, item_min_amount: int, probability):
    """
    添加奖池道具
    :param prize_pool_id: 奖池ID
    :param item_id: 道具ID
    :param item_max_amount: 道具最大数量
    :param item_min_amount: 道具最小数量
    :param probability: 概率
    :return: 添加结果 成功返回[True, 添加结果], 失败返回[False, 失败原因]
    """
    result, prize_pool_info = GetInfo.by_id(prize_pool_id)
    if result:
        if item_id > 5124 or item_id < 1:  # 判断物品id是否合法
            return False, "物品ID超出范围(1-5124)"
        if item_max_amount < 1 or item_max_amount > 999:  # 判断物品最大数量是否合法
            return False, "最大数量超出范围(1-999)"
        if item_min_amount < 1 or item_min_amount > 999:  # 判断物品最小数量是否合法
            return False, "最小数量超出范围(1-999)"
        if item_max_amount < item_min_amount:
            return False, "最大数量小于最小数量"
        if probability <= 0:
            return False, "概率超出范围(>0)"

        if prize_pool_info[5]:
            content = prize_pool_info[5].split(",")
        else:
            content = []
        content.append(f"{item_id}:{item_max_amount}:{item_min_amount}:{probability}")
        result, sql_return_result = utils.server.execute_sql(
            "update prize_pool set content = '%s' where ID = '%s'" % (",".join(content), prize_pool_id))
        if result:
            return True, None
        else:
            return False, sql_return_result
    else:
        return False, prize_pool_info


def delete_item(prize_pool_id: int, item_sn: int):
    """
    删除奖池道具
    :param prize_pool_id: 奖池ID
    :param item_sn: 道具序号
    :return: 删除结果 成功返回[True, 删除结果], 失败返回[False, 失败原因]
    """
    result, prize_pool_info = GetInfo.by_id(prize_pool_id)
    if result:
        if prize_pool_info[5]:
            content = prize_pool_info[5].split(",")
        else:
            content = []

        if item_sn < 1:
            return False, "序号超出范围(>0)"

        if item_sn > len(content):
            return False, f"不存在序号为{item_sn}的物品"

        content.pop(item_sn - 1)

        result, sql_return_result = utils.server.execute_sql(
            "update prize_pool set content = '%s' where ID = '%s'" % (",".join(content), prize_pool_id))
        if result:
            return True, None
        else:
            return False, sql_return_result
    else:
        return False, prize_pool_info


def lottery(qq: str, prize_pool_id: int, count: int = 1):
    """
    抽奖
    :param qq: QQ号
    :param prize_pool_id: 奖池ID
    :param count: 抽奖次数
    :return: 抽奖结果 成功返回[True, 抽奖结果], 失败返回[False, 失败原因]
    """
    result, prize_pool_info = GetInfo.by_id(prize_pool_id)
    if result:
        prize_pool = models.prize_pool.PrizePool(prize_pool_id)
        if prize_pool.content:
            if count < 1 or count > 10:
                return False, "抽奖次数超出范围(1-10)"

            result, server_info = utils.server.GetInfo.by_id(prize_pool.progress_server)
            if result:
                server = models.server.Connect(*server_info[2:])
                result, server_progress = server.progress()
                if result:
                    server_progress = json.loads(server_progress['response'])
                    server_progress["None"] = True
                else:
                    return False, server_progress
            else:
                return False, server_info

            if not server_progress[prize_pool.progress]:
                return False, "未达到进度"

            player = models.player.Player(qq)

            if player.money < count * prize_pool.price:
                return False, f"{config.Currency.name}不足"

            l = []
            for i in prize_pool.content:
                for x in range(int(round(i["item_probability"] / prize_pool.total_probability, 2) * 100)):
                    l.append(i["item_id"])

            with open("items.json", "r", encoding="utf-8") as f:
                items = json.load(f)

            result = []

            for i in range(count):
                result_item_id = random.choice(l)
                for x in prize_pool.content:
                    if x["item_id"] == result_item_id:
                        result_item_amount = random.randint(x["item_min_amount"], x["item_max_amount"])
                        result_item_name = items[result_item_id - 1][1]
                        result.append([result_item_id, result_item_amount, result_item_name])
                        break

            return True, result
        else:
            return False, "奖池没有物品"
    else:
        return False, prize_pool_info
