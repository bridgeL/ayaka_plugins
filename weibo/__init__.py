# 视奸6198086160的微博
# 处于安全考虑，不开放用户编辑权限
import asyncio
from pathlib import Path
from ayaka import *
from ..utils.spider import Spider
from .model import Card


app = AyakaApp("weibo")
app.help = "追踪张怡然最新动态"


accessor = AyakaStorage(str(Path(__file__).parent), "data.json",
                        default="{}").accessor("ids")
sp = Spider()


def get_publisher_info(weibo_id):
    """获取博主信息"""
    sp.url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={weibo_id}"
    data = sp.get_json()

    name = data["data"]["userInfo"]["screen_name"]
    tabs = data["data"]["tabsInfo"]["tabs"]
    for tab in tabs:
        if tab["tab_type"] == "weibo":
            containerid = tab["containerid"]
            break
    else:
        logger.error("获取 containerID 失败")
        raise

    logger.success(f"成功获取 博主名 {name}")
    logger.success(f"成功获取 containerID {containerid}")
    return f"{name} {weibo_id}", containerid


async def loop(bot: Bot):
    if bot.self_id != "2317709898":
        return

    weibo_id = 6198086160
    name, containerid = get_publisher_info(weibo_id)
    while True:
        try:
            cards = get_cards(weibo_id, containerid)
            for card in cards:
                text = f"{card.date}\n\n{card.text}\n\nhttps://m.weibo.cn/status/{card.id}"
                await bot.send_group_msg(group_id=666214666, message=text)
        except:
            logger.exception("爬取weibo出错")

        await asyncio.sleep(60)


def get_cards(weibo_id, containerid):
    # 准备爬虫
    sp.url = "https://m.weibo.cn/api/container/getIndex"
    sp.params = {
        "type": "uid",
        "value": weibo_id,
        "containerid": containerid,
        "page": 1
    }

    json_data = sp.get_json()

    data_list = json_data["data"]["cards"]
    cards = [Card(data) for data in data_list]
    ids: list = accessor.get([])
    cards = [card for card in cards if card.id not in ids]
    ids.extend(card.id for card in cards)
    if len(ids) > 20:
        ids = ids[10:]
    accessor.set(ids)
    return cards


@on_connect
async def _(bot: Bot):
    asyncio.create_task(loop(bot))
