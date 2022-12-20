import os
import time

from PIL import Image, ImageDraw, ImageFont
from nonebot import on_command, logger
from nonebot import require
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent

import config
import models.player
import models.server
import utils.admin
import utils.server
import utils.whitelist

self_kick = on_command("自踢", aliases={"自提"})


@self_kick.handle()
async def self_kick_handle(bot: Bot, event: Event):
    if event.get_plaintext() == "自踢" or event.get_plaintext() == "自提":
        logger.info(f"「{event.get_user_id()}」执行了 「自踢」")
        result, server_info_list = utils.server.GetInfo.all()
        player = models.player.Player(event.get_user_id())
        if player.status_code:
            if result:
                for i in server_info_list:
                    conn = models.server.Connect(i[2], i[3], i[4])
                    result, player_list = conn.kick(player.name, "在群中使用自踢")
            await self_kick.finish(Message("你已被踢出所有可用服务器!"))
    else:
        await self_kick.finish(Message("你没有添加白名单!"))


sign_in = on_command("签到")


@sign_in.handle()
async def sign_in_handle(bot: Bot, event: Event):
    if event.get_plaintext() == "签到":
        logger.info(f"「{event.get_user_id()}」执行了 「签到」")
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
                logger.info(f"「{event.get_user_id()}」签到成功 获得{config.Currency.name}：{get_money} 签到排名：{player_sign_in_log[0]}")
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
        logger.info(f"「{event.get_user_id()}」执行了 「添加{config.Currency.name}」")
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]

            if not money.isdigit():
                await add_money.finish(f"添加失败！\n无效的参数\n{config.Currency.name}数量必须为数字")
            else:
                money = int(money)

            player = models.player.Player(qq)
            result, player_money = player.add_money(money)
            if result:
                await add_money.finish(Message(f"添加成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
                logger.info(f"「{event.get_user_id()}」给 「{player.name}({player.qq})」添加了 {money} {config.Currency.name}")
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
        logger.info(f"「{event.get_user_id()}」执行了 「扣除{config.Currency.name}」")
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]

            if not money.isdigit():
                await add_money.finish(f"添加失败！\n无效的参数\n{config.Currency.name}数量必须为数字")
            else:
                money = int(money)

            player = models.player.Player(qq)
            result, player_money = player.sub_money(money)
            if result:
                await sub_money.finish(Message(f"扣除成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
                logger.info(f"「{event.get_user_id()}」扣除了 「{player.name}({player.qq})」 {money} {config.Currency.name}")
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
        logger.info(f"「{event.get_user_id()}」执行了 「设置{config.Currency.name}」")
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            money = text[2]

            if not money.isdigit():
                await add_money.finish(f"添加失败！\n无效的参数\n{config.Currency.name}数量必须为数字")
            else:
                money = int(money)

            player = models.player.Player(qq)
            result, player_money = player.set_money(money)
            if result:
                await set_money.finish(Message(f"设置成功！\n该玩家剩余{config.Currency.name}：{player_money}"))
                logger.info(f"「{event.get_user_id()}」给 「{player.name}({player.qq})」 设置了 {money} {config.Currency.name}")
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
    logger.info(f"「{event.get_user_id()}」执行了 「玩家信息」")
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


player_inventory = on_command(f"玩家背包")


@player_inventory.handle()
async def player_inventory_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    logger.info(f"「{event.get_user_id()}」执行了 「玩家背包」")
    if (len(text) == 3) or (len(text) == 2):
        if len(text) == 3:
            num = text[1]
            name = text[2]
        elif len(text) == 2:
            num = text[1]
            name = event.get_user_id()
        else:
            await player_inventory.finish(Message(f"查询失败！\n用法错误！\n请输入【帮助 玩家背包】获取该功能更多信息"))
        result, server_info = utils.server.GetInfo.by_id(int(num))
        if result:
            server = models.server.Connect(server_info[2], server_info[3], server_info[4])
            result, response = server.player_inventory(name)
            if not result:
                if isinstance(response, str):
                    await player_inventory.finish(Message(f"查询失败！\n{response}"))
                elif response["status"] == "500":
                    result, player_info = utils.whitelist.GetInfo.by_qq(name)
                    if result:
                        result, response = server.player_inventory(player_info[2])
                        name = player_info[2]
                    else:
                        await player_inventory.finish(Message(f"查询失败！\n不存在此玩家"))
                else:
                    await player_inventory.finish(Message(f"查询失败！\n{response['error']}"))
            if result:
                inventory = []
                for i in response["response"]:
                    inventory.append([i["netID"], i["stack"]])
                bg = Image.open("img/inventory_bg.png").convert("RGBA")

                # 背包 0-49
                row = 0
                column = 0
                for i in inventory[:50]:
                    if int(i[0]) < 0:
                        row += 1
                        continue
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (33 + row * 79, 5 + column * 79), mask=a)
                    if row == 9:
                        row = 0
                        column += 1
                    else:
                        row += 1

                # 金币 50-53
                column = 0
                for i in inventory[50:54]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
                    img.paste(item, (round((40 - item.width) / 2), round((40 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=15)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((30, 30), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (820, 140 + column * 55), mask=a)
                    column += 1

                # 弹药 54-57
                column = 0
                for i in inventory[54:58]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
                    img.paste(item, (round((40 - item.width) / 2), round((40 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=15)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((30, 30), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (882, 140 + column * 55), mask=a)
                    column += 1

                # 垃圾桶 58
                for i in inventory[58:59]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (745, 400), mask=a)

                # 护甲 59 - 61
                column = 0
                for i in inventory[59:62]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (1115, 65 + column * 79), mask=a)
                    column += 1

                # 饰品 62 - 68
                column = 0
                for i in inventory[62:69]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (1115, 310 + column * 79), mask=a)
                    column += 1

                # 护甲装饰 69 - 71
                column = 0
                for i in inventory[69:72]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (1035, 65 + column * 79), mask=a)
                    column += 1

                # 饰品装饰 72 - 78
                column = 0
                for i in inventory[72:79]:
                    try:
                        item = Image.open(f"img/item/Item_{i[0]}.png").convert("RGBA")
                    except FileNotFoundError:
                        item = Image.open(f"img/item/Item_0.png").convert("RGBA")
                    img = Image.new("RGBA", (50, 50), (0, 0, 0, 0))
                    img.paste(item, (round((50 - item.width) / 2), round((50 - item.height) / 2)))
                    img = img.resize((round(img.width * 1.5), (round(img.height * 1.5))))
                    ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
                    draw = ImageDraw.Draw(img)
                    if i[1] != 1 and i[1] != 0:
                        draw.text((40, 40), str(i[1]), font=ft)
                    r, g, b, a = img.split()
                    bg.paste(img, (1035, 310 + column * 79), mask=a)
                    column += 1

                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=50)
                draw = ImageDraw.Draw(bg)
                draw.text((150, 450), f"{server_info[1]}\nQQ群：{event.group_id}\n玩家昵称：{name}", font=ft)
                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=20)
                draw.text((10, 680), "Developed by Qianyi", font=ft)
                draw.text((210, 680), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)
                bg.save("img/inventory.png", format="PNG")
                if os.name == "nt":  # windows
                    await player_inventory.finish(
                        MessageSegment.image("file:///" + os.getcwd() + "\\img\\inventory.png"))
                else:  # linux
                    await player_inventory.finish(
                        Message(MessageSegment.image("file://" + os.getcwd() + "/img/inventory.png")))
            else:
                if isinstance(response, str):
                    await player_inventory.finish(Message(f"查询失败！\n{response}"))
                elif response["status"] == "500":
                    await player_inventory.finish(Message(f"查询失败！\n不存在此玩家"))
                else:
                    await player_inventory.finish(Message(f"查询失败！\n{response['error']}"))
        else:
            await player_inventory.finish(Message(f"查询失败！\n找不到序号为 {num} 的服务器"))
    else:
        await player_inventory.finish(Message(f"查询失败！\n用法错误！\n请输入【帮助 玩家背包】获取该功能更多信息"))
