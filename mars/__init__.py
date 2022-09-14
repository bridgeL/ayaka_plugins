from ayaka import *
from ..utils.file import LocalPath

mars_data = LocalPath(__file__).load_json("mars")
charPYStr: str = mars_data['charPYStr']
ftPYStr: str = mars_data['ftPYStr']


def judge(cc):
    mars_yes = 0
    mars_no = 0
    for c in cc:
        if c in charPYStr:
            mars_no += 1
        elif c in ftPYStr:
            mars_yes += 1
    return mars_yes > mars_no


def mars_encode(cc):
    str = ''
    for c in cc:
        i = charPYStr.find(c)
        if i >= 0:
            str += ftPYStr[i]
        else:
            str += c
    return str


def mars_decode(cc):
    str = ''
    for c in cc:
        i = ftPYStr.find(c)
        if i >= 0:
            str += charPYStr[i]
        else:
            str += c
    return str


app = AyakaApp('mars', no_storage=True)
app.help = "火星文转换器\n[#mars <文字>]自动分析转换方向"


@app.on_command(['mars', '火星文'])
async def mars():
    if app.args:
        arg = app.args[0]
        if judge(arg):
            ans = mars_decode(arg)
        else:
            ans = mars_encode(arg)
        await app.send(ans)
    else:
        await app.send(app.help)
