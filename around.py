from ayaka import *

app = AyakaApp('环绕字', no_storage=True)
app.help = '''生成环绕字，例如：
#81 ab

生成
aaa
aba
aaa'''


@app.on_command(['around', '81', '环绕', '环绕字'])
async def around():
    if app.args:
        a = app.args[0]
        try:
            b = app.args[1]
        except:
            b = a[1:]
            a = a[:1]
        ans = f"{a*3}\n{a}{b}{a}\n{a*3}"
        await app.send(ans)
    else:
        await app.send('没有输入参数')
