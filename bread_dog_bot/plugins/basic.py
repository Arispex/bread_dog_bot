from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.permission import SUPERUSER
import models.server
import models.server
import utils.admin
import utils.server

remote_command = on_command("执行")


@remote_command.handle()
async def remote_command_handle(bot: Bot, event: Event):
    admins = utils.admin.get()
    try:
        if event.get_user_id() in admins:
            text = event.get_plaintext().split(" ")
            id = text[1]
            command = " ".join(text[2:])
            result, server_info = utils.server.GetInfo.by_id(int(id))
            if result:
                conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                result, execute_result = conn.remote_command(command)
                if result:
                    if not execute_result["response"]:
                        execute_result["response"] = ["似乎没有返回结果"]
                    await remote_command.finish(f"执行成功！\n返回以下信息：\n" + "\n".join(execute_result["response"]))
                else:
                    await remote_command.finish(f"执行失败！\n{execute_result}")
            else:
                await remote_command.finish(f"执行失败！\n找不到序号为{id}的服务器")
        else:
            await remote_command.finish("执行失败！\n权限不足！\n请输入【帮助 执行】获取该功能更多信息")
    except ValueError:
        await remote_command.finish("执行失败！\n用法错误！\n请输入【帮助 执行】获取该功能更多信息")


say = on_command("发送")


@say.handle()
async def say_handle(bot: Bot, event: Event):
    text = event.get_plaintext().split(" ")
    if len(text) == 3:
        id = text[1]
        content = text[2]
        result, server_info = utils.server.GetInfo.by_id(int(id))
        if result:
            conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
            result, reason = conn.say(content)
            if result:
                await say.finish(f"发送成功！")
            else:
                await say.finish(f"发送失败！\n{reason}")
        else:
            await say.finish(f"发送失败！\n找不到序号为{id}的服务器")
    else:
        await say.finish("发送失败！\n用法错误！\n请输入【帮助 发送】获取该功能更多信息")
