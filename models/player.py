import utils.server
import utils.player
import random
import config


class Player:
    def __init__(self, qq):
        self.qq = qq
        player = utils.server.execute_sql("select * from whitelist where QQ = '%s'" % qq)
        if not player:
            self.status = False
        else:
            self.status = True

    def sign_in(self):
        """
        签到
        :return: 签到结果 成功返回[True, 金币添加数量] 失败返回[False, 原因]
        """
        if self.status:
            result, reason = utils.player.sign_in(self.qq)
            if result:
                add_money = random.randint(config.min_sign_in_money, config.max_sign_in_money)
                utils.server.execute_sql("update whitelist set money = money + '%d'" % add_money)
                return True, add_money
            else:
                return False, reason
