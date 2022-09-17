'''[待完成]写的很丑'''

from ayaka import *
from .talk import corpus


app = AyakaApp('teach')
app.help = {
    "介绍": "教机器人说话",
    'menu': "[#add] 添加\n[#change] 修改",
    'add_title': "[<文字>] 输入问题",
    'add_content': "[<文字>] 输入回答",
    "change_input_question": "[<文字>] 输入问题以检索",
    "change_choose_question": "[<数字>] 输入数字以选择要修改的条目",
    "change_operate": "[#q] 修改问题\n[#a] 修改回答\n[#del] 删除本条",
    "change_update_question": "[<文字>] 输入更新后的问题",
    "change_update_answer": "[<文字>] 输入更新后的回答"
}


# 指令部分
@app.on_command(['teach', '教学'])
async def start():
    f, info = app.start("menu")
    await app.send(info)
    if f:
        app.state = "menu"
        await app.send_help()

# 添加


@app.on_command(['add', '添加'], 'menu')
async def add_0():
    # 没有变量，正常进入下一个状态
    if len(app.args) == 0:
        app.state = "add_title"
        await app.send_help()
        return

    if len(app.args) == 1:
        app.cache.question = app.args[0]
        app.state = "add_content"
        await app.send_help()
        return

    if len(app.args) >= 2:
        question = app.args[0]
        answer = app.args[1]
        await add_q_and_a(question, answer)


# 输入问题
@app.on_text('add_title')
async def add_title():
    if not app.args:
        await app.send('输入为空')
        return

    app.cache.question = app.args[0]
    app.state = "add_content"
    await app.send_help()

# 输入回答


@app.on_text('add_content')
async def add_content():
    if not app.args:
        await app.send('输入为空')
        return

    question = app.cache.question
    answer = app.args[0]
    await add_q_and_a(question, answer)


# 退出添加
@app.on_command(['exit', '退出'], ['add_title', 'add_content'])
async def exit_add():
    await app.send(f"已取消添加")
    app.state = "menu"
    await app.send_help()

# 彻底退出


@app.on_command(['exit', '退出'], 'menu')
async def exit_menu():
    f, info = app.close()
    await app.send(info)


# 修改
@app.on_command(['change', '修改'], 'menu')
async def change_menu():
    if app.event.message_type != 'group':
        await app.send("该功能仅支持群聊")
        return

    # 没有变量，正常进入下一个状态
    if len(app.args) == 0:
        app.state = "change_input_question"
        await app.send_help()
        return

    if len(app.args) >= 1:
        await find_questions(app.args[0])


# 输入查询词
@app.on_text('change_input_question')
async def handle():
    msg = app.args[0]
    if not msg:
        await app.send('输入为空')
        return

    await find_questions(msg)


# 选择修改条目
@app.on_text('change_choose_question')
async def handle():
    msg = app.args[0]
    if not msg:
        await app.send('输入为空')
        return

    try:
        i = int(msg)
    except:
        await app.send('请输入纯数字')
        return

    id_list = app.cache.id_list

    if i >= len(id_list) or i < 0:
        await app.send('超出范围')
        return

    id = id_list[i]

    data = corpus.get_item(id)
    ans = corpus_data_2_str(data)
    await app.send(ans)

    app.cache.id = id
    app.state = "change_operate"
    await app.send_help()

# 选择修改问题


@app.on_command('q', 'change_operate')
async def handle():
    app.state = "change_update_question"
    await app.send_help()

# 选择修改回答


@app.on_command('a', 'change_operate')
async def handle():
    app.state = "change_update_answer"
    await app.send_help()

# 选择删除条目


@app.on_command('del', 'change_operate')
async def handle():
    id = app.cache.id
    corpus.del_item(id)

    await app.send("成功删除")
    app.state = "menu"
    await app.send_help()


# 输入新问题
@app.on_text('change_update_question')
async def handle():
    await change_q_a(True)


# 输入新回答
@app.on_text('change_update_answer')
async def handle():
    await change_q_a(False)


# 退出修改
@app.on_command(['exit', '退出'], ['change_input_question', 'change_choose_question', 'change_operate', 'change_update_question', 'change_update_answer'])
async def exit_change():
    await app.send(f"已取消修改")
    app.state = "menu"
    await app.send_help()


async def add_q_and_a(q: str, a: str):
    corpus.teach(q, a)
    await app.send(f"问：{q}\n答：{a}")
    app.state = "menu"
    await app.send_help()


async def change_q_a(q_flag: bool):
    msg = app.args[0]

    if not msg:
        await app.send('输入为空')
        return

    id = app.cache.id
    if q_flag:
        corpus.set_item(id, q=msg)
    else:
        corpus.set_item(id, a=msg)

    await app.send('修改成功')
    app.state = "menu"
    await app.send_help()


def corpus_data_2_str(data: dict):
    ans = f"问题：{data['key']}\n回答："
    v = data['value']
    if isinstance(v, list):
        ans += '（具有多个）\n'
        ans += '\n'.join(v)
    else:
        ans += v
    return ans


async def find_questions(key: str):
    if not key:
        await app.send("没有输入参数")
        return

    data = corpus.get_items(key)

    if not data:
        await app.send("没有找到相关问题")
        return

    ans_list = []
    for i in range(len(data)):
        ans = f'[{i}]\n' + corpus_data_2_str(data[i])
        ans_list.append(ans)

    await app.bot.send_group_forward_msg(app.event.group_id, ans_list)

    id_list = [d["id"] for d in data]
    app.cache.id_list = id_list
    app.state = "change_choose_question"
    await app.send_help()
