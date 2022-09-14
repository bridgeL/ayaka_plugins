from .model import Incan
from ayaka import AyakaApp

app = AyakaApp("incan", only_group=True)


@app.on_command(["incan", "印加"])
async def game_entrance():
    f, info = app.start("run")
    await app.send(info)
    app.cache.model = Incan(app)

class Sender:
    def __init__(self, name, uid) -> None:
        self.name = name
        self.uid = uid

@app.on_text("run")
async def handle():
    model: Incan = app.cache.model
    if not model:
        f, info = app.close()
        await app.send(info)
        return

    name = app.event.sender.card if app.event.sender.card else app.event.sender.nickname

    await model.Execute(Sender(name, app.event.user_id), app.args)

    if model.completed:
        f, info = app.close()
        await app.send(info)
