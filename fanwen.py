from ayaka import *

app = AyakaApp("反过来")
app.help = "[#反 文字] 将文字“反”过来输出！~没看懂的话复制一下就知道了"


@app.on_command(["反", "fan"])
async def handle():
    if app.args:
        arg = app.args[0]
        arg = "".join(a for a in reversed(arg))
        arg = "\u202e" + arg
        await app.send(arg)
