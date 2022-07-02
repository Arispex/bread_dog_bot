from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
import models.server
import models.server
import utils.admin
import utils.server

online_players = on_command("在线")


@online_players.handle()
async def online_players_handle(bot: Bot, event: Event):
    result, server_info_list = utils.server.GetInfo.all()
    msg = []
    if result:
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
