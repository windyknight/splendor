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

    def canBuy(self, mony, bonus, gold):
        return (mony+bonus)-self.cost <= gold

class NobleCard(SplendorCard):
    def __init__(self, cost):
        super().__init__(3, cost, None)

    def willVisit(self, bonus):
        return bonus > self.cost

class SplendorDeck(Stack):
    def __init__(self, cards):
        if isinstance(cards, list):
            cards = list(cards)
        super().__init__()
        while cards:
            super().push(cards.pop())
        self.shuffle()

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
        self.devs = {'d':[], 's':[], 'e':[], 'r':[], 'o':[]}
        self.mony = GemSet()
        self.bonus = GemSet()
        self.gold = 0
        self.prestige = 0

    def addGem(self, amt, gem):
        self.mony.addGem(amt, gem)

    def removeGem(self, amt, gem):
        self.mony.removeGem(amt, gem)

    def addGold(self):
        self.gold += 1

    def removeGold(self):
        self.gold = max(0, self.gold - 1)

    def addToHand(self, card):
        self.hand.append(card)

    def getHandSize(self):
        return len(self.hand)

class GemSet:
    """
    Arrangement:
    D S E R O
    """
    def __init__(self, d=0, s=0, e=0, r=0, o=0):
        self.mony = [d,s,e,r,o]
        self.trans = {'d':0, 's':1, 'e':2, 'r':3, 'o':4}

    def __gt__(self, other):
        """
        For comparing between GemSets.
        """
        for i in range(5):
            if self.mony[i] < other.mony[i]:
                return False
        return True

    def __add__(self, other):
        """
        For adding GemSets together.
        """
        a = self.mony[0]+other.mony[0]
        b = self.mony[1]+other.mony[1]
        c = self.mony[2]+other.mony[2]
        d = self.mony[3]+other.mony[3]
        e = self.mony[4]+other.mony[4]
        return GemSet(a,b,c,d,e)

    def __sub__(self, other):
        """
        To determine the min-zero difference between two GemSets.
        Example:
        (1, 2, 3, 4, 5) - (5, 4, 3, 2, 1) = 0 + 0 + 0 + 2 + 4 = 6
        (5, 4, 3, 2, 1) - (0, 0, 0, 0, 0) = 5 + 4 + 3 + 2 + 1 = 15
        """
        ans = 0
        for i in range(5):
            ans += max(0, self.mony[i]-other.mony[i])
        return ans

    def addGem(self, amt, gem):
        i = self.trans[gem.lower()]
        self.mony[i] += max(0, amt)

    def removeGem(self, amt, gem):
        i = self.trans[gem.lower()]
        self.mony[i] = max(0, self.mony[i]-amt)

    def getAmt(self, gem):
        i = self.trans[gem.lower()]
        return self.mony[i]

    def getTotal(self):
        ans = 0
        for i in self.mony:
            ans += i
        return ans


class SplendorGame:
    def __init__(self, numPlayers):
        tier1 = []
        tier2 = []
        tier3 = []
        nobility = []
        self.setup = {2:[4, False, 3], 3:[5, False, 4], 4:[7, True, 5]} #num per gem, can touch gold, num of nobles
        self.trans = {'d':0, 's':1, 'e':2, 'r':3, 'o':4}


        self.rules = self.setup[numPlayers]
        self.numPlayers = numPlayers
        self.gemPool = GemSet(self.rules[0], self.rules[0], self.rules[0], self.rules[0], self.rules[0])
        self.gold = self.rules[0]
        self.decks = [SplendorDeck(nobility), SplendorDeck(tier3), SplendorDeck(tier2), SplendorDeck(tier1)]
        self.rows = [[self.decks[0].deal() for i in range(self.rules[2])], [self.decks[1].deal() for i in range(3)], [self.decks[2].deal() for i in range(3)], [self.decks[3].deal() for i in range(3)]]
        self.players = [SPlayer(input("Player"+str(i+1)+"'s name: ")) for i in range(self.numPlayers)]
        self.gameOver = False
        self.current = 0
        self.actionTaken = False

    def hasEnded(self):
        return self.gameOver

    def endTurn(self):
        #end of turn stuff happens here
        #
        pass

    def take3Diff(self, a, b, c):
        a = a.lower()
        b = b.lower()
        c = c.lower()
        if a == b or a == c or b == c:
            print("Must be 3 different gems!")
        else:
            p = self.players[self.current]
            p.addGem(1, a)
            p.addGem(1, b)
            p.addGem(1, c)
            self.endTurn()

    def take2Same(self, a):
        if self.gemPool.getAmt(a) >= 4:
            p = self.players[self.current]
            p.addGem(2, a)
            self.endTurn()

    def reserveCard(self, row, col):
        p = self.players[self.current]
        if p.getHandSize < 3:
            p.addToHand(self.rows[row].pop(col))
            self.endTurn()

    def buyCard(self, isOnBoard):
        p = self.players[self.current]
        pass





game = SplendorGame(4)