from .model import Incan, Player
from .app import app
from .utils import get_sender

greeting = '''欢迎使用印加宝藏2.0
输入[join]加入游戏
输入[start/run]开始游戏
输入[help]可以查看指令列表
输入[rule/doc查看游戏规则
如果在游戏过程中有什么问题或建议，请@灯夜(2692327749)'''

treasures = {
    'Turquoise': {
        'number': 0,
        'value': 1
    },
    'Obsidian': {
        'number': 0,
        'value': 5
    },
    'Gold': {
        'number': 0,
        'value': 10
    },
    'Artifact': {
        'number': 0,
        'value': 5
    }
}


def InitPlayer(self: Incan, player: Player):
    from copy import deepcopy
    self.members[player.uid] = {
        'status': 0,
        'name': player.name,
        'treasures': treasures,
        'income': deepcopy(treasures)
    }


@app.on_command(["incan", "印加"])
async def game_entrance():
    f, info = app.start("inqueue")
    await app.send(info)

    # 初始化模型
    model = Incan()

    # 缓存
    app.cache.model = model

    # 获取sender
    sender = get_sender(app)

    # 操作
    InitPlayer(model, sender)
    await app.send(greeting)
