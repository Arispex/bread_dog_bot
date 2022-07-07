from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
import config

menu = on_command("菜单")


@menu.handle()
async def menu_handle(bot: Bot, event: Event):
    await menu.finish(Message(
        "———菜单———\n"
        f"{MessageSegment.face(147)}基础功能\n"
        f"{MessageSegment.face(147)}绑定功能\n"
        f"{MessageSegment.face(147)}玩家功能\n"
        f"{MessageSegment.face(147)}管理功能\n"
        f"{MessageSegment.face(147)}云黑功能\n"
        f"{MessageSegment.face(147)}抽奖功能\n"
        f"{MessageSegment.face(147)}商店功能\n"
        f"{MessageSegment.face(147)}排行榜功能\n"
        f"{MessageSegment.face(147)}关于"
    ))


# 基础功能
# 服务器的一些信息（在线，世界信息....)
# 执行命令等等...
basic = on_command("基础功能")


@basic.handle()
async def basic_handle(bot: Bot, event: Event):
    await basic.finish(Message(
        "———基础功能———\n"
        f"{MessageSegment.face(147)}服务器列表\n"
        f"{MessageSegment.face(147)}在线\n"
        f"{MessageSegment.face(147)}执行\n"
        f"{MessageSegment.face(147)}发送\n"
        f"{MessageSegment.face(147)}wiki\n"
    ))

# 绑定功能
# 白名单...
bind = on_command("绑定功能")


@bind.handle()
async def bind_handle(bot: Bot, event: Event):
    await bind.finish(Message(
        "———绑定功能———\n"
        f"{MessageSegment.face(147)}添加白名单\n"
        f"{MessageSegment.face(147)}删除白名单\n"
        f"{MessageSegment.face(147)}重置白名单列表\n"
    ))


player = on_command("玩家功能")


@player.handle()
async def player_handle(bot: Bot, event: Event):
    await player.finish(Message(
        "———玩家功能———\n"
        f"{MessageSegment.face(147)}签到\n"
        f"{MessageSegment.face(147)}玩家信息\n"
        f"{MessageSegment.face(147)}添加{config.Currency.name}\n"
        f"{MessageSegment.face(147)}扣除{config.Currency.name}\n"
        f"{MessageSegment.face(147)}设置{config.Currency.name}\n"
    ))


# 管理功能
# 操作管理员的一些功能 而不是只有管理员可以使用的功能
admin = on_command("管理功能")


@admin.handle()
async def admin_handle(bot: Bot, event: Event):
    await admin.finish(Message(
        "———管理功能———\n"
        f"{MessageSegment.face(147)}添加管理员\n"
        f"{MessageSegment.face(147)}删除管理员\n"
        f"{MessageSegment.face(147)}...\n"
    ))

# 云黑
# 云端黑名单系统
cloud = on_command("云黑功能")


@cloud.handle()
async def cloud_handle(bot: Bot, event: Event):
    await cloud.finish(Message(
        "———云黑功能———\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
    ))


lottery = on_command("抽奖功能")


@lottery.handle()
async def lottery_handle(bot: Bot, event: Event):
    await lottery.finish(Message(
        "———抽奖功能———\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
    ))


shop = on_command("商店功能")


@shop.handle()
async def shop_handle(bot: Bot, event: Event):
    await shop.finish(Message(
        "———商店功能———\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
    ))


rank = on_command("排行榜功能")


@rank.handle()
async def rank_handle(bot: Bot, event: Event):
    await rank.finish(Message(
        "———排行榜功能———\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
        f"{MessageSegment.face(147)}...\n"
    ))


about = on_command("关于")


@about.handle()
async def about_handle(bot: Bot, event: Event):
    await about.finish(Message(
        "———关于———\n"
        "bread dog bot\n"
        "一个高度可自定义化的 Terraria TShock Bot\n"
        "版本: 1.2.0\n"
        "作者: 千亦\n"
        "Github: https://github.com/Qianyiovo/breadDogBot"
    ))
