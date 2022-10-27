'''
    hello world

    ayaka可以帮助实现命令隔离
'''
from ayaka import AyakaApp

# 创建一个应用，起名为hello
app = AyakaApp("hello")

# 为该应用编写帮助
app.help = "第一个示例插件"


# 设置打开应用的指令
@app.on_command("hello")
async def app_entrance():
    '''打开hello world应用'''
    # 打开应用
    await app.start()
    # 应用打开后，进入 world 状态
    app.set_state("world")


# 设置关闭应用的指令
@app.on_state_command(["exit", "退出"], "*")
async def app_exit():
    '''返回到world 或 退出hello world应用'''
    # 只有world状态时可以关闭应用
    if app.state == "world":
        # 关闭应用
        await app.close()

    # 若在其他状态下，则先返回到world状态
    else:
        app.set_state("world")
        await app.send("跳转到 world")


@app.on_state_command(["hi", "hello"], ["world", "moon", "sun"])
async def hello():
    '''打个招呼'''
    # 发送hello world/moon/sun
    await app.send(f"hello, {app.state}!")


@app.on_state_command("hit", "world")
async def hit():
    '''给世界来个大比兜'''
    await app.send("earthquake")


@app.on_state_command("hit", "moon")
async def hit():
    '''给月亮来个大比兜'''
    await app.send("moon fall")


@app.on_state_command("hit", "sun")
async def hit():
    '''给太阳来个大比兜'''
    await app.send("big bang!")


@app.on_state_command("jump", "*")
async def jump_to_somewhere():
    '''跳转到指定的星球'''
    # 应用自动解析jump指令所在的消息，提取出其中的参数
    if not app.arg:
        await app.send("没有参数！")

    else:
        next_state = str(app.arg)

        # 修改状态
        app.set_state(next_state)
        await app.send(f"跳转到 {next_state}")
