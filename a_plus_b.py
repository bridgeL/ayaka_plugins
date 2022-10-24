'''
    a + b 各群聊间、各插件间，数据独立，互不影响
'''
from ayaka import AyakaApp

app = AyakaApp("a-plus-b")


@app.on_command("set_a")
async def set_a():
    app.cache.a = int(str(app.arg)) if app.arg else 0
    await app.send(app.cache.a)


@app.on_command("set_b")
async def set_b():
    app.cache.b = int(str(app.arg)) if app.arg else 0
    await app.send(app.cache.b)


@app.on_command("calc")
async def calc():
    a = app.cache.a or 0
    b = app.cache.b or 0
    await app.send(str(a+b))
