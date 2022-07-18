import os
import utils.admin
from nonebot.permission import SUPERUSER
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
from PIL import Image, ImageChops, ImageDraw, ImageFont
import time
import requests

add_admin = on_command("添加管理员", permission=SUPERUSER)


@add_admin.handle()
async def add_admin_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
        result, reason = utils.admin.add(qq)
        if result:
            await add_admin.finish(f"添加成功！")
        else:
            await add_admin.finish("添加失败！\n他已经是管理员了")
    else:
        await add_admin.finish("添加失败！\n用法错误！\n请输入【帮助 添加管理】获取该功能更多信息")


delete_admin = on_command("删除管理员", permission=SUPERUSER)


@delete_admin.handle()
async def delete_admin_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
        result, reason = utils.admin.delete(qq)
        if result:
            await delete_admin.finish(f"删除成功！")
        else:
            await delete_admin.finish("删除失败！\n他不是管理员")
    else:
        await delete_admin.finish("删除失败！\n用法错误！\n请输入【帮助 删除管理】获取该功能更多信息")


admin_list = on_command("管理员列表")


@admin_list.handle()
async def admin_list_handle(bot: Bot, event: GroupMessageEvent):
    admins = utils.admin.get()
    admin_info_list = []
    group_info = await bot.get_group_info(group_id=event.group_id)
    for i in admins:
        for x in await bot.get_group_member_list(group_id=event.group_id):
            if x["user_id"] == int(i):
                admin_info_list.append({"nickname": x["nickname"], "user_id": x["user_id"]})
                break

    img = Image.open("img/admin_list_bg.png")
    ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=100)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    text_w, text_h = ft.getsize(group_info["group_name"])
    draw.text(((w - text_w) / 2, 0), group_info["group_name"], font=ft)

    ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=60)
    draw = ImageDraw.Draw(img)
    text_w, text_h = ft.getsize("管理员列表")
    draw.text(((w - text_w) / 2, 150), "管理员列表", font=ft)

    ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=30)
    draw = ImageDraw.Draw(img)
    draw.text((10, 1040), "Developed by Qianyi", font=ft)
    draw.text((310, 1040), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), font=ft)

    row = 0
    column = 0

    for i in admin_info_list:
        response = requests.get("http://q1.qlogo.cn/g?b=qq&s=640&nk=" + str(i["user_id"]))
        with open("img/avatar.png", "wb") as f:
            f.write(response.content)
        avatar = Image.open("img/avatar.png")
        avatar = avatar.resize((100, 100))
        bg = Image.new(mode="RGBA", size=(300, 100))
        bg.paste(avatar, (0, 0))
        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=20)
        draw = ImageDraw.Draw(bg)
        draw.text((110, 20), f"昵称：{i['nickname']}", font=ft, fill="black")

        ft = ImageFont.truetype(font="font/Alibaba-PuHuiTi-Light.otf", size=20)
        draw = ImageDraw.Draw(bg)
        draw.text((110, 60), f"QQ：{i['user_id']}", font=ft, fill="black")

        r, g, b, a = bg.split()
        img.paste(bg, (10 + row * 400, 300 + column * 200), mask=a)
        if row == 4:
            row = 0
            column += 1
        else:
            row += 1

    img.save("img/admin_list.png")
    if os.name == "nt":  # windows
        await admin_list.finish(MessageSegment.image("file:///" + os.getcwd() + "\\img\\progress.png"))
    else:  # linux
        await admin_list.finish(Message(MessageSegment.image("file://" + os.getcwd() + "/img/admin_list.png")))
