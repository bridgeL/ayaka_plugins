from ayaka.lazy import *
from .utils.time import get_time_i, time_i2s


app = AyakaApp('wty-time', only_group=True, no_storage=True)
app.help = "wty现在几点了\n[#wty]"


@app.on_command(['wty', "wt"])
async def test():
    time_i = get_time_i() + 3600*11
    time_s = time_i2s(time_i, "%H:%M:%S")
    await app.send(time_s)
