from ayaka import *

app = AyakaApp("bili_cm")
app.help = """快速查看b站热评
- bili_cm <bv>
"""

code ='''
let hide = function(selector){
    let node = document.querySelector(selector);
    if(node) node.style = "display:none";
}

hide("#biliMainHeader");
hide(".v-popover");
hide(".main-reply-box");
hide(".reply-end-mark");

document.querySelector(".reply-list").style.paddingBottom = 0;
'''

@app.on_command("bili_cm")
async def get_screenshot():
    if not app.args:
        return

    bv = str(app.args[0])

    link = f"https://www.bilibili.com/video/{bv}/"
    logger.success(f"正在截图 {link}")
    await app.send("正在生成评论区截图")

    path = app                                  \
        .plugin_storage("pics", suffix=None)    \
        .path.joinpath(f"{bv}.png")             \
        .absolute()

    async with get_new_page(device_scale_factor=2) as page:
        await page.goto(link, wait_until="networkidle")
        await page.wait_for_selector(".comment-container")
        await page.evaluate(code)
        await page.locator(".comment-container").screenshot(path=path)

    image = MessageSegment.image(path) 
    await app.send(image)
