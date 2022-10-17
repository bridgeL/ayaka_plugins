'''爬取nga主题帖内的回复'''
from asyncio import sleep
import requests
from pydantic import BaseModel
import re
import json
from time import time
from typing import List
from bs4 import BeautifulSoup
from ayaka import *

app = AyakaApp("nga_topic")
app.help = "nt <topic_id>"

cookie = app.plugin_storage("cookie", suffix=".txt").load().strip()

headers = {
    'user-agent': "NGA_WP_JW/(;WINDOWS)",
    'cookie': cookie
}


quote_patt1 = re.compile(r"\[quote\].*?\[/quote\]", re.S)
quote_patt2 = re.compile(r"\[b\]Reply to.*?\[/b\]")
collapse_patt = re.compile(r"\[collapse.*?\[/collapse\]")
img_patt = re.compile(r"\[img\].*?\[/img\]")


class PostDictList:
    def __init__(self, post_dict_list: List[dict]):
        self.post_dict_list = post_dict_list

    def add(self, key: str, value):
        '''补充'''
        for post_dict in self.post_dict_list:
            post_dict[key] = value
        return self

    def add_name(self, names: dict):
        for post_dict in self.post_dict_list:
            post_dict["user_name"] = names.get(post_dict["user_id"], "<爬取失败>")
        return self

    def add_comment(self, comments: dict):
        for post_dict in self.post_dict_list:
            comment = comments.get(post_dict["floor"], "---")
            if isinstance(comment, dict):
                post_dict["title"] = comment["title"]
                post_dict["content"] = comment["content"]
            else:
                post_dict["title"] = ""
                post_dict["content"] = comment
        return self

    def convert(self):
        '''转化为post类型的数据'''
        return [NgaPost(**post_dict) for post_dict in self.post_dict_list]


class TopicSoup:
    like_pattern = re.compile(
        r"commonui.postArg.proc\(\s*"
        r"((?P<floor>\d+)|'_(?P<tip>\d*)'|'__(?P<hot>\d*)'),"
        r"((\$\(.*\)|null),)*"
        r"(?P<post_id>\d*),"
        r"\d*,null,"
        r"'(?P<user_id>-?\d*)',"
        r"(?P<create_time>\d*),"
        r"'\d*,(?P<like>\d*),\d*'"
    )

    user_info_pattern = re.compile(
        r"commonui.userInfo.setAll\(\s*"
        r"(.*)"
        r"\).*__SELECTED_FORUM"
    )

    no_num_pattern = re.compile(r"\D")

    def __init__(self, data: BeautifulSoup):
        self.data = data

    def get_user_name(self):
        scripts: List[BeautifulSoup] = self.data.find_all('script')

        scripts = [s for s in scripts if 'commonui.userInfo.setAll' in str(s)]
        if not scripts:
            logger.error('未找到用户名脚本')
            return {}

        script = scripts[0]
        s = script.get_text(strip=True).replace('\r\n', '')

        # 获取uname字典
        r = self.user_info_pattern.search(s)
        if not r:
            logger.error('爬取到异常格式的用户名脚本')
            logger.error(s)
            return {}

        # 网站的api返回数据不标准，有时候字符串缺失了第一个引号，例如
        # "name":你好",
        # 可以考虑使用正则修复
        data = {}
        try:
            data = json.loads(r.group(1), strict=False)
        except:
            logger.warning('用户名脚本转换json时发生未知错误')
            logger.warning(r.group(1))

            s = r.group(1)
            s = re.sub(
                r'"(?P<key>\w*?)":\s*(?P<value>\w*?)",', r'"\1":"\2",', s)

            logger.warning('试图修复')
            try:
                data = json.loads(s, strict=False)
            except:
                logger.error('自动修复失败')
                logger.error(s)
                return {}

        # 排除无关k-v
        data = {uid: data[uid]['username']
                for uid in data if not self.no_num_pattern.search(uid)}

        # 修改匿名
        data['-1'] = '匿名'

        return data

    def get_comment(self):
        items: List[BeautifulSoup] = self.data.find_all(
            'table', class_='forumbox postbox')
        items: List[BeautifulSoup] = [
            item.find('td', class_='c2') for item in items]

        def get_content(floor_num: str, item: BeautifulSoup):
            if floor_num == '0':
                h3: BeautifulSoup = item.find('h3')
                p: BeautifulSoup = item.find('p')
                title = h3.get_text()
                content = p.get_text('\n', True)
                return {
                    "title": title,
                    "content": content
                }
            else:
                span: BeautifulSoup = item.find(
                    'span', class_="postcontent ubbcode")
                content = span.get_text('\n', True)
                return content

        data = {}
        for item in items:
            floor_num = item['id'][len('postcontainer'):]
            data[floor_num] = get_content(floor_num, item)

        return data

    def get_posts(self):
        scripts: List[BeautifulSoup] = self.data.find_all('script')

        scripts = [s for s in scripts if 'commonui.postArg.proc' in str(s)]

        data = []
        for script in scripts:
            s = script.get_text(strip=True).replace('\r\n', '')
            r = self.like_pattern.search(s)
            if not r:
                logger.error('爬取到异常格式的点赞数脚本')
                logger.error(s)
                continue
            else:
                data.append(r.groupdict())

        # 排除热评和贴条
        data = [d for d in data if d['floor'] is not None]

        return PostDictList(data)

    def deal(self, topic_id: int):
        names = self.get_user_name()
        comments = self.get_comment()

        posts = self                             \
            .get_posts()                        \
            .add_name(names)                    \
            .add_comment(comments)              \
            .add("update_time", 0)              \
            .add("topic_id", topic_id)          \
            .add("record_time", int(time()))    \
            .convert()

        return posts


class NgaPost(BaseModel):
    record_time: int
    topic_id: int
    post_id: int
    floor: int
    user_id: int
    user_name: str
    like: int
    create_time: int
    update_time: int
    title: str
    content: str


def get_soup(url: str):
    logger.debug(f"正在爬取 {url}")
    res = requests.get(url=url, headers=headers)
    res.encoding = 'gbk'
    content = res.text
    soup = BeautifulSoup(content, "html.parser")
    return soup


def get_posts(topic_id: int, page: int):
    url = f"https://nga.178.com/read.php?tid={topic_id}&page={page}"
    soup = get_soup(url)
    posts = TopicSoup(soup).deal(topic_id)
    return posts


@app.on_command("nt")
async def _():
    if not app.args:
        return

    msg = Message(app.args).extract_plain_text()
    try:
        tid = int(msg)
    except:
        return

    await app.send("开始爬取")

    posts: List[NgaPost] = []
    for i in range(5):
        if i > 0:
            await sleep(2)
        _ps = get_posts(tid, i+1)
        await app.send(f"第{i+1}页爬取完成")
        if not _ps:
            break
        posts.extend(_ps)

    await app.send(f"正在分析中")

    if not posts:
        return

    p = posts.pop(0)

    def get_content(content: str):
        content = quote_patt1.sub("[引用内容]", content)
        content = quote_patt2.sub("[引用内容]", content)
        content = collapse_patt.sub("[折叠内容]", content)
        content = img_patt.sub("[图片]", content)
        return content
    content = get_content(p.content)

    items = [f"[主题名] {p.title}", f"[主楼内容] [like:{p.like}]\n{content}", "前五页热评"]

    posts.sort(key=lambda p: p.like, reverse=True)
    posts = posts[:10]
    for i, p in enumerate(posts):
        content = get_content(p.content)
        items.append(f"{i+1}. [like:{p.like}] {content}")
    await app.send_many(items)
