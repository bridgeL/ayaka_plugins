# -*- coding: utf-8 -*-

from random import randint, choice, shuffle
from enum import Enum
from typing import List


class Player:
    def __init__(self, name, uid) -> None:
        self.name = name
        self.uid = uid


class Incan:
    def __init__(self):
        self.members = {}
        self.round = 0
        self.route: List[Card] = []
        self.deck = Deck()
        self.monsters = []
        self.artifact = 0
        self.acquiredArtifact = 0
        self.turn = 0
        self.temples = Deck('Temple')

    def GetTeamInfo(self):
        return f'队伍玩家有：<{">, <".join([self.members[uid]["name"] for uid in self.members])}>'

    def GetGameStatus(self):
        status = '角色状态：'
        for uid in self.members:
            state = '还在迷茫中' if self.members[uid]['status'] == 0 else None
            if state is None:
                state = '放弃冒险了' if self.members[uid]['status'] == 3 else '决定好了'
            status += f'<{self.members[uid]["name"]}> {state}\n'
        if self.monsters:
            status += f'警告：\n<{">, <".join(self.monsters)}>'
        else:
            status += f'目前没有收到任何警告'
        return status

    def CheckTurnEnd(self):
        for uid in self.members:
            if self.members[uid]['status'] == 0:
                return False
        return True


class Card:
    class Type(Enum):
        TEMPLE = 0,
        JEWEL = 1,
        MONSTER = 2,
        ARTIFACT = 3

        def ToString(self):
            if self is self.TEMPLE:
                return 'Temple'
            elif self is self.JEWEL:
                return 'Jewel'
            elif self is self.MONSTER:
                return 'Monster'
            elif self is self.ARTIFACT:
                return 'Artifact'
            else:
                raise ValueError

    def __init__(self, ctype, name=None, number=1, value=0):
        self.ctype = ctype
        self.name = name if name else ctype.ToString()
        self.number = number
        self.value = value


class Deck:
    def __init__(self, ctype='Quest'):
        self.cardset: List[Card] = []
        if ctype == 'Quest':
            for i in range(5):
                self.cardset.append(
                    Card(Card.Type.JEWEL, 'Gold', number=randint(10, 15), value=10))
                self.cardset.append(
                    Card(Card.Type.JEWEL, 'Obsidian', number=randint(10, 15), value=5))
                self.cardset.append(
                    Card(Card.Type.JEWEL, 'Turquoise', number=randint(10, 15), value=1))
                self.cardset.append(Card(Card.Type.ARTIFACT, value=5))
            for i in range(3):
                self.cardset.append(Card(Card.Type.MONSTER, 'Viper'))
                self.cardset.append(Card(Card.Type.MONSTER, 'Spider'))
                self.cardset.append(Card(Card.Type.MONSTER, 'Mummy'))
                self.cardset.append(Card(Card.Type.MONSTER, 'Flame'))
                self.cardset.append(Card(Card.Type.MONSTER, 'Collapse'))
        elif ctype == 'Temple':
            self.cardset.append(Card(Card.Type.TEMPLE, '第一神殿'))
            self.cardset.append(Card(Card.Type.TEMPLE, '第二神殿'))
            self.cardset.append(Card(Card.Type.TEMPLE, '第三神殿'))
            self.cardset.append(Card(Card.Type.TEMPLE, '第四神殿'))
            self.cardset.append(Card(Card.Type.TEMPLE, '第五神殿'))
        shuffle(self.cardset)

    def Draw(self):
        card = choice(self.cardset)
        self.cardset.remove(card)
        return card

    def Remove(self, name):
        self.cardset = [card for card in self.cardset if card.name != name]

    def DrawArtifact(self):
        card = choice(self.cardset)
        while card.ctype is not Card.Type.ARTIFACT:
            card = choice(self.cardset)
        self.cardset.remove(card)
        return card

    def DrawJewel(self):
        card = choice(self.cardset)
        while card.ctype is Card.Type.MONSTER:
            card = choice(self.cardset)
        self.cardset.remove(card)
        return card
