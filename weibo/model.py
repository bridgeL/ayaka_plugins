from bs4 import BeautifulSoup


class Card:
    def __init__(self, data) -> None:
        self.pic_ids = []
        self.id = ""
        self.date = ""
        self.text = ""

        try:
            self.pic_ids = data["mblog"]["pic_ids"]
            self.id = data["mblog"]["id"]
            self.date = data["mblog"]["created_at"]
            self.text = BeautifulSoup(data["mblog"]["text"], "html.parser").get_text("\n", True)
        except:
            pass

    @property
    def urls(self):
        return [f"https://wx4.sinaimg.cn/large/{id}.jpg" for id in self.pic_ids]
