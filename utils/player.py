import utils.server
import utils.whitelist
import random
import config


class Money:
    @staticmethod
    def get(qq: str):
        """
        获取玩家的金钱
        :return: 玩家的金钱 成功返回[True, 货币数量] 否则返回[False, 失败原因]
        """
        result, player_info = utils.whitelist.GetInfo.by_qq(qq)
        if result:
            return True, player_info[3]
        else:
            return False, player_info

    @staticmethod
    def set(qq: str, money: int):
        """
        设置玩家的金钱
        :return: 设置结果 成功返回[True, 设置后的货币数量] 否则返回[False, 失败原因]
        """
        result, player_info = utils.whitelist.GetInfo.by_qq(qq)
        if result:
            result, sql_return_result = utils.server.execute_sql(
                "UPDATE whitelist SET Money = '%s' WHERE QQ = '%s'" % (money, qq))
            if result:
                return True, money
            else:
                return False, sql_return_result
        else:
            return False, player_info

    @staticmethod
    def add(qq: str, money: int):
        """
        增加玩家的金钱
        :return: 增加结果 成功返回[True, 增加后的货币数量] 否则返回[False, 失败原因]
        """
        result, player_info = utils.whitelist.GetInfo.by_qq(qq)
        if result:
            result, sql_return_result = utils.server.execute_sql(
                "UPDATE whitelist SET Money = '%s' WHERE QQ = '%s'" % (player_info[3] + money, qq))
            if result:
                return True, player_info[3] + money
            else:
                return False, sql_return_result
        else:
            return False, player_info

    @staticmethod
    def sub(qq: str, money: int):
        """
        减少玩家的金钱
        :return: 减少结果 成功返回[True, 减少后的货币数量] 否则返回[False, 失败原因]
        """
        result, player_info = utils.whitelist.GetInfo.by_qq(qq)
        if result:
            if player_info[3] >= money:
                result, sql_return_result = utils.server.execute_sql(
                    "UPDATE whitelist SET Money = '%s' WHERE QQ = '%s'" % (player_info[3] - money, qq))
                if result:
                    return True, player_info[3] - money
                else:
                    return False, sql_return_result
            else:
                return False, "扣除数量不能大于玩家现有的数量"
        else:
            return False, player_info


def sign_in(qq: str):
    """
    签到
    :return: 签到结果 成功返回[True, 签到获得货币数量] 否则返回[False, 失败原因]
    """
    result, player_info = utils.whitelist.GetInfo.by_qq(qq)
    if result:
        if player_info[4] == 0:
            result, sql_return_result = utils.server.execute_sql(
                "UPDATE whitelist SET SignIn = '1' WHERE QQ = '%s'" % qq)
            if result:
                get_money = random.randint(config.SignIn.min_money, config.SignIn.max_money)
                utils.server.execute_sql(
                    "insert into signInLog (QQ, getMoney) values ('%s', '%s')" % (qq, get_money))
                Money.add(qq, get_money)
                return True, get_money
            else:
                return False, sql_return_result
        else:
            return False, "已经签到过了"
    else:
        return False, player_info


def get_sign_in_log(qq: str):
    """
    获取玩家的签到记录
    :return: 签到记录 成功返回[True, 签到记录] 否则返回[False, 失败原因]
    """
    result, player_info = utils.whitelist.GetInfo.by_qq(qq)
    if result:
        result, sql_return_result = utils.server.execute_sql(
            "SELECT * FROM signInLog WHERE QQ = '%s'" % qq)
        if result:
            return True, sql_return_result[0]
        else:
            return False, sql_return_result
    else:
        return False, player_info
