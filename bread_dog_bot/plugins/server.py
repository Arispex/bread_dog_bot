from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.permission import SUPERUSER

import utils.admin
import utils.server

add_server = on_command("添加服务器", permission=SUPERUSER)


@add_server.handle()
async def add_server_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「添加服务器」")
    text = event.get_plaintext().split(" ")
    if len(text) == 5:
        name = text[1]
        ip = text[2]
        port = text[3]
        token = text[4]
        result, reason = utils.server.add(name, ip, port, token)
        if result:
            result, server_info = utils.server.GetInfo.by_name(name)
            await add_server.finish(f"【{name}】添加成功！\n序号为{server_info[0]}")
        else:
            await add_server.finish(f"【{name}】添加失败！\n{reason}")
    else:
        await add_server.finish("添加失败！\n用法错误！\n请输入【帮助 添加服务器】获取该功能更多信息")


delete_server = on_command("删除服务器", permission=SUPERUSER)


@delete_server.handle()
async def delete_server_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「删除服务器」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        name = text[1]
        result, reason = utils.server.delete(name)
        if result:
            await delete_server.finish(f"【{name}】删除成功！")
        else:
            await delete_server.finish(f"【{name}】删除失败！\n{reason}")
    else:
        await delete_server.finish("删除失败！\n用法错误！\n请输入【帮助 删除服务器】获取该功能更多信息")


reset = on_command("重置服务器列表", permission=SUPERUSER)


@reset.handle()
async def reset_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「重置服务器列表」")
    result, reason = utils.server.reset()
    if result:
        await reset.finish("重置成功！\n已重置服务器序号和删除列表所有服务器")
    else:
        await reset.finish("重置失败！\n" + reason)
