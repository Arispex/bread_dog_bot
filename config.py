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
    token = ""
