'''
快捷跳转到百科
'''
from urllib.parse import quote
from ayaka.lazy import *

app = AyakaApp("百科链接拼凑", no_storage=True)
app.help = "发送[#baike <name>] 给出对应的百科网址"


@app.on_command(["baike", "bk", "百科"])
async def handle():
    if app.args:
        await app.send(f"https://baike.baidu.com/item/{quote(app.args[0])}")
