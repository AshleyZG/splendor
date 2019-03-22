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
        for card in arg['cards']:
            self.cards.append(DevelopCard(card))
        for noble in arg['nobles']:
            self.nobles.append(Noble(noble))
