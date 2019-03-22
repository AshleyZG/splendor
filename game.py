# author: zhangge9194@pku.edu.cn
# file: game.py


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
        # self.players.append(Player(player))

    # def
    def get_token()
