# -*- coding: utf-8 -*-
# author: zhangge9194@pku.edu.cn
# file: game.py

import random
import json
import sys

from table import Table
from player import Player

COLORS = ['green', 'white', 'blue', 'black', 'red', 'gold']


class Game(object):
    """docstring for Game"""

    def __init__(self, states):
        super(Game, self).__init__()
        self.round = states['round']
        self.player_name = states['playerName']
        self.table = Table(states['table'])
        self.players = {}

        for player in states['players']:
            self.players[player['name']] = Player(player)

        self.scarcity = self.get_scarcity()

    def move(self):
        # 如果是 round 1，随机选择三个颜色的卡
        if self.round == 1:
            return {"get_different_color_gems": random.sample(COLORS, 3)}
        # 如果手上的牌加保留牌大于15， 则开始购买保留牌
        SCORED = False
        'to be finished'
        result = None

        card_reserved = self.purchase_card(
            self.players[self.player_name].reserved_cards)
        # 首先购买卡片，在purchase 和 reserved 中选择面值最大的
        card_purchased = self.purchase_card(self.table.cards)

        if card_reserved != None:
            result = {"purchase_reserved_card": card_reserved.to_json()}
            if card_reserved.score > 0:
                SCORED = True
        if card_purchased != None:
            result = {"purchase_card": card_purchased.to_json()}
            if card_purchased.score > 0:
                SCORED = True

        # 如果分数大于12的话，优先购买分数高的卡
        if self.players[self.player_name].score >= 12 and card_reserved != None and card_purchased != None:
            if card_reserved.score >= card_purchased.score:
                result = {"purchase_reserved_card": card_reserved.to_json()}
            else:
                result = {"purchase_card": card_purchased.to_json()}

        # 如果无法购买，查看是否能够保留

        # 既不能购买也不能保留，就拿gem
        colors = self.get_gems()
        if len(colors) == 2 and colors[0] == colors[1]:
            candidate = {"get_two_same_color_gems": colors[0]}
        elif len(colors) > 0:
            candidate = {"get_different_color_gems": colors}
        else:
            candidate = {}
            card = self.reserve_card()
            if card != None:
                result = {"reserve_card": {"card": card.to_json()}}

        if not SCORED and candidate == {} and self.players[self.player_name].score + self.players[self.player_name].reserved_score >= 15:
            card = self.reserve_other_card()
            if card != None:
                result = {"reserve_card": {"card": card.to_json()}}

        if result == None:
            result = candidate

        noble = self.check_noble()
        if noble != None:
            result['noble'] = noble.to_json()
        return result

    def get_gems(self):
        # print('=' * 20, '[Get gems]', '=' * 20)
        cards_score = [(card, self._priority_level(card))
                       for card in self.table.cards + self.players[self.player_name].reserved_cards]

        cards_score = sorted(cards_score, key=lambda x: -x[1][0])

        chosen = []
        max_len = min(10 - self.players[self.player_name].gems_count, 3)
        for card in cards_score:
            dist = card[1][1]
            colors = sorted(list(dist.keys()), key=lambda x: dist[x])
            for color in colors:

                if len(chosen) >= max_len:
                    return chosen
                # 如果该颜色的拥有量已经超过上限，则跳过
                if self.players[self.player_name].purchase_power[color] >= self.table.upper_bound[color]:
                    continue
                if chosen == [] and self.table.get_two_same(color):
                    chosen = [color, color]
                    return chosen
                if color not in chosen and self.table.get_gem(color):
                    chosen.append(color)
        return chosen

    def purchase_card(self, cards):
        '''
        return: DevelopCard / None
        '''
        # print('=' * 20, 'purchase', '=' * 20)
        for card in cards:
            if self.players[self.player_name].afford_develop_card(card):
                return card
        return None

    def reserve_other_card(self):
        if not self.players[self.player_name].reserve_available():
            return None
        player_names = [name for name in self.players.keys()
                        if name != self.player_name]
        for card in self.table.cards:
            for name in player_names:
                if self.players[name].reserve_develop_card(card, bias=card.level - 1) and self.players[name].score + card.score >= 15 and card.score > 0:
                    return card
        return None

    def reserve_card(self):
        # print('=' * 20, 'reserve', '=' * 20)
        if not self.players[self.player_name].reserve_available():
            return None
        cards = sorted(self.table.cards,
                       key=lambda x: -self._priority_level(x)[0])
        for card in cards:
            if self.players[self.player_name].reserve_develop_card(card):
                return card
        return None

    def _priority_level(self, card):
        '计算卡的优先级'
        # return: priority, dist
        score = card.score
        dist = self.players[self.player_name].purchase_dist(card)
        total_dist = sum([dist[color] for color in dist.keys()])
        scarcity = self.scarcity[card.color]
        return 0.5 * score - 1 * total_dist + 0.5 * scarcity, dist
        pass

    def get_scarcity(self):
        '用于判断发展卡的红利的稀缺程度'
        scarcity = {'green': 0, 'white': 0,
                    'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        # upper bound - purchase power
        for color in self.table.upper_bound.keys():
            scarcity[color] = max(0, self.table.upper_bound[color] -
                                  self.players[self.player_name].purchase_power[color])
        return scarcity

    def check_noble(self):
        '检查是否有noble 可获得，返回对应的noble card / None'
        for card in self.table.nobles:
            if self.players[self.player_name].afford_noble(card):
                return card
        return None


if __name__ == '__main__':

    if sys.argv[1].endswith('.json'):
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.loads(sys.argv[1])

    game = Game(data)
    with open('{}_{}.json'.format(game.round, game.player_name), 'w') as fout:
        fout.write(json.dumps(data, indent=2))
    move = game.move()

    print(json.dumps(move, ensure_ascii=False, indent=2))

    with open('act_{}.txt'.format(game.player_name), 'w' if game.round == 1 else 'a') as fout2:
        fout2.write('round {}'.format(game.round))
        fout2.write('\n')
        fout2.write(json.dumps(move, ensure_ascii=False, indent=2))
        fout2.write('\n')
    # print(game.players[game.player_name].gems)
    # print(game.players[game.player_name].gems_count)
