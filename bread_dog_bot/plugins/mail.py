import json
import time
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent

import config
import models.player
from PIL import Image, ImageChops, ImageDraw, ImageFont
import os
import utils.admin
import utils.server

mail = on_command("玩家邮箱")


@mail.handle()
async def mail_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
    elif len(text) == 1:
        qq = event.get_user_id()
    else:
        await mail.finish("获取失败！\n用法错误！\n请输入【帮助 玩家邮箱】获取该功能更多信息")

    player = models.player.Player(qq)
    result, player_mail = player.get_mail()
    if result:
        group_info = await bot.get_group_info(group_id=event.group_id)

        img = Image.open("img/mail_bg.png")
        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        text_w, text_h = ft.getsize(group_info["group_name"])
        draw.text(((w - text_w) / 2, 0), group_info["group_name"], font=ft)

        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
        draw = ImageDraw.Draw(img)
        text_w, text_h = ft.getsize(f"{player.name}的邮箱({player.qq})")
        draw.text(((w - text_w) / 2, 150), f"{player.name}的邮箱({player.qq})", font=ft)

        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
        draw = ImageDraw.Draw(img)
        draw.text((10, 1040), "Developed by Qianyi", font=ft)
        draw.text((300, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)

        row = 0
        column = 0
        num = 1
        for i in player_mail:
            item_bg = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
            item_img = Image.open(f"img/item/item_{i[0]}.png")
            item_img = item_img.resize((item_img.width * 2, item_img.height * 2))
            r, g, b, a = item_img.split()
            item_bg.paste(item_img, (round((150 - item_img.width) / 2), round((150 - item_img.height) / 2)), mask=a)
            ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=30)
            draw = ImageDraw.Draw(item_bg)
            if i[1] != 1:
                draw.text((100, 100), str(i[1]), font=ft)
            ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=20)
            draw.text((10, 10), str(num), font=ft)
            img.paste(item_bg, (85 + row * 200, 300 + column * 200), mask=item_bg)

            if row == 8:
                row = 0
                column += 1
            else:
                row += 1
            num += 1

        img.save("img/mail.png")

        if os.name == "nt":  # windows
            await mail.finish(
                MessageSegment.image("file:///" + os.getcwd() + "\\img\\mail.png"))
        else:  # linux
            await mail.finish(
                Message(MessageSegment.image("file://" + os.getcwd() + "/img/mail.png")))
    else:
        await mail.finish(f"获取失败！\n{player_mail}")


add_mail = on_command("添加邮件")


@add_mail.handle()
async def add_mail_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 4:
            qq = text[1]
            item_id = text[2]
            item_num = text[3]

            player = models.player.Player(qq)
            result, reason = player.add_mail(int(item_id), int(item_num))
            if result:
                await add_mail.finish(f"添加成功！")
            else:
                await add_mail.finish(f"添加失败！\n{reason}")
        else:
            await add_mail.finish("添加失败！\n用法错误！\n请输入【帮助 添加邮件】获取该功能更多信息")
    else:
        await add_mail.finish("添加失败！\n权限不足！\n请输入【帮助 添加邮件】获取该功能更多信息")


sub_mail = on_command("删除邮件")


@sub_mail.handle()
async def sub_mail_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            qq = text[1]
            item_sn = text[2]

            player = models.player.Player(qq)
            result, reason = player.empty_mail(int(item_sn))
            if result:
                await sub_mail.finish("删除成功！")
            else:
                await sub_mail.finish(f"删除失败！\n{reason}")

        else:
            await sub_mail.finish("删除失败！\n用法错误！\n请输入【帮助 删除邮件】获取该功能更多信息")
    else:
        await sub_mail.finish("删除失败！\n权限不足！\n请输入【帮助 删除邮件】获取该功能更多信息")


send_mail = on_command("发送邮件")


@send_mail.handle()
async def send_mail_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 3:
        qq = text[1]
        item_sn = text[2]

        player = models.player.Player(event.get_user_id())
        result, reason = player.send_mail(qq, int(item_sn))
        if result:
            await send_mail.finish("发送成功！")
        else:
            await send_mail.finish(f"发送失败！\n{reason}")
    else:
        await sub_mail.finish("发送失败！\n用法错误！\n请输入【帮助 发送邮件】获取该功能更多信息")


pick_up_mail = on_command("领取邮件")


@pick_up_mail.handle()
async def pick_up_mail_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 3:
        server_num = text[1]
        item_sn = text[2]

        if not item_sn.isdigit():
            await pick_up_mail.finish("领取失败！\n物品编号错误！")
        player = models.player.Player(event.get_user_id())
        result, server_info = utils.server.GetInfo.by_id(int(server_num))
        if result:
            result, reason = player.pick_up_mail(int(item_sn), *server_info[2:])
            if result:
                await pick_up_mail.finish("领取成功！")
            else:
                await pick_up_mail.finish(f"领取失败！\n{reason}")
        else:
            await pick_up_mail.finish(f"领取失败！\n{server_info}")
    else:
        await pick_up_mail.finish("领取失败！\n用法错误！\n请输入【帮助 领取邮件】获取该功能更多信息")


recycle_mail = on_command("回收邮件")


@recycle_mail.handle()
async def recycle_mail_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        item_sn = text[1]

        if not item_sn.isdigit():
            await pick_up_mail.finish("领取失败！\n物品编号错误！")

        player = models.player.Player(event.get_user_id())
        result, reason = player.recycle_mail(int(item_sn))
        if result:
            await recycle_mail.finish(f"回收成功！\n获得{config.Currency.name}：{reason}")
        else:
            await recycle_mail.finish(f"回收失败！\n{reason}")
    else:
        await recycle_mail.finish("回收失败！\n用法错误！\n请输入【帮助 回收邮件】获取该功能更多信息")
