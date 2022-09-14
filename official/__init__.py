from random import randint
from ayaka import *
from ..utils.file import LocalPath

app = AyakaApp(name="公文体", only_group=True)
app.help = "公文体 [#公文体 <数字>]"

data:dict = LocalPath(__file__).load_json("official")

data_bin = []
for v in data.values():
    data_bin.extend(v)


def get_values(cnt: int):
    im = len(data_bin)
    cnt = max(3, min(im, cnt))

    i = randint(0, im-1)
    data = data_bin[i:i+cnt]
    if i+cnt > im:
        data += data_bin[:i+cnt-im]

    return data


@app.on_command("公文体")
async def handle():
    i = 3
    if app.args:
        try:
            i = int(app.args[0])
        except:
            pass

    values = get_values(i)
    if len(values) > 50:
        items = []
        for i in range(0, len(values), 10):
            items.append("\n".join(values[i:i+10]))
        await app.bot.send_group_forward_msg(app.event.group_id, items)
    else:
        ans = "\n".join(values)
        await app.send(ans)
