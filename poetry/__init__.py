import re
from asyncio import sleep
from ayaka import *
from .poetry import Poetry

poetry = Poetry()

app = AyakaApp('poetry', only_group=True)
app.help = {
    "介绍": "诗歌",
    "menu": "[#add] 添加一首诗\n[#list] 诗歌列表\n[<诗名>] 从上次中断处念诗\n[<诗名> <数字>] 从指定行开始念诗",
    "add_title": "[<文字>] 输入诗歌名称",
    "add_content": "[<文字>] 输入诗歌内容，可解析多行文本 或 合并转发消息",
    "speak": "[#exit] 退出"
}


# 启动
@app.on_command(['poetry', '诗歌'])
async def poetry_entrance():
    f, info = app.start("menu")
    await app.send(info)
    if not app.args:
        await app.send(app.help["menu"])
    else:
        await speak(app)


# 关闭
@app.on_command(['exit', '退出'], 'menu')
async def poetry_exit():
    f, info = app.close()
    await app.send(info)


# 添加
@app.on_command(['add', '添加'], 'menu')
async def begin_add():
    # 没有变量，正常进入下一个状态
    if len(app.args) == 0:
        await to_state(app, "add_title")
        return

    if len(app.args) >= 1:
        await add_title(app)


@app.on_text('add_title')
async def add_title_handle():
    await add_title(app)


@app.on_text('add_content')
async def add_content():
    # 解析多行文本 或 合并转发消息
    if app.message[0].type == 'forward':
        id = app.message[0].data['id']
        res_json = await app.bot.call_api('get_forward_msg', message_id=id)
        msgs = res_json['messages']
        # 得到多行数组
        lines = [msg['content'].rstrip('\r\n') for msg in msgs]
    else:
        # 得到多行数组
        lines = str(app.message).replace('\r\n', '\n').split('\n')

    if not ''.join(lines):
        await app.send('不可输入为空')
        return

    # 提取纯净文字
    def get_pure_line(line: str):
        pure_line = re.sub(r'(?<=[^,.，。、；;])[,.，。、；;]$', '', line)
        return pure_line

    lines = [get_pure_line(line) for line in lines]

    # 排除空行
    lines = [line for line in lines if line]

    # 获取标题
    title = app.cache.title
    poetry.set_poetry(title, lines)

    await app.send(f"成功保存诗歌《{title}》")
    ans = '\n'.join(lines[:10])
    await app.send(ans[:200])

    await to_state(app, "menu")


# 退出添加
@app.on_command(['exit', '退出'], ['add_title', 'add_content'])
async def exit_add():
    await app.send("已取消添加")
    await to_state(app, "menu")


# 查看列表
@app.on_command(['list', '列表'], 'menu')
async def list_show():
    await app.send("已收录以下诗歌")
    names = poetry.get_info()
    await app.bot.send_group_forward_msg(group_id=app.event.group_id, messages=names)


# 点诗
@app.on_text('menu')
async def choose_poetry():
    await speak(app)


# 退出朗读
@app.on_command(['exit', '退出'], 'speak')
async def exit_speak():
    await app.send("已终止朗读")
    await to_state(app, "menu")


async def smart_sleep(line: str):
    t = 0.2 * len(line)
    t = 0.4 if t < 0.4 else t

    s = 5
    if t > s:
        t = (t - s) / 4 + s

    await sleep(t)


async def to_state(app: AyakaApp, state: str):
    app.state = state
    await app.send(app.help[state])


async def speak(app: AyakaApp):
    args = app.args
    title = args[0]

    # 查询诗歌是否存在
    item = poetry.get_poetry(title)
    if item is None:
        await app.send(f'没有收录诗歌《{title}》')
        return

    if len(args) >= 2:
        last_line_num = args[1]
        try:
            last_line_num = int(last_line_num)
        except:
            await app.send(f'请输入正确数字')
            return

    else:
        # 默认从上次位置继续
        if 'last_line_num' in item:
            last_line_num = item['last_line_num']
        else:
            last_line_num = 0
            item['last_line_num'] = 0

    time_s = item['time_s']
    lines = item['content']

    if last_line_num >= 0:
        await app.send(f"从第{last_line_num}行开始")
    else:
        await app.send(f"从倒数第{-last_line_num}行开始")
        last_line_num += len(lines)

    if last_line_num >= len(lines) or last_line_num < 0:
        await app.send(f'超出范围')
        return

    if app.state != "menu":
        return

    # 修改状态为speak
    app.state = "speak"
    last_line = title

    # 开始朗读
    await app.send(f"《{title}》\n添加时间：{time_s}")

    # 循环朗读
    for i in range(last_line_num, len(lines)):
        line = lines[i]
        await smart_sleep(last_line)

        # 监测state
        if app.state != 'speak':
            poetry.set_last_line_num(title, i)
            return

        line = line.rstrip(',.，。、;；')
        await app.send(line)
        last_line = line

    poetry.set_last_line_num(title, 0)
    await to_state(app, "menu")


async def add_title(app: AyakaApp):
    if not app.args or not app.args[0]:
        await app.send('不可输入为空')
        return

    msg = app.args[0]
    app.cache.title = msg
    await app.send(f"诗歌名 {msg}")
    await to_state(app, "add_content")
