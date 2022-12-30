from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event

import config

help = on_command("帮助")


@help.handle()
async def help_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「帮助」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        command = text[1]
        if command == "帮助":
            await help.finish("——帮助——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "获取指定功能的使用说明\n"
                              "用法：\n"
                              "帮助 [名称]\n"
                              "参数：\n"
                              "名称 - 功能名称")
        elif command == "在线":
            await help.finish("——在线——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "获取服务器列表所有服务器的在线玩家\n"
                              "用法：\n"
                              "在线\n"
                              "参数：\n"
                              "无")
        elif command == "执行":
            await help.finish("——执行——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "向服务器执行远程指令\n"
                              "用法：\n"
                              "执行 [序号] [命令]\n"
                              "参数：\n"
                              "序号 - 服务器序号\n"
                              "命令 - 需要执行的远程命令")
        elif command == "添加白名单":
            await help.finish("——添加白名单——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "向所有服务器以及数据库添加白名单\n"
                              "用法：\n"
                              "添加白名单 [昵称]\n"
                              "参数：\n"
                              "昵称 - 玩家游戏昵称")
        elif command == "删除白名单":
            await help.finish("——删除白名单——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "向所有服务器以及数据库删除白名单\n"
                              "用法：\n"
                              "删除白名单 [QQ]\n"
                              "参数：\n"
                              "QQ - 玩家绑定的QQ")
        elif command == "添加管理员":
            await help.finish("——添加管理——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "添加机器人管理员\n"
                              "用法：\n"
                              "添加管理 [QQ]\n"
                              "参数：\n"
                              "QQ - 玩家QQ")
        elif command == "删除管理员":
            await help.finish("——删除管理——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "删除机器人管理员\n"
                              "用法：\n"
                              "删除管理 [QQ]\n"
                              "参数：\n"
                              "QQ - 玩家QQ")
        elif command == "添加服务器":
            await help.finish("——添加服务器——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "为服务器列表添加服务器\n"
                              "用法：\n"
                              "添加服务器 [名称] [IP] [端口] [token]\n"
                              "参数：\n"
                              "名称 - 服务器名称\n"
                              "IP = 服务器IP\n"
                              "端口 - 服务器端口\n"
                              "token = 服务器token")
        elif command == "删除服务器":
            await help.finish("——删除服务器——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "删除指定的已存在于服务器列表的服务器\n"
                              "用法：\n"
                              "删除服务器 [名称]\n"
                              "参数：\n"
                              "名称 - 服务器名称")
        elif command == "重置服务器列表":
            await help.finish("——重置序号——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "删除服务器列表中的所有服务器\n"
                              "用法：\n"
                              "重置序号\n"
                              "参数：\n"
                              "无")
        elif command == "服务器列表":
            await help.finish("——服务器列表——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "获取服务器列表的所有服务器并显示IP和端口\n"
                              "用法：\n"
                              "服务器列表\n"
                              "参数：\n"
                              "无")
        elif command == "发送":
            await help.finish("——发送——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "发送消息至服务器\n"
                              "用法：\n"
                              "发送 [序号] [内容]\n"
                              "参数：\n"
                              "序号 - 服务器序号\n"
                              "内容 - 要发送的消息内容")
        elif command == "管理员列表":
            await help.finish("——管理员列表——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查看本群的机器人的管理员\n"
                              "一页最多显示20个\n"
                              "用法：\n"
                              "管理员列表 [页数]\n"
                              "参数：\n"
                              "页数 - 查看的页数，可选参数，默认为1")
        elif command == "重置白名单":
            await help.finish("——重置白名单——\n"
                              "权限：\n"
                              "超级管理员\n"
                              "介绍：\n"
                              "重置数据库中的白名单\n"
                              "用法：\n"
                              "重置白名单\n"
                              "参数：\n"
                              "无")
        elif command == "签到":
            await help.finish("——签到——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "每日签到\n"
                              "用法：\n"
                              "签到\n"
                              "参数：\n"
                              "无")
        elif command == "wiki":
            await help.finish("——wiki——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "在wiki中查询指定内容\n"
                              "用法：\n"
                              "wiki [内容]\n"
                              "参数：\n"
                              "内容 - 要查询的内容")
        elif command == f"添加{config.Currency.name}":
            await help.finish(f"——添加{config.Currency.name}——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "给指定玩家添加货币\n"
                              "用法：\n"
                              f"添加{config.Currency.name} [玩家昵称/QQ] [数量]\n"
                              "参数：\n"
                              "玩家昵称/QQ - 玩家昵称或QQ号\n"
                              "数量 - 要添加的数量")
        elif command == f"扣除{config.Currency.name}":
            await help.finish(f"——扣除{config.Currency.name}——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "扣除指定玩家的货币\n"
                              "用法：\n"
                              f"扣除{config.Currency.name} [玩家昵称/QQ] [数量]\n"
                              "参数：\n"
                              "玩家昵称/QQ - 玩家昵称或QQ号\n"
                              "数量 - 要扣除的数量")
        elif command == f"设置{config.Currency.name}":
            await help.finish(f"——设置{config.Currency.name}——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "设置指定玩家的货币数量\n"
                              "用法：\n"
                              f"设置{config.Currency.name} [玩家昵称/QQ] [数量]\n"
                              "参数：\n"
                              "玩家昵称/QQ - 玩家昵称或QQ号\n"
                              "数量 - 要设置的数量")
        elif command == "玩家信息":
            await help.finish("——玩家信息——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查询自己或指定玩家或QQ的信息\n"
                              "用法：\n"
                              "玩家信息 [玩家昵称/QQ]\n"
                              "参数：\n"
                              "玩家昵称/QQ - 可选参数 玩家昵称或QQ号 不填则查询自己")
        elif command == "云黑检测":
            await help.finish("——云黑检测——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "检测群内是否存在云黑玩家\n"
                              "用法：\n"
                              "云黑检测\n"
                              "参数：\n"
                              "无")
        elif command == "云黑信息":
            await help.finish("——云黑信息——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "查询指定QQ的云黑信息\n"
                              "用法：\n"
                              "云黑信息 [QQ]\n"
                              "参数：\n"
                              "QQ - 查询的QQ")
        elif command == "添加云黑":
            await help.finish("——添加云黑——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "添加指定QQ至云黑\n"
                              "用法：\n"
                              "添加云黑 [QQ] [原因]\n"
                              "参数：\n"
                              "QQ - 添加的QQ\n"
                              "原因 - 添加原因")
        elif command == "删除云黑":
            await help.finish("——删除云黑——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "删除云黑中的指定QQ\n"
                              "用法：\n"
                              "删除云黑 [QQ]\n"
                              "参数：\n"
                              "QQ - 删除的QQ")
        elif command == "玩家背包":
            await help.finish("——玩家背包——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查询服务器中指定玩家的背包\n"
                              "用法：\n"
                              "玩家背包 [序号] [昵称/QQ]\n"
                              "参数：\n"
                              "序号 - 服务器序号\n"
                              "昵称 - 玩家昵称 可选参数 不填则查询自己")
        elif command == "进度":
            await help.finish("——进度——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查询服务器进度\n"
                              "用法：\n"
                              "进度 [序号]\n"
                              "参数：\n"
                              "序号 - 服务器序号\n")
        elif command == "自踢":
            await help.finish("——自踢——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "将自己踢出服务器\n"
                              "用法：\n"
                              "自踢\n"
                              "参数：\n"
                              "无\n")
        elif command == "玩家邮箱":
            await help.finish("——玩家邮箱——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查询自己或指定玩家的邮箱\n"
                              "用法：\n"
                              "玩家邮箱 [QQ/昵称]\n"
                              "参数：\n"
                              "QQ/昵称 - 指定玩家的QQ或昵称 可选参数 不填则查询自己 \n")
        elif command == "添加邮件":
            await help.finish("——添加邮件——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "为指定玩家的邮箱添加邮件(物品)\n"
                              "用法：\n"
                              "添加邮箱 [QQ/昵称] [物品ID] [物品数量]\n"
                              "参数：\n"
                              "QQ/昵称 - 指定玩家的QQ或昵称\n"
                              "物品ID - 需要添加的物品的ID\n"
                              "物品数量 - 需要添加的物品的数量")
        elif command == "删除邮件":
            await help.finish("——删除邮件——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              "删除指定玩家的指定邮件(物品)\n"
                              "用法：\n"
                              "删除邮件 [QQ/昵称] [邮件序号]\n"
                              "参数：\n"
                              "QQ/昵称 - 指定玩家的QQ或昵称\n"
                              "邮件序号 - 需要删除的邮件(物品)序号")
        elif command == "发送邮件":
            await help.finish("——发送邮件——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "发送邮件至指定玩家\n"
                              "用法：\n"
                              "发送邮件 [QQ/昵称] [邮件序号]\n"
                              "参数：\n"
                              "QQ/昵称 - 指定玩家的QQ或昵称\n"
                              "邮件序号 - 需要发送的邮件(物品)序号")
        elif command == "领取邮件":
            await help.finish("——领取邮件——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "领取邮件(物品)至指定服务器的背包\n"
                              "玩家需在线\n"
                              "用法：\n"
                              "领取邮件 [服务器序号] [邮件序号]\n"
                              "参数：\n"
                              "服务器序号 - 指定的服务器序号\n"
                              "邮件序号 - 需要领取的邮件(物品)序号")
        elif command == "随机抽奖":
            await help.finish("——随机抽奖——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "随机抽奖 奖品直接发送至邮件\n"
                              f"每次抽奖需要{config.Lottery.RandomLottery.cost_money}{config.Currency.name}\n"
                              "用法：\n"
                              "随机抽奖 [次数]\n"
                              "参数：\n"
                              "次数 - 抽奖的次数")
        elif command == "回收邮件":
            await help.finish("——回收邮件——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              f"回收垃圾邮件 转化为{config.Currency.name}\n"
                              "用法：\n"
                              "回收邮件 [邮件序号]\n"
                              "参数：\n"
                              "邮件序号 - 邮件(物品)序号\n")
        elif command == "奖池列表":
            await help.finish("——奖池列表——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              f"查看所有奖池\n"
                              "用法：\n"
                              "奖池列表\n"
                              "参数：\n"
                              "无")
        elif command == "奖池":
            await help.finish("——奖池——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              f"获取奖池内容\n"
                              "用法：\n"
                              "奖池 [序号]\n"
                              "参数：\n"
                              "序号 - 奖池序号")
        elif command == "添加奖池":
            await help.finish("——添加奖池——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              f"添加指定奖池\n"
                              "用法：\n"
                              "添加奖池 [名称] [价格] [进度] [服务器ID]\n"
                              "参数：\n"
                              "名称 - 奖池名称\n"
                              "价格 - 单次抽奖价格\n"
                              "进度 - 服务器进度限制\n"
                              "服务器ID - 进度参考服务器ID")
        elif command == "删除奖池":
            await help.finish("——删除奖池——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              f"删除指定奖池\n"
                              "用法：\n"
                              "奖池 [序号]\n"
                              "参数：\n"
                              "序号 - 奖池序号")
        elif command == "添加奖池物品":
            await help.finish("——添加奖池物品——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              f"添加指定奖池物品\n"
                              "用法：\n"
                              "添加奖池物品 [序号] [物品ID] [最大数量] [最小数量] [概率]\n"
                              "参数：\n"
                              "序号 - 奖池序号\n"
                              "物品ID - 物品ID\n"
                              "最大数量 - 获得最大数量\n"
                              "最小数量 - 获得最小数量\n"
                              "概率 - 内部概率")
        elif command == "删除奖池物品":
            await help.finish("——删除奖池物品——\n"
                              "权限：\n"
                              "管理员\n"
                              "介绍：\n"
                              f"删除指定奖池物品\n"
                              "用法：\n"
                              "删除奖池物品 [序号]\n"
                              "参数：\n"
                              "序号 - 奖池物品序号")
        elif command == "奖池抽奖":
            await help.finish("——奖池抽奖——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              f"指定奖池抽奖\n"
                              "用法：\n"
                              "奖池抽奖 [序号] [次数]\n"
                              "参数：\n"
                              "序号 - 奖池物品\n"
                              "次数 - 抽奖次数")
    else:
        await help.finish("执行失败，用法错误\n请输入【帮助 帮助】 获取该功能更多信息")
