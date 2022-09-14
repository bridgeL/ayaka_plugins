import sys
from ayaka import *
from pydantic import BaseModel
from .utils.spider import Spider

app = AyakaApp("setu", only_group=True, no_storage=True)
app.help = '来张涩图\n[#setu] 可以色色'

create_path("data", "setu")


class SetuData(BaseModel):
    pid: int = 0
    title: str = ""
    author: str = ""
    url: str = ""
    name: str = ""

    def __init__(self, **data) -> None:
        url: str = data['urls']['original']
        name = url[url.rfind('/')+1:]
        super().__init__(**data, url=url, name=name)

    def get_info(self):
        ans = "\n".join([
            f"[PID] {self.pid}",
            f"[标题] {self.title}",
            f"[作者] {self.author}",
            f"[地址] {self.url}"
        ])
        return ans


proxy = 'http://127.0.0.1:7890'
api = 'https://api.lolicon.app/setu/v2'


@app.on_command(['setu', '涩图', '色图', '瑟图'])
async def handle():
    local = sys.platform == 'win32'
    if not local:
        logger.debug(f"setu正在云端运行")

    try:
        # 获取url
        if local:
            data = Spider(api, proxy=proxy).get_json()
        else:
            data = Spider(api).get_json()

        data = data["data"][0]
    except:
        await app.send('setu 未获取到图片地址')
        return
    else:
        # 提取感兴趣的属性
        data = SetuData(**data)
        ans = data.get_info()
        await app.send(ans)

    try:
        if local:
            res = Spider(data.url, proxy=proxy).get_res()
        else:
            res = Spider(data.url).get_res()

        res = res.content
        open(f'data/setu/{data.name}', 'wb').write(res)
        await app.send(Message(MessageSegment.image(res)))
    except:
        await app.send('setu 太涩了，发不出来(')
        return
