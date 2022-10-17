# 视奸6198086160的微博
from dateutil.parser import parse
import requests
import datetime
from typing import List
from ayaka import *
from pydantic import BaseModel

app = AyakaApp("weibo_yy")
app.help = "24h视奸yy微博"

mid_file = app.plugin_storage("mids", default=[])
uid_file = app.plugin_storage("uids", default=[])


code = '''
document.querySelector("[role='navigation']").style = 'display:none';
document.querySelector(".Bar_main_R1N5v").style = 'display:none';
'''


class _Group(BaseModel):
    group_id: int
    bot_id: int


class _Weibo(BaseModel):
    uid: int
    cid: int
    name: str
    groups: List[_Group] = []

    def find(self, bot_id: int, group_id: int):
        for g in self.groups:
            if g.bot_id == bot_id and g.group_id == group_id:
                return g


class _WeiboList(BaseModel):
    value: List[_Weibo] = []

    def find(self, uid: int):
        for weibo in self.value:
            if weibo.uid == uid:
                return weibo


def load():
    return _WeiboList(value=uid_file.load())


def save(weibo_list: _WeiboList):
    uid_file.save(weibo_list.dict()["value"])


async def get_screenshot(link: str, name: str):
    path = app                                  \
        .plugin_storage("pics", suffix=None)    \
        .path.joinpath(f"{name}.png")           \
        .absolute()

    async with get_new_page(device_scale_factor=2) as page:
        await page.goto(link, wait_until="networkidle")
        await page.wait_for_selector("header .woo-avatar-img")
        await page.evaluate(code)
        await page.locator("article").screenshot(path=path)
    return path


def get_container_id(uid):
    url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}"
    data = requests.get(url).json()
    return int(data["data"]["tabsInfo"]["tabs"][1]["containerid"])


def get_links(uid, cid):
    url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid={cid}"
    data = requests.get(url).json()
    cards = data["data"]["cards"]

    date = datetime.datetime.now().date()
    links: List[str] = []
    mids: list = mid_file.load()

    for card in cards:
        mid = card["mblog"]["bid"]
        _date = parse(card["mblog"]["created_at"]).date()
        link = f"https://weibo.com/{uid}/{mid}"

        if _date == date and mid not in mids:
            mids.append(mid)
            links.append(link)

    if links:
        mid_file.save(mids)

    return links


@app.on_interval(60)
async def handle():
    weibo_list = load()
    for weibo in weibo_list.value:
        # 查看动态
        links = get_links(weibo.uid, weibo.cid)

        # 依次截图、下载、发送
        for link in links:
            name = link.split("/")[-1]
            logger.success(f"正在截图 {link}")
            # 截取两次，尝试解决图片加载不全的问题
            image_path = await get_screenshot(link, name)
            image_path = await get_screenshot(link, name)
            image = MessageSegment.image(image_path)

            for g in weibo.groups:
                await app.t_send(g.bot_id, g.group_id, link)
                await app.t_send(g.bot_id, g.group_id, image)
