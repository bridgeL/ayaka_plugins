'''
分析上一个卡片
'''
import json
from .utils import BaseJson
from ayaka import *

app = AyakaApp("分析卡片", only_group=True)
app.help = "分析上一个转发的卡片 [#card]"


@app.on_text(super=True)
async def save_card():
    for m in app.message:
        if m.type == "json":
            break
    else:
        return

    data = json.loads(m.data['data'])
    data = BaseJson(**data)
    app.cache.last = data


@app.on_command("card")
async def handle():
    data: BaseJson = app.cache.last
    if not data:
        await app.send("没有捕获到上张卡片")
        return

    items = [
        f"[小程序名称]\n{data.app}",
        f"[卡片创建时间]\n{data.ctime_s}",
        f"[卡片描述]\n{data.desc}",
        f"[卡片提示]\n{data.prompt}",
        f"[卡片元内容描述]\n{data.meta.desc}",
        f"[卡片元内容来源]\n{data.meta.tag}",
        f"[卡片元内容标题]\n{data.meta.title}",
        "[卡片链接嗅探]"
    ]

    items.extend(data.meta.urls)

    await app.bot.send_group_forward_msg(app.event.group_id, items)
