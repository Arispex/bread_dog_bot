import utils.prize_pool
import utils.text_handle


class PrizePool(object):
    """
    奖池
    """

    def __init__(self, prize_pool_id: int):
        """
        初始化奖池
        :param prize_pool_id: 奖池ID
        """
        result, prize_pool_info = utils.prize_pool.GetInfo.by_id(prize_pool_id)
        print(result, prize_pool_info)
        if result:
            self.status = True
            self.id = prize_pool_info[0]
            self.name = prize_pool_info[1]
            self.price = prize_pool_info[2]
            self.progress = prize_pool_info[3]
            self.progress_zh = utils.text_handle.Translator.Progress.en_to_zh(self.progress)
            self.progress_server = prize_pool_info[4]
            if prize_pool_info[5]:
                self.content = [
                    {"item_id": int(i.split(':')[0]), "item_max_amount": int(i.split(':')[1]),
                     "item_min_amount": int(i.split(':')[2]),
                     "item_probability": int(i.split(':')[3])} for i in
                    prize_pool_info[5].split(",")]
                self.total_probability = sum([int(i["item_probability"]) for i in self.content])
            else:
                self.content = []
                self.total_probability = 0
        else:
            self.status = False
            self.error = prize_pool_info

    def reload(self):
        """
        重读数据
        """
        result, prize_pool_info = utils.prize_pool.GetInfo.by_id(self.id)
        if result:
            self.status = True
            self.id = prize_pool_info[0]
            self.name = prize_pool_info[1]
            self.price = prize_pool_info[2]
            self.progress = prize_pool_info[3]
            self.progress_server = prize_pool_info[4]
            if prize_pool_info[5]:
                self.content = [
                    {"item_id": int(i.split(':')[0]), "item_max_amount": int(i.split(':')[1]), "item_min_amount": int(i.split(':')[2]),
                     "item_probability": int(i.split(':')[3])} for i in
                    prize_pool_info[5].split(",")]
                self.total_probability = sum([int(i["item_probability"]) for i in self.content])
            else:
                self.content = []
                self.total_probability = 0
        else:
            self.status = False
            self.error = prize_pool_info

    def add(self, item_id: int, item_max_amount: int, item_min_amount: int, probability: int):
        """
        添加物品
        :param item_id: 物品id
        :param item_max_amount: 最大数量
        :param item_min_amount: 最小数量
        :param probability: 概率
        """
        if self.status:
            result, reason = utils.prize_pool.add_item(self.id, item_id, item_max_amount, item_min_amount, probability)
            if result:
                self.reload()
                return True, None
            else:
                return False, reason
        else:
            return False, self.error

    def delete(self, item_sn: int):
        """
        删除物品
        :param item_sn: 物品序号
        """
        if self.status:
            result, reason = utils.prize_pool.delete_item(self.id, item_sn)
            if result:
                self.reload()
                return True, None
            else:
                return False, reason
        else:
            return False, self.error