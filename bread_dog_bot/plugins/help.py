from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event

help = on_command("帮助")


@help.handle()
async def help_handle(bot: Bot, event: Event):
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
                              "下划线(_)代替空格\n"
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
                              "发送消息 [序号] [内容]\n"
                              "参数：\n"
                              "序号 - 服务器序号\n"
                              "内容 - 要发送的消息内容")
        elif command == "白名单列表":
            await help.finish("——白名单列表——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查看数据库中的白名单\n"
                              "用法：\n"
                              "白名单列表\n"
                              "参数：\n"
                              "无")
        elif command == "管理员列表":
            await help.finish("——管理员列表——\n"
                              "权限：\n"
                              "无\n"
                              "介绍：\n"
                              "查看机器人的管理员\n"
                              "用法：\n"
                              "管理员列表\n"
                              "参数：\n"
                              "无")
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
    else:
        await help.finish("执行失败，用法错误\n请输入【帮助 帮助】 获取该功能更多信息")
