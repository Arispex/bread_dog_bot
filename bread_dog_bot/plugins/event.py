from nonebot import on_command, export
from nonebot.typing import T_State
from nonebot import on_notice
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, GroupIncreaseNoticeEvent, Message, \
    GroupDecreaseNoticeEvent
import config
import utils.server
import utils.whitelist
import models.server
import utils.cloud_blacklist

export = export()
export.name = '进群欢迎'
export.usage = '欢迎新人'

welcom = on_notice()


# 群友入群
@welcom.handle()  # 监听 welcom
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    qq = event.get_user_id()  # 获取新成员的id
    msg = f'{MessageSegment.at(qq)}\n欢迎加入{config.Group.name}~\n请发送【服务器列表】来查看本群的所有服务器'
    await welcom.send(message=Message(msg))  # 发送消息
    result, reason = utils.cloud_blacklist.query(qq)
    if result:
        if config.Event.Welcome.kick_blacklist:
            msg = "机器人开启了自动踢出功能"
            try:
                await bot.set_group_kick(group_id=event.group_id, user_id=int(qq))
                msg += "\n已踢出该玩家"
            except:
                msg += "\n踢出失败，请设置机器人为群管理员"
        else:
            msg = "机器人未开启自动踢出功能"
        await welcom.finish(f"云黑检测成功！\n该玩家位于云黑名单中\n添加群：{reason[1]}\n原因：{reason[2]}\n{msg}")
    else:
        if reason == "未找到该QQ":
            await welcom.finish(f'云黑检测成功！\n该玩家未在云黑名单中，快来和大家一起玩吧！')
        else:
            await welcom.finish(f'云黑检测失败！\n{reason}')


# 群友退群
@welcom.handle()
async def h_r(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):  # event: GroupDecreaseNoticeEvent  群成员减少事件
    qq = event.get_user_id()  # 获取新成员的id
    result, player_info = utils.whitelist.GetInfo.by_qq(qq)
    if result:
        result, server_list = utils.server.GetInfo.all()
        for i in server_list:
            conn = models.server.Connect(i[2], i[3], i[4])
            conn.delete_whitelist(qq)
        msg = f'{qq} 离开了{config.Group.name}，已删除对应白名单，大家快出来送别它吧！\n'
    else:
        msg = f"{qq} 离开了{config.Group.name}，大家快出来送别它吧！"
    await welcom.finish(message=Message(msg))  # 发送消息
