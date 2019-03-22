# author: zhangge9194@pku.edu.cn
# file: card.py


class Card(object):
    """docstring for Card"""

    def __init__(self, arg):
        super(Card, self).__init__()
        # self.arg = arg
        pass


class DevelopCard(Card):
    """docstring for DevelopCard"""

    def __init__(self, arg):
        super(DevelopCard, self).__init__()
        # self.arg = arg
        self.level = arg['level']
        self.score = arg['score']
        self.color = arg['color']
        self.costs = arg['costs']


class Noble(Card):
    """docstring for Noble"""

    def __init__(self, arg):
        super(Noble, self).__init__()
        self.score = arg['score']
        self.requirements = arg['requirements']
