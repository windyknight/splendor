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
        self.check = ['d', 's', 'e', 'r', 'o']
        self.nobles = []

    def __lt__(self, other):
        return self.getNumDevs() < other.getNumDevs()

    def addGem(self, amt, gem):
        self.mony.addGem(amt, gem)

    def removeGem(self, amt, gem):
        self.mony.removeGem(amt, gem)

    def addGold(self):
        self.gold += 1

    def removeGold(self, amt):
        self.gold = max(0, self.gold - max(0, amt))

    def addToHand(self, card):
        self.hand.append(card)

    def getHandSize(self):
        return len(self.hand)

    def canBuyCard(self, card):
        return card.canBuy(self.mony, self.bonus, self.gold)

    def canBuyFromHand(self, num):
        return self.canBuyCard(self.hand[num])

    def canBeVisited(self, noble):
        return noble.willVisit(self.bonus)

    def buyCard(self, card):
        cost = card.cost ^ self.bonus
        a = 0
        #gold shit
        if self.gold > 0:
            deduct = GemSet()
            a = int(input("How much gold would you like to allocate to this purchase? "))
            a = min(a, self.gold)
            a = max(0, a)
            if a > 0:
                alloc = input("Please enter what gems will be replaced by gold (Example: D D S): ").split()
                for i in alloc:
                    i = i.lower()
                    if i in self.check:
                        deduct.addGem(1,i)
                cost = cost ^ deduct
                self.removeGold(a)
        self.mony = self.mony - cost
        self.bonus.addGem(1, card.bonus.lower())
        self.devs[card.bonus.lower()].append(card)
        self.prestige += card.prestige
        return (cost, a)

    def getNumTokens(self):
        return self.mony.getTotal() + self.gold

    def receiveNoble(self, noble):
        self.nobles.append(noble)
        self.prestige += noble.prestige

    def getNumDevs(self):
        ans = 0
        for k, v in self.devs.items():
            ans += len(v)
        return ans

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

    def __xor__(self, other):
        """
        Hacky way to simply determine the difference between two GemSets.
        """
        a = self.mony[0]-other.mony[0]
        b = self.mony[1]-other.mony[1]
        c = self.mony[2]-other.mony[2]
        d = self.mony[3]-other.mony[3]
        e = self.mony[4]-other.mony[4]
        return GemSet(a,b,c,d,e)

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

    def giveGem(self, player, amt, gem):
        amt = max(0, amt)
        if self.gemPool.getAmt(gem) - amt >= 0:
            player.addGem(amt, gem)
            self.gemPool.removeGem(amt, gem)
        else:
            print("Too few gems left to do that.")

    def giveGold(self, player):
        if self.gold > 0:
            player.addGold()
            self.gold -= 1

    def processTurn(self):
        """
        Print the thing.
        Enter your choice.
        Do things.
        Yeah.
        """
        #print interface crap here
        while not self.actionTaken:
            pass #print queries here
        self.endTurn()

    def endTurn(self):
        """
        End of turn processing.
        1. Checks if player has more than 10 tokens.
        2. Checks for noble visits.
        3. Deals cards to fill in gaps.
        4. Shifts counter to move to next player.
        5. If round is complete, checks if a player has won.
        """
        #end of turn stuff happens here
        p = self.players[self.current]
        if p.getNumTokens() > 10:
            toReturn = input("Please input "+str(p.getNumTokens()-10)+" token/s to return [D, S, E, R, O, G]: ").split()
            for i in toReturn:
                i = i.lower()
                if i == 'g':
                    p.removeGold(1)
                else:
                    p.removeGem(1, i)
        visits = []
        for i in range(len(self.rows[0])):
            if p.canBeVisited(self.rows[0][i]):
                visits.append(i)
        if visits:
            if len(visits) > 1:
                #print the cards??? be warned that visits contains indices
                ans = int(input("Select which noble will visit you [0-"+str(len(visits)-1))+"]: ")
                noble = self.rows[0].pop(visits[ans])
                p.receiveNoble(noble)
            else:
                p.receiveNoble(self.rows[0].pop(visits[0]))
                print("You have been visited by a noble!")
        for i in range(4):
            if i is 0:
                if len(self.rows[i]) < self.rules[2]:
                    self.rows[i].append(self.decks[i].deal())
            else:
                if len(self.rows[i]) < 4:
                    self.rows[i].append(self.decks[i].deal())
        self.current += 1
        self.current %= self.numPlayers
        self.actionTaken = False
        if self.current == 0:
            win = []
            winner = None
            for p in self.players:
                if p.prestige >= 15:
                    win.append(p)
            if win:
                if len(win) > 1:
                    win.sort()
                    winner = win[0]
                else:
                    winner = win[0]
                print(winner.name + " has won! Congratulations!")
                self.gameOver = True

    def take3Diff(self, a, b, c):
        a = a.lower()
        b = b.lower()
        c = c.lower()
        if a == b or a == c or b == c:
            print("Must be 3 different gems!")
        else:
            p = self.players[self.current]
            self.giveGem(p, 1, a)
            self.giveGem(p, 1, b)
            self.giveGem(p, 1, c)
            self.actionTaken = True

    def take2Same(self, a):
        if self.gemPool.getAmt(a) >= 4:
            p = self.players[self.current]
            self.giveGem(p, 2, a)
            self.actionTaken = True
        else:
            print("There must be at least 4 tokens of that type left to do that.")

    def reserveCard(self, row, col):
        p = self.players[self.current]
        if p.getHandSize < 3:
            p.addToHand(self.rows[row].pop(col))
            if self.rules[1]:
                self.giveGold(p)
            self.actionTaken = True
        else:
            print("You have too many reservations.")

    def buyCardFromBoard(self, row, col):
        p = self.players[self.current]
        card = self.rows[row][col]
        if p.canBuyCard(card):
            x = p.buyCard(self.rows[row].pop(col))
            self.gold += x[1]
            self.gemPool = self.gemPool + x[0]
            self.actionTaken = True
        else:
            print("Cannot afford that card.")

    def buyCardFromHand(self, num):
        p = self.players[self.current]
        if num < p.getHandSize() and num >= 0:
            if p.canBuyFromHand(num):
                x = p.buyCard(p.hand.pop(num))
                self.gold += x[1]
                self.gemPool = self.gemPool + x[0]
                self.actionTaken = True
            else:
                print("Cannot afford that card.")
        print("Invalid selection number.")




game = SplendorGame(int(input("How many players [2-4]?: ")))