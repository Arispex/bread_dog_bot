import math

from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message, GroupMessageEvent
import models.player
import config
from nonebot import require
import utils.server
import utils.admin
import utils.whitelist
import models.server
from PIL import Image, ImageChops, ImageDraw, ImageFont
import time
import os
import utils.prize_pool
import models.prize_pool
import utils.admin

random_lottery = on_command("随机抽奖")


@random_lottery.handle()
async def random_lottery_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        count = text[1]

        if not count.isdigit():
            await random_lottery.finish("抽奖失败！\n无效的参数\n次数必须是数字")
        else:
            count = int(count)

        qq = event.get_user_id()
        player = models.player.Player(qq)
        result, lottery_result = player.random_lottery(count)
        group_info = await bot.get_group_info(group_id=event.group_id)
        if result:
            img = Image.open("img/lottery_bg.png")
            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
            draw = ImageDraw.Draw(img)
            w, h = img.size
            text_w, text_h = ft.getsize(group_info["group_name"])
            draw.text(((w - text_w) / 2, 0), group_info["group_name"], font=ft)

            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
            draw = ImageDraw.Draw(img)
            text_w, text_h = ft.getsize(f"{player.name}({player.qq})的随机抽奖")
            draw.text(((w - text_w) / 2, 150), f"{player.name}({player.qq})的随机抽奖", font=ft)

            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
            draw = ImageDraw.Draw(img)
            draw.text((10, 1040), "Developed by Qianyi", font=ft)
            draw.text((300, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)
            w, h = ft.getsize(f"QQ群：{group_info['group_name']}({group_info['group_id']})")
            draw.text((img.width - w - 10, 10), f"QQ群：{group_info['group_name']}({group_info['group_id']})", font=ft)
            draw.text((650, 1040), f"次数：{count}    "
                                   f"花费{config.Currency.name}：{config.Lottery.RandomLottery.cost_money * count}    "
                                   f"剩余{config.Currency.name}：{player.money}", font=ft)

            row = 0
            column = 0
            for i in lottery_result:
                item_bg = Image.new("RGBA", (200, 200))
                item_img = Image.open(f"img/item/item_{i[0]}.png")
                item_img = item_img.resize((item_img.width * 2, item_img.height * 2))
                r, g, b, a = item_img.split()
                item_bg.paste(item_img, (round((200 - item_img.width) / 2), round((150 - item_img.height) / 2)), mask=a)
                ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=30)
                draw = ImageDraw.Draw(item_bg)
                if i[1] != 1:
                    draw.text((100, 100), str(i[1]), font=ft)

                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                text_w, text_h = ft.getsize(i[2][:6])
                draw.text(((item_bg.width - text_w) / 2, 150), i[2][:6], font=ft, fill="white")
                img.paste(item_bg, (120 + row * 370, 300 + column * 370), mask=item_bg)

                if row == 4:
                    row = 0
                    column += 1
                else:
                    row += 1

            img.save("img/lottery.png")
            if os.name == "nt":  # windows
                await random_lottery.finish(
                    MessageSegment.image("file:///" + os.getcwd() + "\\img\\lottery.png"))
            else:  # linux
                await random_lottery.finish(
                    Message(MessageSegment.image("file://" + os.getcwd() + "/img/lottery.png")))
        else:
            await random_lottery.finish(f"抽奖失败！\n{lottery_result}")
    else:
        await random_lottery.finish("抽奖失败！\n用法错误！\n请输入【帮助 随机抽奖】获取该功能更多信息")


prize_pool_list = on_command("奖池列表")


@prize_pool_list.handle()
async def prize_pool_list_handle(bot: Bot, event: GroupMessageEvent):
    if event.get_plaintext() == "奖池列表":
        result, prize_pools = utils.prize_pool.GetInfo.all()
        if result:
            if len(prize_pools) == 0:
                await prize_pool_list.finish("群主很懒，暂时还没有添加奖池！")
            msg_list = [f"๑{i[0]}๑{MessageSegment.face(89)}{i[1]}" for i in prize_pools]
            await prize_pool_list.finish(Message("\n".join(msg_list)))
        else:
            await prize_pool_list.finish(f"获取失败！\n{prize_pools}")


add_prize_pool = on_command("添加奖池")


@add_prize_pool.handle()
async def add_prize_pool_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 5:
            name = text[1]
            price = text[2]
            progress = text[3]
            progress_server = text[4]

            if not name.isalnum():
                await add_prize_pool.finish("抽奖失败！\n无效的参数\n奖池名称不能包含特殊字符")

            if not price.isdigit():
                await add_prize_pool.finish("抽奖失败！\n无效的参数\n价格必须为数字")
            else:
                price = int(price)

            if not progress.isalpha():
                await add_prize_pool.finish("抽奖失败！\n无效的参数\n进度限制必须为中文")

            if not progress_server.isdigit():
                await add_prize_pool.finish("抽奖失败！\n无效的参数\n进度参照服务器ID必须为数字")
            else:
                progress_server = int(progress_server)

            result, reason = utils.prize_pool.add(name, price, progress, progress_server)
            if result:
                await add_prize_pool.finish("添加成功！")
            else:
                await add_prize_pool.finish(f"添加失败！\n{reason}")
        else:
            await add_prize_pool.finish("添加失败！\n用法错误！\n请输入【帮助 添加奖池】获取该功能更多信息")
    else:
        await add_prize_pool.finish("添加失败！\n权限不足！\n请输入【帮助 添加奖池】获取该功能更多信息")


sub_prize_pool = on_command("删除奖池")


@sub_prize_pool.handle()
async def sub_prize_pool_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            prize_pool_name = text[1]

            if not prize_pool_name.isalnum():
                await add_prize_pool.finish("抽奖失败！\n无效的参数\n奖池名称不能包含特殊字符")

            result, reason = utils.prize_pool.delete(prize_pool_name)
            if result:
                await sub_prize_pool.finish("删除成功！")
            else:
                await sub_prize_pool.finish(f"删除失败！\n{reason}")
        else:
            await sub_prize_pool.finish("删除失败！\n用法错误！\n请输入【帮助 删除奖池】获取该功能更多信息")
    else:
        await sub_prize_pool.finish("删除失败！\n权限不足！\n请输入【帮助 删除奖池】获取该功能更多信息")


add_prize_pool_item = on_command("添加奖池物品")


@add_prize_pool_item.handle()
async def add_prize_pool_item_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 6:
            prize_pool_id = text[1]
            item_id = text[2]
            item_max_amount = text[3]
            item_min_amount = text[4]
            probability = text[5]

            if not prize_pool_id.isdigit():
                await add_prize_pool_item.finish("抽奖失败！\n无效的参数\n奖池ID必须为数字")
            else:
                prize_pool_id = int(prize_pool_id)

            if not item_id.isdigit():
                await add_prize_pool_item.finish("抽奖失败！\n无效的参数\n物品ID必须为数字")
            else:
                item_id = int(item_id)

            if not item_max_amount.isdigit():
                await add_prize_pool_item.finish("抽奖失败！\n无效的参数\n物品最大数量必须为数字")
            else:
                item_max_amount = int(item_max_amount)

            if not item_min_amount.isdigit():
                await add_prize_pool_item.finish("抽奖失败！\n无效的参数\n物品最小数量必须为数字")
            else:
                item_min_amount = int(item_min_amount)

            if not probability.isdigit():
                await add_prize_pool_item.finish("抽奖失败！\n无效的参数\n概率必须为数字")
            else:
                probability = int(probability)

            prize_pool = models.prize_pool.PrizePool(prize_pool_id)
            result, reason = prize_pool.add(item_id, item_max_amount, item_min_amount, probability)
            if result:
                await add_prize_pool_item.finish("添加成功！")
            else:
                await add_prize_pool_item.finish(f"添加失败！\n{reason}")
        else:
            await add_prize_pool_item.finish("添加失败！\n用法错误！\n请输入【帮助 添加奖池物品】获取该功能更多信息")
    else:
        await add_prize_pool_item.finish("添加失败！\n权限不足！\n请输入【帮助 添加奖池物品】获取该功能更多信息")


del_prize_pool_item = on_command("删除奖池物品")


@del_prize_pool_item.handle()
async def del_prize_pool_item_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    if event.get_user_id() in admins:
        text = event.get_plaintext().split(" ")
        if len(text) == 3:
            prize_pool_id = text[1]
            item_sn = text[2]

            if not prize_pool_id.isdigit():
                await del_prize_pool_item.finish("抽奖失败！\n无效的参数\n奖池ID必须为数字")
            else:
                prize_pool_id = int(prize_pool_id)

            if not item_sn.isdigit():
                await del_prize_pool_item.finish("抽奖失败！\n无效的参数\n物品序号必须为数字")
            else:
                item_sn = int(item_sn)

            prize_pool = models.prize_pool.PrizePool(prize_pool_id)
            result, reason = prize_pool.delete(item_sn)
            if result:
                await del_prize_pool_item.finish("删除成功！")
            else:
                await del_prize_pool_item.finish(f"删除失败！\n{reason}")
        else:
            await del_prize_pool_item.finish("删除失败！\n用法错误！\n请输入【帮助 删除奖池物品】获取该功能更多信息")
    else:
        await del_prize_pool_item.finish("删除失败！\n权限不足！\n请输入【帮助 删除奖池物品】获取该功能更多信息")


check_prize_pool = on_command("奖池")


@check_prize_pool.handle()
async def check_prize_pool_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 2 or len(text) == 3:
        if len(text) == 2:
            page = 1
        else:
            if text[2].isdigit():
                page = int(text[2])
            else:
                await check_prize_pool.finish("查询失败！\n无效的参数\n页数必须为数字")

        prize_pool_id = text[1]

        if not prize_pool_id.isdigit():
            await check_prize_pool.finish("查询失败！\n无效的参数\n奖池ID必须为数字")
        else:
            prize_pool_id = int(prize_pool_id)

        prize_pool = models.prize_pool.PrizePool(prize_pool_id)

        if not prize_pool.status:
            await check_prize_pool.finish(f"查询失败！\n{prize_pool.error}")

        items = prize_pool.content
        total_probability = prize_pool.total_probability
        total_page = math.ceil(len(items) / 20)
        group_info = await bot.get_group_info(group_id=event.group_id)
        result, server_info = utils.server.GetInfo.by_id(prize_pool.progress_server)

        if not result:
            await check_prize_pool.finish(f"查询失败！\n{server_info}")

        if total_page == 0:
            await check_prize_pool.finish(f"群主很懒，还没有添加物品！")

        if page > total_page:
            await check_prize_pool.finish(f"查询失败！\n无效的页数\n总页数为{total_page}")

        img = Image.open("img/prize_pool_bg.png")
        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
        draw = ImageDraw.Draw(img)
        w, h = img.size
        text_w, text_h = ft.getsize(group_info["group_name"])
        draw.text(((w - text_w) / 2, 0), group_info["group_name"], font=ft)

        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
        draw = ImageDraw.Draw(img)
        text_w, text_h = ft.getsize("奖池")
        draw.text(((w - text_w) / 2, 150), "奖池", font=ft)

        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
        draw = ImageDraw.Draw(img)
        draw.text((10, 1040), "Developed by Qianyi", font=ft)
        draw.text((300, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)
        draw.text((650, 1040), f"奖池ID：{prize_pool.id}    "
                               f"奖池名称：{prize_pool.name}    "
                               f"进度限制：{prize_pool.progress_zh}    "
                               f"进度参照：{server_info[1]}({server_info[0]})    "
                               f"价格：{prize_pool.price}{config.Currency.name}/次", font=ft)
        draw.text((10, 10), f"当前页数：{page}/{total_page}", font=ft)
        w, h = ft.getsize(f"QQ群：{group_info['group_name']}({group_info['group_id']})")
        draw.text((img.width - w - 10, 10), f"QQ群：{group_info['group_name']}({group_info['group_id']})", font=ft)

        row = 0
        column = 0
        begin = 0
        for i in items[(page - 1) * 20:page * 20]:
            item_bg = Image.new("RGBA", (300, 150), (255, 255, 255, 120))
            item_img = Image.open(f"img/item/item_{i['item_id']}.png")
            item_img = item_img.resize((item_img.width * 2, item_img.height * 2))
            r, g, b, a = item_img.split()
            item_bg.paste(item_img, (round((150 - item_img.width) / 2), round((item_bg.height - item_img.height) / 2)),
                          mask=a)
            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=20)
            draw = ImageDraw.Draw(item_bg)
            draw.text((150, 10), f"序号：{items.index(i, begin) + 1}", font=ft, fill=(255, 255, 255, 255))
            begin = items.index(i, begin)
            draw.text((150, 30), f"物品ID：{i['item_id']}", font=ft, fill=(0, 0, 0, 255))
            draw.text((150, 50), f"最大数量：{i['item_max_amount']}", font=ft, fill=(0, 0, 0, 255))
            draw.text((150, 70), f"最小数量：{i['item_min_amount']}", font=ft, fill=(0, 0, 0, 255))
            draw.text((150, 90), f"概率：{round((i['item_probability'] / total_probability) * 100, 2)}%", font=ft,
                      fill=(0, 0, 0, 255))
            draw.text((150, 110), f"内部概率：{i['item_probability']}", font=ft, fill=(0, 0, 0, 255))

            img.paste(item_bg, (70 + row * 370, 300 + column * 170), mask=item_bg)

            if row == 4:
                row = 0
                column += 1
            else:
                row += 1

        img.save("img/prize_pool.png")

        if os.name == "nt":  # windows
            await check_prize_pool.finish(MessageSegment.image("file:///" + os.getcwd() + "\\img\\prize_pool.png"))
        else:  # linux
            await check_prize_pool.finish(MessageSegment.image("file://" + os.getcwd() + "/img/prize_pool.png"))
    else:
        await check_prize_pool.finish("查询失败！\n用法错误！\n请输入【帮助 奖池】获取该功能更多信息")


prize_pool_lottery = on_command("奖池抽奖")


@prize_pool_lottery.handle()
async def prize_pool_lottery_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 3:
        prize_pool_id = text[1]
        count = text[2]

        if not prize_pool_id.isdigit():
            await prize_pool_lottery.finish("抽奖失败！\n无效的参数\n奖池ID必须为数字")
        else:
            prize_pool_id = int(prize_pool_id)

        if not count.isdigit():
            await prize_pool_lottery.finish("抽奖失败！\n无效的参数\n抽奖次数必须为数字")
        else:
            count = int(count)

        player = models.player.Player(event.get_user_id())
        prize_pool = models.prize_pool.PrizePool(prize_pool_id)
        result, lottery_result = player.prize_pool_lottery(prize_pool_id, count)

        group_info = await bot.get_group_info(group_id=event.group_id)
        if result:
            img = Image.open("img/lottery_bg.png")
            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
            draw = ImageDraw.Draw(img)
            w, h = img.size
            text_w, text_h = ft.getsize(group_info["group_name"])
            draw.text(((w - text_w) / 2, 0), group_info["group_name"], font=ft)

            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
            draw = ImageDraw.Draw(img)
            text_w, text_h = ft.getsize(f"{player.name}({player.qq})的奖池抽奖")
            draw.text(((w - text_w) / 2, 150), f"{player.name}({player.qq})的奖池抽奖", font=ft)

            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
            draw = ImageDraw.Draw(img)
            draw.text((10, 1040), "Developed by Qianyi", font=ft)
            draw.text((300, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)
            w, h = ft.getsize(f"QQ群：{group_info['group_name']}({group_info['group_id']})")
            draw.text((img.width - w - 10, 10), f"QQ群：{group_info['group_name']}({group_info['group_id']})", font=ft)
            draw.text((650, 1040), f"奖池ID：{prize_pool.id}    "
                                   f"奖池名称：{prize_pool.name}    "
                                   f"次数：{count}    "
                                   f"花费{config.Currency.name}：{prize_pool.price * count}    "
                                   f"剩余{config.Currency.name}：{player.money}", font=ft)

            row = 0
            column = 0
            for i in lottery_result:
                item_bg = Image.new("RGBA", (200, 200))
                item_img = Image.open(f"img/item/item_{i[0]}.png")
                item_img = item_img.resize((item_img.width * 2, item_img.height * 2))
                r, g, b, a = item_img.split()
                item_bg.paste(item_img, (round((200 - item_img.width) / 2), round((150 - item_img.height) / 2)), mask=a)
                ft = ImageFont.truetype(font="font/JetBrainsMono-Bold-Italic.ttf", size=30)
                draw = ImageDraw.Draw(item_bg)
                if i[1] != 1:
                    draw.text((100, 100), str(i[1]), font=ft)

                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                text_w, text_h = ft.getsize(i[2][:6])
                draw.text(((item_bg.width - text_w) / 2, 150), i[2][:6], font=ft, fill="white")
                img.paste(item_bg, (120 + row * 370, 300 + column * 370), mask=item_bg)

                if row == 4:
                    row = 0
                    column += 1
                else:
                    row += 1

            img.save("img/lottery.png")
            if os.name == "nt":  # windows
                await prize_pool_lottery.finish(
                    MessageSegment.image("file:///" + os.getcwd() + "\\img\\lottery.png"))
            else:  # linux
                await prize_pool_lottery.finish(
                    Message(MessageSegment.image("file://" + os.getcwd() + "/img/lottery.png")))
        else:
            await prize_pool_lottery.finish(f"抽奖失败！\n{lottery_result}")
    else:
        await prize_pool_lottery.finish("抽奖失败！\n用法错误！\n请输入【帮助 奖池抽奖】获取该功能更多信息")
