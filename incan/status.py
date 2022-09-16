from .model import Incan
from .app import app


@app.on_command("status", "inqueue")
async def handle():
    model: Incan = app.cache.model
    await app.send(model.GetTeamInfo())


@app.on_command("status", "gaming")
async def handle():
    model: Incan = app.cache.model
    await app.send(model.GetGameStatus())
