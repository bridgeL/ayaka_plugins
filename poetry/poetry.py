import json
from ayaka import beauty_save
from ..utils.time import get_time_s
from ..utils.file import LocalPath


class Poetry:
    def __init__(self) -> None:
        self.path = LocalPath(__file__).get_json_path("poetry")

    def load(self) -> dict:
        with self.path.open("r", encoding="utf8") as f:
            data = json.load(f)
        return data

    def get_info(self):
        data = self.load()
        names = [f"《{k}》\n收录时间：{data[k]['time_s']}" for k in data]
        return names

    def get_poetry(self, name):
        data = self.load()
        for k in data:
            if k == name:
                return data[k]
        return None

    def set_last_line_num(self, name, num):
        data = self.load()
        data[name]['last_line_num'] = num
        beauty_save(self.path, data)

    def set_poetry(self, name, lines: list):
        lines = [line for line in lines if line]
        data = self.load()
        data[name] = {
            'time_s': get_time_s(),
            'content': lines
        }
        beauty_save(self.path, data)
