import random
import config
import json
import models.player
import models.prize_pool


def random_lottery(qq: str, count: int = 1):
    """
    随机抽奖
    :param qq: 玩家QQ
    :param count: 抽奖次数
    """
    enable = config.Lottery.RandomLottery.enable
    if enable:
        if count < 1 or count > 10:
            return False, "抽奖次数必须在1-10次之间"
        player = models.player.Player(qq)
        cost_money = config.Lottery.RandomLottery.cost_money * count
        if player.money >= cost_money:
            max_item_id = config.Lottery.RandomLottery.max_item_id
            min_item_id = config.Lottery.RandomLottery.min_item_id

            max_item_count = config.Lottery.RandomLottery.max_item_count
            min_item_count = config.Lottery.RandomLottery.min_item_count

            result = []

            with open("items.json", "r", encoding="utf-8") as f:
                items = json.load(f)

            for i in range(count):
                item_id = random.randint(min_item_id, max_item_id)
                item_count = random.randint(min_item_count, max_item_count)

                item_name = items[item_id - 1][1]

                result.append([item_id, item_count, item_name])

            return True, result
        else:
            return False, f"{config.Currency.name}不足"

    else:
        return False, "随机抽奖未开启"
