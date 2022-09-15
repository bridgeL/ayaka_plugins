# -*- coding: utf-8 -*-

from random import randint, choice, shuffle
from enum import Enum
from asyncio import sleep
from typing import List
from ayaka import *
import inspect


def print_history():
    ss = inspect.stack(0)
    for s in reversed(ss):
        print(s.frame)


helpdoc = '''指令列表: 
[start/run] 开始游戏
[join] 加入游戏
[status] 查看状态
[go/back] 前进/撤退
[rule/doc] 查看规则
[exit/quit] 退出'''

ruledoc = '''1. 前进，玩家翻开一张卡牌
2. 撤退，玩家沿着来时的路径原路返回
3. 遇到宝石，玩家平分宝石，剩余的宝石留在原地
4. 遇到遗物，当且仅当一名玩家撤退时可从卡片上获得遗物
5. 在前进时遇到怪物，第二次遇到将被驱逐出神殿，丢失此轮在神殿中获得的一切收益
6. 前两个被带出的遗物计5分，后3个被带出的遗物计10分'''

greeting = '''欢迎使用印加宝藏2.0
输入[join]加入游戏
输入[start/run]开始游戏
输入[help]可以查看指令列表
输入[rule/doc查看游戏规则
如果在游戏过程中有什么问题或建议，请@灯夜(2692327749)'''

warnings = [
    '人类，离开此地！',
    '吾等奉命守护此地，驱逐一切外来者',
    '别让我第二次看到你'
]

findArtifact = [
    '就是这个！谢谢你帮我找到它！能将这孩子带出神殿么？', '这是……我留下的……遗物？',
    '虽说是我最重要的东西，但埋藏在神殿里的话根本就没意义嘛！',
    '遗物流通于世，这个世界一定会发生某些变化吧~真是期待呢~',
    '遗物拥有特殊的力量，沉睡在神殿里的话是没办法苏醒的呢~'
]

goddess = [
    '有且仅有一个人撤退才能带走遗物哦~趁别人不知道的时候偷偷撤退吧！',
    '说起来，我曾在神殿一共制造了5个魔偶呢~欸？难道说已经见过了？危险了啊，赶快离开比较好哦！'
    '帮我带出遗物的话，宝石什么的，要多少有多少哦~'
    '不能平分的东西为什么不能被带走呢？啊，难道是因为自己得不到的东西也不能让别人得到？'
    '沿原路返回的时候可以拿到来时没能平分的宝石和遗物哦~',
    '<Turquoise>有1积分，<Obsidian>有5积分，<Gold>竟然有10积分吗！？'
    '遗物只要出现了一次就不会再出现了呢~'
    '就算发生的概率再低，对于面对的人来说，概率就是100%呢'
    '只要尺度足够大，一切事件都必然发生，那么，谁是幸运儿呢？'
    '幸运或者不幸，对我来说都没有意义，那是从人类的角度才存在的东西'
]

deads = [
    '下次不要这么贪了哦~'
    '多亏了你们，我重新获得了这只魔偶的控制权呢，你们不会再遇到这孩子了',
    '该说是有勇气呢还是无谋呢还是说盲目自信呢……不是很懂你们这些人类。'
    '不要放弃，下次更加谨慎一点吧！'
]


class Sender:
    def __init__(self, name, uid) -> None:
        self.name = name
        self.uid = uid


class Option(Enum):
    FORWARD = 1,
    RETREAT = 2,
    STATUS = 3,
    RULE = 5,
    HELP = 6,
    GAMESTART = 7,
    START = 8,
    JOINGAME = 9,
    EXIT = 0


class Incan:
    def __init__(self, app: AyakaApp):
        self.status = IncanStatus.READY
        self.members = {}
        self.round = 0
        self.route = []
        self.deck = Deck()
        self.monsters = []
        self.artifact = 0
        self.acquiredArtifact = 0
        self.turn = 0
        self.temples = Deck('Temple')
        self.app = app
        self.completed = False

    def InitPlayer(self, player: Sender):
        treasures = {
            'Turquoise': {
                'number': 0,
                'value': 1
            },
            'Obsidian': {
                'number': 0,
                'value': 5
            },
            'Gold': {
                'number': 0,
                'value': 10
            },
            'Artifact': {
                'number': 0,
                'value': 5
            }
        }
        from copy import deepcopy
        self.members[player.uid] = {
            'status': 0,
            'name': player.name,
            'treasures': treasures,
            'income': deepcopy(treasures)
        }

    async def Execute(self, sender: Sender, option: Option):
        self.option = option
        if self.status is IncanStatus.READY:
            await self.Ready(sender)
        elif self.status is IncanStatus.INQUEUE:
            await self.InQueue(sender)
        elif self.status is IncanStatus.GAMING and sender.uid in self.members:
            await self.Gaming(sender)


    async def InQueue(self, sender: Sender):
        if self.option is Option.EXIT:
            await self.app.send('游戏结束~下次再见~')
            await self.Exit()
        elif self.option is Option.HELP:
            await self.app.send(helpdoc)
        elif self.option is Option.RULE:
            await self.app.send(ruledoc)
        elif self.option is Option.STATUS:
            await self.app.send(self.GetTeamInfo())
        elif self.option is Option.JOINGAME:
            if sender.uid in self.members:
                await self.app.send(f'{sender.name}已经在小队中了，无需重复加入')
            else:
                self.InitPlayer(sender)
                await self.app.send(f'<{sender.name}>加入了小队，当前小队共{len(self.members)}人。')
        elif self.option is Option.START:
            self.status = IncanStatus.GAMING
            await self.app.send('游戏开始，输入[go/back]决定前进/撤退，此指令支持私聊我发出哦~')
            await sleep(1)
            await self.app.send(f'第1轮：{self.temples.Draw().name}')

            device_id = self.app.device.device_id
            for uid in self.members:
                dev = await self.app.abot.get_device(uid)
                if dev:
                    await dev.add_listener(device_id)

    async def Ready(self, sender):
        if self.option is Option.EXIT:
            await self.app.send('游戏结束~下次再见~')
            await self.Exit()
        elif self.option is Option.HELP:
            await self.app.send(helpdoc)
        elif self.option is Option.RULE:
            await self.app.send(ruledoc)
        elif self.option is Option.GAMESTART:
            self.status = IncanStatus.INQUEUE
            self.InitPlayer(sender)
            await self.app.send(greeting)

    async def Gaming(self, sender: Sender):
        if self.option is Option.EXIT:
            await self.app.send('游戏结束~下次再见~')
            await self.Exit()
        elif self.option is Option.HELP:
            await self.app.send(helpdoc)
        elif self.option is Option.RULE:
            await self.app.send(ruledoc)
        elif self.option is Option.STATUS:
            await self.app.send(self.GetGameStatus())
        elif self.option is Option.FORWARD and self.members[sender.uid]['status'] == 0:
            self.members[sender.uid]['status'] = 1
        elif self.option is Option.RETREAT and self.members[sender.uid]['status'] == 0:
            self.members[sender.uid]['status'] = 2

        if self.CheckTurnEnd():
            self.turn += 1
            await self.DoRetreat()
            await sleep(1)
            for uid in self.members:
                if self.members[uid]['status'] == 1:
                    self.members[uid]['status'] = 0
                elif self.members[uid]['status'] == 2:
                    self.members[uid]['status'] = 3
            adventures = [
                uid for uid in self.members if self.members[uid]['status'] == 0]
            if adventures:
                card = None
                if self.turn == 1:
                    card = self.deck.DrawJewel()
                else:
                    card = self.deck.Draw()
                if card.ctype is Card.Type.MONSTER:
                    if card.name in self.monsters:
                        for uid in adventures:
                            for jewel in self.members[uid]['treasures'].values():
                                jewel['number'] = 0
                        await self.app.send(f'第{self.turn}回合, <{">, <".join([self.members[uid]["name"] for uid in adventures])}>被<{card.name}>驱逐出神殿，一无所获\n<概率女神> {choice(deads)}')
                        await sleep(1)
                        self.deck = Deck()
                        self.deck.Remove(card.name)
                        await self.EnterNextRound()
                    else:
                        self.monsters.append(card.name)
                        await self.app.send(f'第{self.turn}回合, 发现了来自<{card.name}>的警告\n<{card.name}>: {choice(warnings)}')
                elif card.ctype is Card.Type.JEWEL:
                    await self.app.send(f'第{self.turn}回合, 发现了宝石<{card.name}>{card.number}枚\n<概率女神> {choice(goddess)}')
                    num = len(adventures)
                    for uid in adventures:
                        self.members[uid]['treasures'][card.name]['number'] += card.number // num
                    card.number = card.number % num
                    self.route.append(card)
                elif card.ctype is Card.Type.ARTIFACT:
                    self.route.append(card)
                    self.artifact += 1
                    await self.app.send(f'第{self.turn}回合, 发现了遗物<{card.name}>\n<概率女神> {choice(findArtifact)}')
            else:
                self.deck = Deck()
                await self.EnterNextRound()

    async def Exit(self):
        device_id = self.app.device.device_id
        for uid in self.members:
            dev = await self.app.abot.get_device(uid)
            if dev:
                await dev.remove_listener(device_id)

        self.completed = True

        f, info = self.app.close()
        await self.app.send(info)

    async def EnterNextRound(self):
        self.turn = 0
        self.monsters.clear()
        self.route.clear()
        for i in range(self.artifact):
            self.deck.DrawArtifact()
        for uid in self.members:
            self.members[uid]['status'] = 0
            for name in self.members[uid]['treasures']:
                self.members[uid]['income'][name]['number'] += self.members[uid]['treasures'][name]['number']
                self.members[uid]['treasures'][name]['number'] = 0
        self.round += 1
        if self.round == 5:
            await self.Clearing()
        else:
            await self.app.send(f'第{self.round}轮结束')
            await sleep(1)
            await self.app.send(f'第{self.round+1}轮：{self.temples.Draw().name}')

    async def Clearing(self):
        alternate = {'uid': [], 'value': 0}
        for uid, member in self.members.items():
            income = 0
            for name, jewel in member['income'].items():
                income += jewel['number'] * jewel['value']
            if income > alternate['value']:
                alternate['uid'].clear()
                alternate['uid'].append(uid)
                alternate['value'] = income
            elif income == alternate['value'] and income > 0:
                alternate['uid'].append(uid)
        if alternate['value'] > 0:
            relic = -1
            winner = []
            for uid in alternate['uid']:
                if self.members[uid]['income']['Artifact']['number'] > relic:
                    relic = self.members[uid]['income']['Artifact']['number'] > relic
                    winner.clear()
                    winner.append(uid)
                elif relic == self.members[uid]['income']['Artifact']['number'] and relic > 0:
                    winner.append(uid)
            for uid in winner:
                trophy = []
                for name, jewel in self.members[uid]['income'].items():
                    trophy.append(f'<{name}>{jewel["number"]}枚')
                await self.app.send(f'<{self.members[uid]["name"]}>带着{", ".join(trophy)}获得了胜利')
                await sleep(1)
                await self.app.send('游戏结束~')
        else:
            await self.app.send('有勇气才能获得宝石哦！')
            await sleep(1)
            await self.app.send('游戏结束~')
        await self.Exit()

    async def DoRetreat(self):
        runaways = [
            uid for uid in self.members if self.members[uid]['status'] == 2]
        num = len(runaways)
        if num == 0:
            return
        for card in self.route:
            for uid in runaways:
                self.members[uid]['treasures'][card.name]['number'] += card.number // num
            if card.ctype is Card.Type.ARTIFACT and num == 1:
                self.acquiredArtifact += 1
                if self.acquiredArtifact > 2:
                    self.members[uid]['treasures'][card.name]['value'] = 10
            card.number = card.number % num
        await self.app.send(f'<{">, <".join([self.members[uid]["name"] for uid in runaways])}>放弃了冒险')

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


class IncanStatus(Enum):
    READY = 0,
    INQUEUE = 1,
    GAMING = 3


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
