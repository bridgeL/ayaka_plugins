from ayaka.lazy import *
from .corpus import Corpus

corpus = Corpus()

app = AyakaApp('talk', no_storage=True)
app.help = "命令式傻瓜聊天机器人"


@app.on_text()
async def talk():
    msg = str(app.message)
    ans = corpus.search(msg, True)
    if ans:
        await app.send(Message(ans))
        return True
    return False
