from urllib import parse
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

# 感谢@ACaiCat的提供的wiki代码
wiki = on_startswith(("搜索", "wiki", "Wiki", "WIKI"))


@wiki.handle()
async def wiki_(bot: Bot, event: GroupMessageEvent):
    logger.info(f"「{event.get_user_id()}」执行了 「wiki」")
    text = event.get_plaintext().split(" ")
    if len(text) == 2:
        msg = event.get_plaintext().replace("搜索", "").replace("wiki", "").replace("Wiki", "").replace("WIKI", "").replace(
            " ", "")
        await wiki.finish(
            f"\n已从Wiki上帮你找到【{msg}】，点击对应链接查看：\n1⃣官方百科：\nhttps://terraria.wiki.gg/zh/wiki/Special:%E6%90%9C%E7%B4%A2?search={parse.quote(msg)}\n2⃣旧百科：\nhttps://terraria.fandom.com/zh/wiki/Special:%E6%90%9C%E7%B4%A2?search={parse.quote(msg)}\n"
            f"3⃣BWiki(非常旧)：\nhttps://searchwiki.biligame.com/tr/index.php?search={parse.quote(msg)}", at_sender=True)
    else:
        await wiki.finish("\n搜索失败！\n搜索内容不能为空！\n请输入【帮助 wiki】获取该功能更多信息", at_sender=True)
