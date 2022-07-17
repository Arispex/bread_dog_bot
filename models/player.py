import time
import utils.server
import utils.player
import utils.whitelist


class Player:
    """
    玩家类
    """

    def __init__(self, qq):
        """
        初始化玩家
        :param qq: 玩家白名单绑定的qq或玩家昵称
        """
        self.qq = qq
        result, player_info = utils.whitelist.GetInfo.by_qq(qq)
        if result:
            self.status_code = True
            self.player_info = player_info
            self.id = player_info[0]
            self.qq = player_info[1]
            self.name = player_info[2]
            self.money = player_info[3]
            self.sign_in_code = player_info[4]
            self.get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        else:
            result, player_info = utils.whitelist.GetInfo.by_name(qq)
            if result:
                self.status_code = True
                self.player_info = player_info
                self.id = player_info[0]
                self.qq = player_info[1]
                self.name = player_info[2]
                self.money = player_info[3]
                self.sign_in_code = player_info[4]
                self.get_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            else:
                self.status_code = False
                self.player_info = player_info
                self.reason = player_info

    def add_money(self, money):
        """
        增加金钱
        :param money: 金钱数量
        :return: 添加结果 成功返回[True, 新的金钱数量] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.player.Money.add(self.qq, money)
            if result:
                self.money += money
                return True, self.money
            else:
                return False, reason
        else:
            return False, self.player_info

    def sub_money(self, money):
        """
        减少金钱
        :param money: 金钱数量
        :return: 减少结果 成功返回[True, 新的金钱数量] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.player.Money.sub(self.qq, money)
            if result:
                self.money -= money
                return True, self.money
            else:
                return False, reason
        else:
            return False, self.player_info

    def set_money(self, money):
        """
        设置金钱
        :param money: 金钱数量
        :return: 设置结果 成功返回[True, 新的金钱数量] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.player.Money.set(self.qq, money)
            if result:
                self.money = money
                return True, self.money
            else:
                return False, reason
        else:
            return False, self.player_info

    def sign_in(self):
        """
        签到
        :return: 签到结果 成功返回[True, 签到获得的金钱数量] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.player.sign_in(self.qq)
            if result:
                self.money += reason
                return True, reason
            else:
                return False, reason
        else:
            return False, self.player_info

    def get_sign_in_log(self):
        """
        获取签到记录
        :return: 签到记录 成功返回[True, 签到记录] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.player.get_sign_in_log(self.qq)
            if result:
                return True, reason
            else:
                return False, reason
        else:
            return False, self.player_info
