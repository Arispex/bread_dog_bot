import utils.admin
from nonebot.permission import SUPERUSER
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
import io
from nonebot_plugin_htmlrender import (
    text_to_pic,
    md_to_pic,
    template_to_pic,
    get_new_page,
)
from PIL import Image

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
async def admin_list_handle(bot: Bot, event: Event):
    from pathlib import Path

    template_path = str(Path(__file__).parent / "templates")
    template_name = "adminList.html"
    # 设置模板
    # 模板中本地资源地址需要相对于 base_url 或使用绝对路径
    pic = await template_to_pic(
        template_path=template_path,
        template_name=template_name,
        templates={"admin_list": utils.admin.get()},
        pages={
            "viewport": {"width": 250, "height": len(utils.admin.get()) * 25},
            "base_url": f"file://{template_path}",
        },
        wait=2,
    )

    a = Image.open(io.BytesIO(pic))
    a.save("admin_list.png", format="PNG")

    await admin_list.finish(MessageSegment.image(pic))
