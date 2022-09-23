'''
自动解析b站视频
'''
from html import unescape
import json
import re
from typing import List, Tuple
from bs4 import BeautifulSoup
from ayaka import *
from .utils.spider import Spider

app = AyakaApp("bili")
app.help = "自动解析b站视频"

sp = Spider()

url_matcher = re.compile(
    r"https://(b23\.tv|www\.bilibili\.com/video)(.*?\?|.*)")
info_matcher = re.compile(r"(?P<desc>.*?)"
                          r"(?=视频播放量)(?P<digital>.*?)"
                          r"(?=视频作者)(?P<author>.*?)"
                          r"(?=相关视频)(?P<relate>.*)")

pic_matcher = re.compile(r"(jpg|png)$")


@app.on_text(super=True)
async def supervise():
    for m in app.message:
        if m.type == "json":
            data = str(json.loads(m.data['data']))
            break
    else:
        data = unescape(str(app.message))

    r = url_matcher.search(data)

    if r:
        url = r.group().rstrip("?/")
        await deal(url)


async def deal(url: str):
    sp.url = url
    soup = sp.get_soup()
    head: BeautifulSoup = soup.head
    metas: List[BeautifulSoup] = head.find_all("meta")

    params = {}
    params["url"] = url

    data: List[Tuple[str, str]] = []
    for meta in metas:
        try:
            itemprop = meta["itemprop"]
            content = meta["content"]
            data.append((itemprop, content))
        except:
            continue

    for itemprop, content in data:
        if pic_matcher.search(content):
            params["image"] = MessageSegment.image(content)

        elif itemprop == "description":
            r = info_matcher.search(content)
            if r:
                detail = r.groupdict()
                for k, v in detail.items():
                    params[k] = v
            else:
                params[itemprop] = content
        else:
            params[itemprop] = content

    await app.send(Message([
        params["image"],
        "作者 - ",
        params["author"],
        "\n标题 - ",
        params["name"].replace("_哔哩哔哩_bilibili", "")
    ]))
    await app.send(url.rsplit("/", maxsplit=1)[-1])

    # if app.device.group:
    #     items = [Message([f"[{k}]\n", v]) for k, v in params.items()]
    #     await app.bot.send_group_forward_msg(app.event.group_id, items)
