'''
分割网址
'''
import json
from urllib.parse import unquote
from .utils.spider.utils import div_url
from ayaka import *

app = AyakaApp("分割网址")
app.help = "[#div <url>] 分割网址和参数"


@app.on_command("div")
async def div_url_handle():
    if not app.args:
        await app.send(app.help)
        return

    api, params = div_url(app.args[0])
    await app.send(api)

    if params:
        await app.send(json.dumps(params, ensure_ascii=False))

    website, page = api.rsplit("/", maxsplit=1)
    await app.send(unquote(page))
    