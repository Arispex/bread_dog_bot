import time

import config
import utils.server
import utils.player
import utils.whitelist
import utils.mail
import utils.lottery


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

    def get_mail(self):
        """
        获取邮箱
        :return: 获取结果 成功返回[True, 邮箱内容(list)] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, player_mail = utils.mail.get(self.qq)
            if result:
                return True, player_mail
            else:
                return False, player_mail
        else:
            return False, self.player_info

    def add_mail(self, item_id: int, item_num: int):
        """
        增加邮件
        :param item_id: 物品ID
        :param item_num: 物品数量
        "return: 添加结果 成功返回[True, None] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.mail.add(self.qq, item_id, item_num)
            if result:
                return True, None
            else:
                return False, reason
        else:
            return False, self.player_info

    def sub_mail(self, item_id: int, item_num: int):
        """
        删除邮件
        :param item_id: 物品ID
        :param item_num: 物品数量
        "return: 删除结果 成功返回[True, None] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.mail.sub(self.qq, item_id, item_num)
            if result:
                return True, None
            else:
                return False, reason
        else:
            return False, self.player_info

    def empty_mail(self, item_sn: int):
        """
        清空邮箱指定序号的物品
        :param item_sn: 邮箱物品序号
        :return: 清空结果 成功返回[True, None] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.mail.empty(self.qq, item_sn)
            if result:
                return True, None
            else:
                return False, reason
        else:
            return False, self.player_info

    def send_mail(self, target_qq: str, item_sn: int):
        """
        发送邮件至指定目标玩家
        :param target_qq: 目标玩家QQ或昵称
        :param item_sn: 物品物品序号
        :return: 发送结果 成功返回[True, None] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, player_mail = self.get_mail()
            if result:
                if len(player_mail) < item_sn:  # 判断序号是否超出邮箱的长度
                    return False, f"不存在序号为{item_sn}的物品"
                item_id = player_mail[item_sn - 1][0]
                item_num = player_mail[item_sn - 1][1]

                result, reason = utils.mail.empty(self.qq, item_sn)
                if result:  # 是否清空成功
                    target_player = Player(target_qq)  # 创建Player对象，可以无需判断传入的是QQ还是玩家昵称
                    result, reason = utils.mail.add(target_player.qq, int(item_id), int(item_num))
                    if result:  # 是否发送成功
                        return True, None
                    else:
                        utils.mail.add(self.qq, int(item_id), int(item_num))
                        if reason == "不存在此玩家":
                            reason = "目标玩家不存在，邮件被退回"
                        return False, reason
                else:
                    return False, reason
            else:
                return False, player_mail
        else:
            return False, self.player_info

    def pick_up_mail(self, item_sn: int, ip: str, port: str, token: str):
        """
        领取邮件
        :param item_sn: 邮箱中邮件(物品)的序号
        :param ip: 服务器ip
        :param port: 服务器端口
        :param token: 服务器token
        :return: 领取结果 成功返回[True, None] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.mail.pick_up(self.qq, item_sn, ip, port, token)
            if result:
                return True, None
            else:
                return False, reason
        else:
            return False, self.player_info

    def recycle_mail(self, item_sn: int):
        """
        回收邮件
        :param item_sn: 回收的邮件(物品)序号
        :return: 回收结果 成功返回[True, 获取金币数量] 失败返回[False, 错误信息]
        """
        if self.status_code:
            result, reason = utils.mail.recycle(self.qq, item_sn)
            if result:
                return True, reason
            else:
                return False, reason
        else:
            return False, self.player_info

    def random_lottery(self, count: int = 1):
        if self.status_code:
            result, lottery_result = utils.lottery.random_lottery(self.qq, count)
            if result:
                result, player_mail = self.get_mail()
                if result:
                    if 36 - len(player_mail) >= count:
                        for i in lottery_result:
                            self.add_mail(i[0], i[1])
                        return True, lottery_result
                    else:
                        self.add_money(count * config.Lottery.RandomLottery.cost_money)
                        return False, "邮箱空间不足\n请先清理邮箱"
                else:
                    self.add_money(count * config.Lottery.RandomLottery.cost_money)
                    return False, player_mail
            else:
                return False, lottery_result
        else:
            return False, self.player_info
