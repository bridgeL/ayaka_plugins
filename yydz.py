from random import randint
from ayaka import *

app = AyakaApp("yydz", no_storage=True)
app.help = "选择困难了吗？让丁真来帮你吧\n[#yydz <a> <b> <c>]"


@app.on_command(["yydz", "一眼丁真"])
async def handle():
    if not app.args:
        await app.send("一眼丁真，鉴定为 啥也没输入")
    elif len(app.args) == 1:
        await app.send("一眼丁真，鉴定为 没得选")
    else:
        i = randint(0, len(app.args)*3)
        if i == 0:
            ans = ["我全都要", "为定鉴，真丁眼一", "".join(app.args)][randint(0, 2)]
        else:
            ans = app.args[i % len(app.args)]
        await app.send(f"一眼丁真，鉴定为 {ans}")
