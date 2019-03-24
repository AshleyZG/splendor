# -*- coding: utf-8 -*-
# author: zhangge9194@pku.edu.cn
# file: table.py


from card import DevelopCard, Noble


class Table(object):
    """docstring for Table"""

    def __init__(self, arg):
        super(Table, self).__init__()
        self.gems = arg['gems']
        self.cards = []
        self.nobles = []
        # for card in arg['cards']:
        for card in arg.get('cards', []):
            self.cards.append(DevelopCard(card))
        # for noble in arg['nobles']:
        for noble in arg.get('nobles', []):
            self.nobles.append(Noble(noble))
        self.upper_bound = self._get_upper_limit()
        # 对卡片按照性价比排序
        self.cards = sorted(self.cards, key=lambda x: -x.score_cost_ratio)

        self.gem_count = {item['color']: item.get(
            'count', 0) for item in self.gems}

    def _get_upper_limit(self):
        '计算每种颜色需要的卡的上限'
        bound = {'green': 0, 'white': 0,
                 'blue': 0, 'black': 0, 'red': 0, 'gold': 0}
        for card in self.cards:
            for cost in card.costs:
                bound[cost['color']] = max(bound[cost['color']], cost['count'])
        return bound

    def get_two_same(self, color):
        return self.gem_count[color] >= 4

    def get_gem(self, color):
        return self.gem_count[color] > 0
