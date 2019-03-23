# author: zhangge9194@pku.edu.cn
# file: game.py

import random
import json
import sys

from table import Table
from player import Player


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
        # 如果手上的牌加保留牌大于15， 则开始购买保留牌
        'to be finished'
        # 首先购买保留的卡片
        result = None

        card = self.purchase_card(
            self.players[self.player_name].reserved_cards)
        if card != None:
            result = {"purchase_reserved_card": card.to_json()}
        # 尝试购买桌面上的卡片
        card = self.purchase_card(self.table.cards)
        if card != None:
            result = {"purchase_card": card.to_json()}
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
        # for card, _ in cards_score:

        #     self.players[self.player_name].afford_develop_card(card)
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
    with open('{}.json'.format(game.round), 'w') as fout:
        fout.write(json.dumps(data, indent=2))
    move = game.move()

    print(json.dumps(move, ensure_ascii=False, indent=2))

    with open('act.txt', 'w' if game.round == 1 else 'a') as fout2:
        fout2.write('round {}'.format(game.round))
        fout2.write('\n')
        fout2.write(json.dumps(move, ensure_ascii=False, indent=2))
        fout2.write('\n')
    # print(game.players[game.player_name].gems)
    # print(game.players[game.player_name].gems_count)
