import re
import traceback
from .utils import *
from ayaka.lazy import *

app = AyakaApp("nonebot-plugin-atri", only_group=True, no_storage=True)
app.help = '''ATRI VITS 模型拟声
ATRI
- 说(日语)
'''


@app.on_command("voice")
async def handle():
    await app.send()

# atri_regex = "^(?:亚托莉|)(发送|说)(.+)$"
# yozo_regex = "^(宁宁|爱瑠|芳乃|茉子|丛雨|小春|七海)(发送|说)(.+)$"
gs_regex = "^(派蒙|凯亚|安柏|丽莎|琴|香菱|枫原万叶|迪卢克|温迪|可莉|早柚|托马|芭芭拉|优菈|云堇|钟离|魈|凝光|雷电将军|北斗|甘雨|七七|刻晴|神里绫华|雷泽|神里绫人|罗莎莉亚|阿贝多|八重神子|宵宫|荒泷一斗|九条裟罗|夜兰|珊瑚宫心海|五郎|达达利亚|莫娜|班尼特|申鹤|行秋|烟绯|久岐忍|辛焱|砂糖|胡桃|重云|菲谢尔|诺艾尔|迪奥娜|鹿野院平藏)(发送|说)(.+)$"


# atri_cmd = re.compile(atri_regex)
# yozo_cmd = re.compile(yozo_regex)
gs_cmd = re.compile(gs_regex)


# @app.on_text()
# async def handle():
#     msg = app.args[0]

#     r = atri_cmd.match(msg)
#     if not r:
#         return

#     cmd, msg = matched[0], matched[1]
#     if cmd == '发送':
#         try:
#             await app.bot.send_group_msg(group_id=app.event.group_id, message=atri_func(msg=msg))
#             await app.send('发送成功')
#         except:
#             await app.send('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')
#     else:
#         try:
#             await app.send(atri_func(msg=msg))
#         except:
#             await app.send('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')


# @yozo_cmd.handle()
# async def _(bot: Bot, event: MessageEvent, matched: Tuple[Any, ...] = RegexGroup()):
#     name, cmd, msg = matched[0], matched[1], matched[2]
#     if cmd == '发送':
#         user_id = event.get_user_id()
#         if user_id not in BotSelfConfig.superusers:
#             await yozo_cmd.finish('权限不足')
#         try:
#             if (gp):
#                 await app.bot.send_group_msg(group_id=app.event.group_id, message=yozo_func(msg=msg, name=name))
#             else:
#                 await app.bot.send_private_msg(user_id=send_id, message=yozo_func(msg=msg, name=name))
#             await yozo_cmd.finish('发送成功')
#         except:
#             await yozo_cmd.finish('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')
#     else:
#         try:
#             if (gp):
#                 await yozo_cmd.finish(message=yozo_func(msg=msg, name=name))
#             else:
#                 await yozo_cmd.finish(message=yozo_func(msg=msg, name=name))
#         except:
#             await yozo_cmd.finish('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')


@app.on_text()
async def handle():
    msg = app.args[0]
    r = gs_cmd.match(msg)
    if not r:
        return

    name, cmd, msg = r.group(1), r.group(2), r.group(3)
    if cmd == '发送':
        try:
            await app.bot.send_group_msg(group_id=app.event.group_id, message=gs_func(msg=msg, name=name))
            await app.send('发送成功')
        except:
            await app.send('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')
    else:
        try:
            await app.send(gs_func(msg=msg, name=name))
        except:
            await app.send('API调用失败：' + traceback.format_exc() + '。请检查输入字符是否匹配语言。')
