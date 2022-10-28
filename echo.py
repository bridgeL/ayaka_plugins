'''
    具有状态机的复读模块
'''
from ayaka import AyakaApp

app = AyakaApp("echo")
app.help = {
    "init": "复读只因",
    "reverse": "说反话模式"
}
# init、reverse表示不同的状态
# 当app在某状态下时，app.help = 该状态对应的帮助
# app.intro = init对应的帮助


# 打开app
@app.on_command("echo")
async def app_entrance():
    '''开始复读 或 打开复读机'''
    # 输入参数则复读参数（无状态响应
    # > #echo hihi
    # < hihi
    if app.arg:
        await app.send(app.arg)
        return

    # 没有输入参数则运行该应用
    # 运行后，应用初始状态默认为init
    await app.start()

# on_state_text、on_state_command注册的回调都是在app运行后才有机会响应

# 正常复读
@app.on_state_text()
async def repeat():
    await app.send(app.message)


# 任意状态均可直接退出
@app.on_state_command(["exit", "退出"], "*")
async def app_exit():
    '''退出复读机'''
    await app.close()


# 通过命令，跳转到reverse状态
@app.on_state_command(["rev", "reverse", "话反说", "反", "说反话"])
async def start_rev():
    '''开始说反话'''
    app.set_state("reverse")
    await app.send("开始说反话")


# 反向复读
@app.on_state_text("reverse")
async def reverse_echo():
    msg = str(app.message)
    msg = "".join(reversed(msg))
    await app.send(msg)


# 通过命令，跳转回初始状态
@app.on_state_command("back", "reverse")
async def back():
    '''停止说反话'''
    app.set_state()
    await app.send("话反说止停")
    