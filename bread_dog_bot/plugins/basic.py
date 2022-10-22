from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent

import models.server
import models.server
import utils.admin
import utils.server

remote_command = on_command("执行")


@remote_command.handle()
async def remote_command_handle(bot: Bot, event: Event):
    logger.info(f"「{event.get_user_id()}」执行了 「执行」")
    admins = utils.admin.get()
    try:
        if event.get_user_id() in admins:
            text = event.get_plaintext().split(" ")
            id = text[1]
            command = " ".join(text[2:])

            if not id.isdigit():
                await remote_command.finish("执行失败！\n无效的参数\n服务器序号必须为数字")

            if not command.startswith("/"):
                await remote_command.finish("执行失败！\n无效的参数\n命令必须以/开头")

            result, server_info = utils.server.GetInfo.by_id(int(id))
            if result:
                conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
                result, execute_result = conn.remote_command(command)
                if result:
                    if not execute_result["response"]:
                        execute_result["response"] = ["似乎没有返回结果"]
                    await remote_command.finish(f"执行成功！\n返回以下信息：\n" + "\n".join(execute_result["response"]))
                    logger.info(f"「{event.get_user_id()}」在 {id} 号服务器执行了 {command}")
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
async def say_handle(bot: Bot, event: GroupMessageEvent):
    logger.info(f"「{event.get_user_id()}」执行了 「发送」")
    text = event.get_plaintext().split(" ")
    if len(text) == 3:
        id = text[1]
        content = text[2]

        if not id.isdigit():
            await say.finish("发送失败！\n无效的参数\n服务器序号必须为数字")

        result, server_info = utils.server.GetInfo.by_id(int(id))
        member_info = await bot.get_group_member_info(group_id=event.group_id, user_id=int(event.get_user_id()))
        content = f"{member_info['nickname']}({member_info['user_id']})：{content}"
        if result:
            conn = models.server.Connect(server_info[2], server_info[3], server_info[4])
            result, reason = conn.say(content)
            if result:
                await say.finish(f"发送成功！")
                logger.info(f"「{event.get_user_id()}」在 {id} 号服务器发送了一条消息：{content}")
            else:
                await say.finish(f"发送失败！\n{reason}")
        else:
            await say.finish(f"发送失败！\n找不到序号为{id}的服务器")
    else:
        await say.finish("发送失败！\n用法错误！\n请输入【帮助 发送】获取该功能更多信息")
