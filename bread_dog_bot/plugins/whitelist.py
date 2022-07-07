from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.permission import SUPERUSER
import models.server
import utils.server
import utils.admin
import utils.whitelist

add_whitelist = on_command("添加白名单")


@add_whitelist.handle()
async def add_whitelist_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        player_name = text[1]
        result, server_info_list = utils.server.GetInfo.all()
        msg = []
        if result:
            for i in server_info_list:
                conn = models.server.Connect(i[2], i[3], i[4])
                result, reason = conn.add_whitelist(event.get_user_id(), player_name)
                if result:
                    msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                               f"添加成功！")
                else:
                    msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                               f"添加失败！\n"
                               f"{reason}")
            await add_whitelist.finish(Message("\n".join(msg)))
        else:
            await add_whitelist.finish(Message("添加失败！\n无法连接至数据库"))
    else:
        await add_whitelist.finish("添加失败！\n用法错误！\n请输入【帮助 添加白名单】获取该功能更多信息")


delete_whitelist = on_command("删除白名单")


@delete_whitelist.handle()
async def delete_whitelist_handle(bot: Bot, event: Event):
    admin_list = utils.admin.get()
    if event.get_user_id() in admin_list:
        text = event.get_plaintext().split(" ")
        if len(text) == 2:
            qq = text[1]
            result, server_info_list = utils.server.GetInfo.all()
            msg = []
            if result:
                for i in server_info_list:
                    conn = models.server.Connect(i[2], i[3], i[4])
                    result, reason = conn.delete_whitelist(qq)
                    if result:
                        msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                   f"删除成功！")
                    else:
                        msg.append(f"๑{i[0]}๑{MessageSegment.face(190)}{i[1]}\n"
                                   f"删除失败！\n"
                                   f"{reason}")
            else:
                await delete_whitelist.finish(Message("删除失败！\n无法连接至数据库"))

            await delete_whitelist.finish(Message("\n".join(msg)))
        else:
            await delete_whitelist.finish("删除失败！\n用法错误！\n请输入【帮助 删除白名单】获取该功能更多信息")

    else:
        await delete_whitelist.finish("删除失败！\n权限不足！\n请输入【帮助 删除白名单】获取该功能更多信息")

reset = on_command("重置白名单", permission=SUPERUSER)


@reset.handle()
async def reset_handle(bot: Bot, event: Event):
    result, reason = utils.whitelist.reset()
    if result:
        await reset.finish("重置成功！\n已重置数据库中的白名单")
    else:
        await reset.finish("重置失败！\n" + reason)
