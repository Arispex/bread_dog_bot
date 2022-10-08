import math
import os
import time

import requests
from PIL import Image, ImageDraw, ImageFont
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupMessageEvent, Message
from nonebot.permission import SUPERUSER

import utils.admin

add_admin = on_command("添加管理员", permission=SUPERUSER)


@add_admin.handle()
async def add_admin_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
        if qq.isdigit():
            result, reason = utils.admin.add(qq)
            if result:
                await add_admin.finish(f"添加成功！")
            else:
                await add_admin.finish("添加失败！\n他已经是管理员了")
        await add_admin.finish("添加失败！\n无效的参数\n请输入正确的QQ号")
    else:
        await add_admin.finish("添加失败！\n用法错误！\n请输入【帮助 添加管理】获取该功能更多信息")


delete_admin = on_command("删除管理员", permission=SUPERUSER)


@delete_admin.handle()
async def delete_admin_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        qq = text[1]
        if qq.isdigit():
            result, reason = utils.admin.delete(qq)
            if result:
                await delete_admin.finish(f"删除成功！")
            else:
                await delete_admin.finish("删除失败！\n他不是管理员")
        await delete_admin.finish("删除失败！\n无效的参数\n请输入正确的QQ号")
    else:
        await delete_admin.finish("删除失败！\n用法错误！\n请输入【帮助 删除管理】获取该功能更多信息")


admin_list = on_command("管理员列表")


@admin_list.handle()
async def admin_list_handle(bot: Bot, event: GroupMessageEvent):
    text = event.get_plaintext().split(" ")
    if len(text) == 1:
        page = 1
    elif len(text) == 2:
        if text[1].isdigit():
            page = int(text[1])
        else:
            await admin_list.finish("查询失败！\n无效的参数\n页数必须为数字")
    else:
        await admin_list.finish("查询失败！\n用法错误！\n请输入【帮助 管理员列表】获取该功能更多信息")

    admins = utils.admin.get()
    if admins[0] == "" or not admins:
        await admin_list.finish("群主很懒，还没有添加任何管理员")
    admin_info_list = []
    group_info = await bot.get_group_info(group_id=event.group_id)
    for i in admins:
        for x in await bot.get_group_member_list(group_id=event.group_id):
            if x["user_id"] == int(i):
                admin_info_list.append({"nickname": x["nickname"], "user_id": x["user_id"]})
                break
    total_page = math.ceil(len(admin_info_list) / 20)
    if page > total_page:
        await admin_list.finish(f"查询失败！\n无效的页数\n总页数为{total_page}")

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
    draw.text((650, 1040), f"管理员总数量：{len(admin_info_list)}", font=ft)
    draw.text((10, 10), f"当前页数：{page}/{total_page}", font=ft)
    w, h = ft.getsize(f"QQ群：{group_info['group_name']}({group_info['group_id']})")
    draw.text((img.width - w - 10, 10), f"QQ群：{group_info['group_name']}({group_info['group_id']})", font=ft)

    row = 0
    column = 0

    for i in admin_info_list[(page - 1) * 20:page * 20]:
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
        await admin_list.finish(MessageSegment.image("file:///" + os.getcwd() + "\\img\\admin_list.png"))
    else:  # linux
        await admin_list.finish(Message(MessageSegment.image("file://" + os.getcwd() + "/img/admin_list.png")))
