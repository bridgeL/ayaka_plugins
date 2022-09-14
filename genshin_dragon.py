import json
from ayaka.lazy import *
from random import randint
import re
from pypinyin import lazy_pinyin


def load_json(filename: str):
    path = create_file("data", "plugins", "genshin_dragon",
                       filename, default="{}")
    data: dict = json.load(path.open("r", encoding="utf8"))
    return data


# 语料库
words = load_json('bin.json')
search_bin = load_json('search.json')

not_zh = re.compile(r'[^\u4e00-\u9fa5]*')


app = AyakaApp("原神接龙", only_group=True, no_storage=True)
app.help = "原神接龙，关键词中了就行"


@app.on_text()
async def handle():
    msg = str(app.message)

    # 删除所有非汉字
    msg = not_zh.sub('', msg)

    if not msg:
        return

    if msg not in words:
        return

    py = lazy_pinyin(msg[-1])[0]
    if py not in search_bin:
        return

    ans_list = search_bin[py]
    if ans_list:
        ans = ans_list[randint(0, len(ans_list)-1)]
        await app.send(ans)
