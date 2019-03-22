# author: zhangge9194@pku.edu.cn
# file: game.py

import random
import json

from table import Table
from player import Player

SKIP = -1


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

    def move(self):
        '随机选择三种应对方式之一'
        choices = [1, 2, 3, 4]
        choice = random.choice(choices)
        if choice == 1:
            colors = self.get_different_color_gems()
            return {"get_different_color_gems": colors}

        elif choice == 2:
            color = self.get_two_same_color_gems()
            return {"get_two_same_color_gems": color}
        elif choice == 3:
            card = self.purchase_card()
            if card is None:
                return None
            return {"purchase_card": card.to_json()}
        else:
            card = self.reserve_card()
            if card is None:
                return None
            return {"reserve_card": {"card": card.to_json()}}

    def get_different_color_gems(self):
        '''
        return: List of string ['red','blue'] / []
        '''
        if not self.players[self.player_name].token_available():
            return []
        candidate_colors = list(set([gem['color']
                                     for gem in self.table.gems]))
        number = 10 - self.players[self.player_name].gems_count
        colors = random.sample(candidate_colors, min(
            number, len(candidate_colors)))
        return colors

    def get_two_same_color_gems(self):
        '''
        return: string / None
        '''
        candidate_colors = [gem['color']
                            for gem in self.table.gems if gem['count'] >= 4]
        if candidate_colors == []:
            return None
        return random.choice(candidate_colors)

    def purchase_card(self):
        '''
        return: DevelopCard / None
        '''
        cards = sorted(self.table.cards, key=lambda x: x.score)
        for card in cards:
            if self.players[self.player_name].afford_develop_card(card):
                return card
        return None

    def reserve_card(self):
        card = max(self.table.cards, key=lambda x: x.score)

        return card


if __name__ == '__main__':
    with open('sample_splendor_request.json', 'r') as f:
        data = json.load(f)
    game = Game(data)
    move = game.move()
    print(json.dumps(move, ensure_ascii=False, indent=2))
