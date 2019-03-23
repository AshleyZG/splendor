# author: zhangge9194@pku.edu.cn
# file: player.py

from card import DevelopCard, Noble


class Player(object):
    """docstring for Player"""

    def __init__(self, arg):
        super(Player, self).__init__()
        self.name = arg['name']
        self.score = arg.get('score', 0)
        # print(arg.keys())
        # 如果用户当前没有，返回空list
        self.gems = arg.get('gems', [])
        self.gems_count = sum([gem['count'] for gem in self.gems])
        self.purchased_cards = []
        self.reserved_cards = []
        self.nobles = []
        for card in arg.get('purchasedCards', []):
            self.purchased_cards.append(DevelopCard(card))
        for card in arg.get('reservedCards', []):
            self.reserved_cards.append(DevelopCard(card))
        for card in arg.get('nobles', []):
            self.nobles.append(Noble(card))
        # print(len(self.reserved_cards))
        self.reserved_cards = sorted(
            self.reserved_cards, key=lambda x: -x.score_cost_ratio)

        self.purchase_power = self._set_purchase_power()
        self.noble_power = self._set_noble_power()

    def token_available(self):
        '判断该用户是否能够拿token'

        return self.gems_count < 10

    def reserve_available(self):
        '判断该用户是否能够拿保留牌'
        # print(len(self.reserved_cards))
        return len(self.reserved_cards) < 3

    def _set_purchase_power(self):
        '玩家对 develop card 的购买力'
        '''
        purchase_power: {'green': 0, 'white': 0, 'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        '''
        purchase_power = {'green': 0, 'white': 0,
                          'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        for gem in self.gems:
            purchase_power[gem['color']] += gem['count']
        for card in self.purchased_cards:
            purchase_power[card.color] += 1
        return purchase_power

    def _set_noble_power(self):
        '玩家对noble 的购买力'
        '''
        noble_power: {'green': 0, 'white': 0, 'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        '''
        noble_power = {'green': 0, 'white': 0,
                       'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        for card in self.purchased_cards:
            noble_power[card.color] += 1
        return noble_power
        pass

    def purchase_dist(self, card):
        dist = {'green': 0, 'white': 0,
                'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        for cost in card.costs:
            dist[cost['color']] = max(
                0, cost['count'] - self.purchase_power[cost['color']])
        return dist

    def afford_develop_card(self, card: DevelopCard):
        '判断用户当前是否能够购买发展卡'
        # print(card.__dict__)
        costs = card.costs
        dist = 0
        for gem in costs:
            dist += max(0, gem['count'] - self.purchase_power[gem['color']])
        # print('dist: ', dist)
        return dist <= self.purchase_power['gold']

    def reserve_develop_card(self, card: DevelopCard):
        '判断用户当前是否应该保留牌'
        # 如果保留牌已有三张，不行
        # print(card.__dict__)
        if len(self.reserved_cards) > 3:
            return False

        if card.level == 1 and card.score == 0:
            return False
        costs = card.costs
        dist = 0
        for gem in costs:
            dist += max(0, gem['count'] - self.purchase_power[gem['color']])

        # print(dist)
        return dist <= self.purchase_power['gold'] + card.level + 1

    def afford_noble(self, card: Noble):
        '判断用户当前能否获得 noble '
        requirements = card.requirements
        for gem in requirements:
            if gem['count'] > self.noble_power[gem['color']]:
                return False
        return True
