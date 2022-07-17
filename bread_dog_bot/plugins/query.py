import os

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
import models.server
import models.server
import utils.admin
import utils.server
import json
from PIL import Image, ImageChops, ImageDraw, ImageFont
import time

online_players = on_command("在线")


@online_players.handle()
async def online_players_handle(bot: Bot, event: Event):
    result, server_info_list = utils.server.GetInfo.all()
    msg = []
    if result:
        if not server_info_list:
            msg.append("群主很懒，没有添加任何服务器！")

        for i in server_info_list:
            conn = models.server.Connect(i[2], i[3], i[4])
            result, player_list = conn.online_players()
            if result:
                msg.append(
                    f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n在线玩家({conn.playercount}/{conn.maxplayers})：\n" + ", ".join(
                        player_list))
            else:
                msg.append(
                    f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n{conn.error}")
    else:
        msg.append(
            f"{server_info_list}")
    await online_players.finish(Message("\n".join(msg)))


server_list = on_command("服务器列表")


@server_list.handle()
async def server_list_handle(bot: Bot, event: Event):
    result, server_info_list = utils.server.GetInfo.all()
    msg = []
    if result:
        if not server_info_list:
            msg.append("群主很懒，没有添加任何服务器！")
        for i in server_info_list:
            conn = models.server.Connect(i[2], i[3], i[4])
            if conn.status_code:
                msg.append(
                    f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\nIP：{conn.ip}\n端口：{conn.server_port}")
            else:
                msg.append(
                    f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n{conn.error}")
    else:
        msg.append(
            f"{server_info_list}")

    await server_list.finish(Message("\n".join(msg)))


world_progress = on_command("进度")


@world_progress.handle()
async def world_progress_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        num = text[1]
        result, server_info = utils.server.GetInfo.by_id(int(num))
        if result:
            conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
            result, progress = conn.progress()
            if result:
                progress = json.loads(progress["response"])
                img = Image.open("img/progress_bg.png")
                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
                draw = ImageDraw.Draw(img)
                w, h = img.size
                text_w, text_h = ft.getsize(server_info[1])
                draw.text(((w - text_w) / 2, 0), server_info[1], font=ft)

                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
                draw = ImageDraw.Draw(img)
                text_w, text_h = ft.getsize("进度")
                draw.text(((w - text_w) / 2, 150), "进度", font=ft)

                ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                draw = ImageDraw.Draw(img)
                draw.text((10, 1040), "Developed by Qianyi", font=ft)
                draw.text((310, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)

                row = 0
                column = 0
                add = 0

                for i in progress.values():
                    if row == 2 and column == 0:
                        if i:
                            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                            draw = ImageDraw.Draw(img)
                            draw.text((270 + row * 230 + 20, 440 + column * 250), "已击败", font=ft, fill="red")

                            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                            draw = ImageDraw.Draw(img)
                            draw.text((270 + (row + 1) * 230 + 100, 440 + column * 250), "已击败", font=ft, fill="red")
                        else:
                            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                            draw = ImageDraw.Draw(img)
                            draw.text((270 + row * 230 + 20, 440 + column * 250), " 未击败", font=ft, fill="black")

                            ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                            draw = ImageDraw.Draw(img)
                            draw.text((270 + (row + 1) * 230 + 100, 440 + column * 250), " 未击败", font=ft, fill="black")
                        row += 2
                        continue
                    if row == 2:
                        add = 20
                    if row >= 3:
                        add = 100 + (row - 3) * 40
                        if row == 5:
                            add -= 40
                    if i:
                        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                        draw = ImageDraw.Draw(img)
                        draw.text((270 + row * 230 + add, 440 + column * 250), "已击败", font=ft, fill="red")
                    else:
                        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
                        draw = ImageDraw.Draw(img)
                        draw.text((270 + row * 230 + add, 440 + column * 250), " 未击败", font=ft, fill="black")
                    if row == 5:
                        row = 0
                        column += 1
                        add = 0
                    else:
                        row += 1

                img.save("img/progress.png")
                await world_progress.finish(MessageSegment.image("file://" + os.getcwd() + "/img/progress.png"))
            else:
                await world_progress.finish(f"查询失败！\n{progress}")
        else:
            await world_progress.finish(f"查询失败！\n找不到序号为{num}的服务器")
    else:
        await world_progress.finish("查询失败！\n用法错误！\n请输入【帮助 进度】获取该功能更多信息")
