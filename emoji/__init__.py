from typing import List
from ayaka import *
from ..utils.file import LocalPath
emojiBin = LocalPath(__file__).load_json("emoji")

app = AyakaApp('emoji查询', only_group=True)
app.help = "[#e <参数>] 简单查询emoji\n[#emoji <参数>] 详细查询emoji"


def search(app: AyakaApp):
    if not app.args:
        return []

    arg = app.args[0]

    def relate(tags: List[str]):
        for tag in tags:
            ss = tag.split("_")
            for s in ss:
                if s.startswith(arg):
                    return True

    es = [e for e in emojiBin if relate(emojiBin[e])]
    return es


@app.on_command('e')
async def emoji():
    es = search(app)
    if es:
        await app.bot.send_group_forward_msg(app.event.group_id, es)


@app.on_command('emoji')
async def emoji():
    es = search(app)
    if not es:
        await app.send('没有相关结果')
        return

    items = [f"{e} 标签\n" + "\n".join(emojiBin[e]) for e in es]
    await app.bot.send_group_forward_msg(app.event.group_id, items)
