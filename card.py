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
        super(DevelopCard, self).__init__(arg)
        # self.arg = arg
        # print(arg)
        self.level = arg['level']
        # self.score = arg['score']
        self.score = arg.get('score', 0)
        self.color = arg['color']
        self.costs = arg['costs']

    def to_json(self):
        return {'color': self.color,
                'costs': self.costs,
                'level': self.level,
                'score': self.score}

    # def to_json_purchase(self):
    #     return {'color': self.color,
    #             'costs': self.costs,
    #             'level': self.level,
    #             'score': self.score}


class Noble(Card):
    """docstring for Noble"""

    def __init__(self, arg):
        super(Noble, self).__init__(arg)
        self.score = arg['score']
        self.requirements = arg['requirements']
