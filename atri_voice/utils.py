import os
from string import Template
import requests
# from .utils.VITS import Trans, Trans2
from ayaka.lazy import *


def atoi(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num


extra = {
    "unique_name": "Gal-Voice",
    "example": "说お兄ちゃん大好き",
    "author": "KOG <1458038842@qq.com>",
    "version": "0.0.1",
}


# # api for other plugins
# def atri_func(msg):
#     Trans(msg, 'voice.wav')
#     voice = f'file:///'+os.getcwd()+'/voice.wav'
#     return MessageSegment.record(voice)


yozo_dict = {"宁宁": 0, "爱瑠": 1, "芳乃": 2, "茉子": 3, "丛雨": 4, "小春": 5, "七海": 6, }


# def yozo_func(msg, name):
#     Trans2(msg, yozo_dict[name], 'voice.wav')
#     voice = f'file:///'+os.getcwd()+'/voice.wav'
#     return MessageSegment.record(voice)


cnapi = Template(
    "http://233366.proxy.nscc-gz.cn:8888?speaker=${id}&text=${text}")


def gs_func(msg, name='派蒙'):
    voice = requests.get(cnapi.substitute(text=msg, id=name)).content
    return MessageSegment.record(voice)
