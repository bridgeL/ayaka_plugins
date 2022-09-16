from .model import Player
from ayaka import AyakaApp


def get_sender(app: AyakaApp):
    name = app.event.sender.card if app.event.sender.card else app.event.sender.nickname
    return Player(name, app.event.user_id)
