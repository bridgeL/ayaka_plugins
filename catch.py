from ayaka import *
from .bag import get_uid_name

app = AyakaApp("catch", only_group=True, no_storage=True)
app.help = "强调群里某人的发言 [#catch @xx]"


@app.on_command("catch")
async def handle():
    uid = app.cache.uid

    if not app.args:
        if uid:
            await app.send(f"目前正在追踪 ({uid})")
        else:
            await app.send("目前没有任何追踪开启")
        await app.send(app.help)
        return

    uid, name = await get_uid_name(app.bot, app.event, app.args[0])
    app.cache.uid = uid

    if uid:
        await app.send(f"已开启对 {name}({uid})的追踪")
    else:
        await app.send("已关闭追踪")


@app.on_text(super=True)
async def handle():
    uid = app.cache.uid
    if uid and uid == app.event.user_id:
        await app.send(app.message)
