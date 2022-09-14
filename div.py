'''
分割网址
'''
import json
from urllib.parse import unquote
from ayaka import *

app = AyakaApp("分割网址")
app.help = "[#div <url>] 分割网址和参数"


def must_div(msg: str, sep: str, split: int, left=True):
    if left:
        items = msg.split(sep, split)
    else:
        items = msg.rsplit(sep, split)

    items += [""]*(split + 1 - len(items))
    return items


@app.on_command("div")
async def div_url():
    if not app.args:
        await app.send(app.help)
        return

    url = app.args[0]
    api, param_str = must_div(url, "?", 1)
    website, page = must_div(api, "/", 1, False)

    await app.send(api)
    await app.send(website)
    await app.send(unquote(page))

    if param_str:
        pairs = param_str.split("&")
        items = [must_div(pair, "=", 1) for pair in pairs]
        params = {unquote(k): unquote(v) for k, v in items}
        await app.send(json.dumps(params, ensure_ascii=False))
