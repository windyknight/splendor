from linkedlists import Stack
from random import shuffle

class SplendorCard:
    def __init__(self, prestige, cost, bonus):
        self.prestige = prestige
        self.cost = cost
        self.bonus = bonus

class DevCard(SplendorCard):
    def __init__(self, prestige, cost, bonus):
        super().__init__(prestige, cost, bonus)

    def buyable(self, mony, bonus, gold):
        for i in len(super().cost):
            if super().cost[i] is not 0:
                if mony[i] + bonus[i] + gold < super().cost[i]:
                    return False
        return True

class NobleCard(SplendorCard):
    def __init__(self, cost):
        super().__init__(3, cost, None)

    def willVisit(self, capital):
        for i in len(super().cost):
            if super().cost[i] is not 0:
                if capital[i] < super().cost[i]:
                    return False
        return True

class SplendorDeck(Stack):
    def __init__(self, cards):
        if isinstance(cards, list):
            cards = list(cards)
        super().__init__()
        while cards:
            super().push(cards.pop())

    def shuffle(self):
        cards = []
        while not super().empty():
            cards.append(super().pop())
        shuffle(cards)
        while cards:
            super().push(cards.pop())

    def deal(self):
        return super().pop()

class SPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.mony = [0 for i in range(6)]
        self.bonus = [0 for i in range(6)]

class SplendorGame:
    def __init__(self, numPlayers):
        tier1 = []
        tier2 = []
        tier3 = []
        nobility = []
        setup = {2:[4, False, 3], 3:[5, False, 4], 4:[7, True, 5]} #num per gem, can touch gold, num of nobles

        self.rules = setup[numPlayers]
        self.numPlayers = numPlayers
        self.gemPool = [self.rules[0] for i in range(6)]
        self.deck1 = SplendorDeck(tier1)
        self.deck2 = SplendorDeck(tier2)
        self.deck3 = SplendorDeck(tier3)
        self.ndeck = SplendorDeck(nobility)
        self.row1 = [self.deck1.deal() for i in range(3)]
        self.row2 = [self.deck2.deal() for i in range(3)]
        self.row3 = [self.deck3.deal() for i in range(3)]
        self.nrow = [self.ndeck.deal() for i in range(3)]
        self.players = [SPlayer(input("Player"+str(i+1)+"'s name: ")) for i in range(self.numPlayers)]


game = SplendorGame(4)