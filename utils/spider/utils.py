''' 工具包 '''
import json
from random import choice
from pathlib import Path
import unicodedata
from urllib.parse import unquote
from datetime import datetime
from colorama import Fore
import colorama
colorama.init(autoreset=True)


class Logger:
    color_dict = {
        "_DEBUG_": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.LIGHTRED_EX,
    }

    def __init__(self, path=None) -> None:
        self.path = Path(path) if path else None

    def base_print(self, rank: str, *args):
        time_s = get_time_s()

        if self.path:
            with self.path.open("a+", encoding="utf8") as f:
                args_s = " ".join(str(arg) for arg in args)
                text = f"{time_s} [{rank}] {args_s}\n"
                f.write(text)

        # time
        print(Fore.GREEN + time_s + Fore.RESET, end=" ")

        # rank
        color = self.color_dict.get(rank, Fore.RESET)
        print("[" + color + rank + Fore.RESET + "]", end=" ")

        # args
        for arg in args:
            print(str(arg), end=" ")
        print()

    def info(self, *args):
        self.base_print("INFO", *args)

    def success(self, *args):
        self.base_print("SUCCESS", *args)

    def warning(self, *args):
        self.base_print("WARNING", *args)

    def error(self, *args):
        self.base_print("ERROR", *args)

    def debug(self, *args):
        self.base_print("_DEBUG_", *args)


log = Logger()


def get_time_s(time_i=-1, format="%Y/%m/%d %H:%M:%S"):
    if time_i < 0:
        return datetime.now().strftime(format)
    return datetime.fromtimestamp(time_i).strftime(format)


def get_time_i(time_s: str = '', format: str = r'%Y/%m/%d %H:%M:%S'):
    '''
        - time_s存在时，转换time_s为对应time_i，time_s必须完整包含时间、日期
        - time_s缺失时，则返回当前时间日期
    '''
    if not time_s:
        return int(datetime.now().timestamp())
    return int(datetime.strptime(time_s, format).timestamp())


def div_url(url: str):
    '''输入网址，自动分离简单api与参数对'''
    if '?' not in url:
        return url, {}

    api, params_str = url.split('?', maxsplit=1)

    items = [pair.split("=") for pair in params_str.split('&') if pair]
    # 不能提前unquote，因为一些参数内可能包含了=#?%等符号
    # 所以只有到最后一步才可以转义回去
    params = {item[0]: unquote(item[1]) for item in items}

    return api, params


def combine_url(url: str, params: dict):
    if not params:
        return url

    return url + '?' + '&'.join(f"{k}={v}" for k, v in params.items())


def strQ2B(ustring):
    '''全角转半角 一些网页可能会用上'''
    return unicodedata.normalize("NFKC", ustring)


USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]


def get_user_agent():
    return choice(USER_AGENT_LIST)


class Saver:
    def __init__(self, *path: str, mode="a+") -> None:
        self.path = Path(*path)
        if not self.path.parent.exists():
            self.path.parent.mkdir(parents=True)
        self.mode = mode

    @classmethod
    def create_saver(self, path: str, suffix=".json"):
        '''默认依据时间日期创建a+模式的saver'''
        if not path:
            return None

        date = get_time_s(format="%Y-%m-%d")
        file = get_time_s(format="%H-%M-%S") + suffix
        return Saver("data", path, date, file)

    def save(self, data):
        with self.path.open(self.mode, encoding="utf8") as f:
            s = json.dumps(data, ensure_ascii=False)
            f.write(s + "\n")

    def save_text(self, text: str):
        with self.path.open(self.mode, encoding="utf8") as f:
            f.write(text + "\n")

    def save_list(self, iterable) -> None:
        with self.path.open(self.mode, encoding="utf8") as f:
            for data in iterable:
                s = json.dumps(data, ensure_ascii=False)
                f.write(s + "\n")
