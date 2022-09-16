from typing import List
from ayaka import *
from ..utils.file import LocalPath
emojiBin = LocalPath(__file__).load_json("emoji")

app = AyakaApp('emoji查询', only_group=True)
app.help = "[#e <参数>] 简单查询emoji\n[#emoji <参数>] 详细查询emoji"


async def search(app: AyakaApp):
    if not app.args:
        await app.send('没有相关结果')
        return []

    arg = app.args[0]

    def relate(tags: List[str]):
        for tag in tags:
            ss = tag.split("_")
            for s in ss:
                if s.startswith(arg):
                    return True

    es = [e for e in emojiBin if relate(emojiBin[e])]

    if not es:
        await app.send('没有相关结果')
    return es


@app.on_command('e')
async def emoji():
    es = await search(app)
    await app.bot.send_group_forward_msg(app.event.group_id, es)


@app.on_command('emoji')
async def emoji():
    es = await search(app)
    items = [f"{e} 标签\n" + "\n".join(emojiBin[e]) for e in es]
    await app.bot.send_group_forward_msg(app.event.group_id, items)
