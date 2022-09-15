from .model import Incan, Sender, Option
from ayaka import AyakaApp

app = AyakaApp("incan", only_group=True)


def get_sender():
    name = app.event.sender.card if app.event.sender.card else app.event.sender.nickname

    return Sender(name, app.event.user_id)


@app.on_command(["incan", "印加"])
async def game_entrance():
    f, info = app.start("run")
    await app.send(info)

    # 初始化模型
    model = Incan(app)

    # 缓存
    app.cache.model = model

    # 获取sender
    sender = get_sender()

    # 操作
    await model.Execute(sender, Option.GAMESTART)


@app.on_command(["help", "-h", "--help"], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.HELP)


@app.on_command(['rule', 'document', 'doc'], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.RULE)


@app.on_command("join", "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.JOINGAME)


@app.on_command(['go', 'forward'], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.FORWARD)


@app.on_command(['back', 'retreat', 'escape'], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.RETREAT)


@app.on_command("status", "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.STATUS)


@app.on_command(['start', 'run'], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.START)


@app.on_command(['exit', 'quit'], "run")
async def handle():
    model: Incan = app.cache.model
    sender = get_sender()
    await model.Execute(sender, Option.EXIT)
