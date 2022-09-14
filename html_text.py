from typing import List
from ayaka import *
from .utils.spider import Spider

app = AyakaApp("html文本抓取", only_group=True)
app.help = "抓取html页面的文本内容 [#ht <url>]"

sp = Spider()


def smart_cut(ans: str, limit: int):
    cuts = []
    for i, s in enumerate(ans):
        if s == "。" or s == "\n":
            cuts.append(i+1)

    # 切割
    data: List[str] = []
    last = 0
    for i in range(len(cuts) - 1):
        if cuts[i+1] > last + limit:
            data.append(ans[last:cuts[i]])
            last = cuts[i]

    data.append(ans[last:])

    data = [d.strip("\n") for d in data]
    return data


@app.on_command("ht")
async def handle():
    try:
        sp.url = app.args[0]
        soup = sp.get_soup()
    except:
        await app.send("爬取网址失败")
        return

    ans = soup.find("body").get_text("\n", True)
    data = smart_cut(ans, 200)
    await app.bot.send_group_forward_msg(app.event.group_id, data)
