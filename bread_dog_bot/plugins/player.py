from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent
import models.player
import config
from nonebot import require
import utils.server
import utils.admin
import utils.whitelist

sign_in = on_command("签到")


@sign_in.handle()
async def sign_in_handle(bot: Bot, event: Event):
    player = models.player.Player(event.get_user_id())
    if player.status_code:
        result, get_money = player.sign_in()
        if result:
            result, player_sign_in_log = player.get_sign_in_log()
            if get_money > config.SignIn.max_money / 2:
                msg = "哇，今天你的运气看起来不错哦！"
            else:
                msg = "摸摸头，今天你的运气似乎不佳，没关系，明天再来！"
            await sign_in.finish(Message(f"{MessageSegment.at(event.get_user_id())}\n签到成功！\n"
                                         f"{msg}\n"
                                         f"获得{config.Currency.name}：{get_money}\n"
                                         f"当前{config.Currency.name}：{player.money}\n签到排名：{player_sign_in_log[0]}"))
        else:
            msg = "摸摸头，今天你已经签到过了哦！"
            result, player_sign_in_log = player.get_sign_in_log()
            await sign_in.finish(Message(f"{MessageSegment.at(event.get_user_id())}\n签到失败！\n"
                                         f"{msg}\n"
                                         f"获得{config.Currency.name}：{player_sign_in_log[2]}\n"
                                         f"当前{config.Currency.name}：{player.money}\n签到排名：{player_sign_in_log[0]}"))
    else:
        if player.player_info == "不存在此玩家":
            player.player_info = "您还没有添加白名单"
        await sign_in.finish(Message(f"{MessageSegment.at(event.get_user_id())}\n签到失败！\n{player.player_info}"))


scheduler = require('nonebot_plugin_apscheduler').scheduler


# 设置在几点启动脚本
@scheduler.scheduled_job('cron', hour='0', minute='0')
# 启动的脚本
async def reset_sign_in():
    utils.server.execute_sql("UPDATE whitelist SET signIn = 0")
    utils.server.execute_sql("delete from signInLog")
    utils.server.execute_sql("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'signInLog'")


add_money = on_command(f"添加{config.Currency.name}")


@add_money.handle()
async def add_money_handle(bot: Bot, event: Event):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]
            player = models.player.Player(qq)
            result, player_money = player.add_money(int(money))
            if result:
                await add_money.finish(Message(f"添加成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
            else:
                await add_money.finish(Message(f"添加失败！\n{player_money}"))
        else:
            await add_money.finish(Message(f"添加失败！\n用法错误！\n请输入【帮助 添加{config.Currency.name}】获取该功能更多信息"))
    else:
        await add_money.finish(Message(f"添加失败！\n权限不足！\n请输入【帮助 添加{config.Currency.name}】获取该功能更多信息"))


sub_money = on_command(f"扣除{config.Currency.name}")


@sub_money.handle()
async def sub_money_handle(bot: Bot, event: Event):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]
            player = models.player.Player(qq)
            result, player_money = player.sub_money(int(money))
            if result:
                await sub_money.finish(Message(f"扣除成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
            else:
                await sub_money.finish(Message(f"扣除失败！\n{player_money}"))
        else:
            await sub_money.finish(Message(f"扣除失败！\n用法错误！\n请输入【帮助 扣除{config.Currency.name}】获取该功能更多信息"))
    else:
        await sub_money.finish(Message(f"扣除失败！\n权限不足！\n请输入【帮助 扣除{config.Currency.name}】获取该功能更多信息"))


set_money = on_command(f"设置{config.Currency.name}")


@set_money.handle()
async def set_money_handle(bot: Bot, event: Event):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]
            player = models.player.Player(qq)
            result, player_money = player.set_money(int(money))
            if result:
                await set_money.finish(Message(f"设置成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
            else:
                await set_money.finish(Message(f"设置失败！\n{player_money}"))
        else:
            await set_money.finish(Message(f"设置失败！\n用法错误！\n请输入【帮助 设置{config.Currency.name}】获取该功能更多信息"))
    else:
        await set_money.finish(Message(f"设置失败！\n权限不足！\n请输入【帮助 设置{config.Currency.name}】获取该功能更多信息"))


player_info = on_command(f"玩家信息")


@player_info.handle()
async def player_info_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
        player = models.player.Player(qq)
        if player.status_code:
            await player_info.finish(Message(f"玩家昵称：{player.name}\n绑定QQ：{player.qq}\n"
                                             f"拥有{config.Currency.name}：{player.money}\n"
                                             f"获取时间：{player.get_time}"))
        else:
            await player_info.finish(Message(f"查询失败！\n{player.reason}"))
    elif len(text) == 1:
        player = models.player.Player(event.get_user_id())
        if player.status_code:
            await player_info.finish(Message(f"玩家昵称：{player.name}\n绑定QQ：{player.qq}\n"
                                             f"拥有{config.Currency.name}：{player.money}\n"
                                             f"获取时间：{player.get_time}"))
        else:
            await player_info.finish(Message(f"查询失败！\n{player.reason}"))
    else:
        await player_info.finish(Message(f"查询失败！\n用法错误！\n请输入【帮助 玩家信息】获取该功能更多信息"))