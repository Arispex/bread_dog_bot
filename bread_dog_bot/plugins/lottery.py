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


random_lottery = on_command("随机抽奖")


@random_lottery.handle()
async def random_lottery_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        count = int(text[1])
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
            text_w, text_h = ft.getsize(f"{player.name}的随机抽奖({player.qq})")
            draw.text(((w - text_w) / 2, 150), f"{player.name}的随机抽奖({player.qq})", font=ft)

            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
            draw = ImageDraw.Draw(img)
            draw.text((10, 1040), "Developed by Qianyi", font=ft)
            draw.text((300, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)

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