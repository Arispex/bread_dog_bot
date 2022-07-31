class Group:
    # QQ群昵称 用于群员加入与退出
    id = "489192282"
    name = "Terraria Journey"


class Currency:
    # 货币名称
    name = "金币"


class SignIn:
    # 签到获取最大金钱
    max_money = 100
    # 签到获取最小金钱
    min_money = 10


class CloudBlacklist:
    # 云黑地址
    # 可自行搭建云黑服务器
    # Github: https://github.com/Qianyiovo/bread_dog_bot_server
    url = "https://service-c2b8evns-1302721716.gz.apigw.tencentcs.com/"
    # 云黑密钥(Token) 用于验证用户
    # Token均为BDT_开头 需要请找云黑主人获取
    # 需要项目自带的云黑TOKEN请联系千亦
    # 邮箱：qianyi@qianyiovo.com
    token = ""


class Whitelist:
    # 白名单模式
    # normal: 普通模式 一对一添加白名单 即每个服务器都需要添加白名单
    # cluster: 集群模式 一对多添加白名单 即只需添加一次白名单（一个服务器的白名单）所有服务器都可以进入
    method = "normal"
    # 主要的服务器 用于cluster集群模式 其他模式无需设置 参数为服务器序号
    # 比如我序号1的服务器是主城 就填写1 这样只对主城服务器添加白名单
    main_server = 1


class Lottery:
    # 随机抽奖
    class RandomLottery:
        # 随机抽奖开关 是否启用随机抽奖
        enable = True
        # 随机抽奖物品id范围
        # 最小id 不能小于1
        min_item_id = 1
        # 最大id 不能大于5124(v1.4.3.6)
        max_item_id = 5124
        # 随机抽奖物品数量范围
        # 最小数量 不能小于1
        min_item_count = 1
        # 最大数量 不能大于999
        max_item_count = 100
        # 每次抽奖消耗金币数量
        cost_money = 50


class Event:
    class Welcome:
        # 进群自动检测黑名单 如果检测到是否自动踢出该玩家
        kick_blacklist = True
