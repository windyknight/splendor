from linkedlists import Stack
from random import shuffle

class SplendorCard:
    '''
    This class creates a basic Splendor Card.
    '''
    def __init__(self, prestige, cost, bonus):
        '''
        Properties of SplendorCard class.
        '''
        self.prestige = prestige
        self.cost = cost
        self.bonus = bonus

class DevCard(SplendorCard):
    '''
    This class is a SplendorCard subclass for development cards.
    '''
    def __init__(self, prestige, cost, bonus):
        '''
        Properties of DevCard class.
        '''
        super().__init__(prestige, cost, bonus)

    def canBuy(self, mony, bonus, gold):
        '''
        Returns a boolean value if the development card is buyable.
        '''
        return (mony+bonus)-self.cost <= gold

class NobleCard(SplendorCard):
    '''
    This class is a SplendorCard subclass for noble cards.
    '''
    def __init__(self, cost):
        '''
        Properties of NobleCard class.
        '''
        super().__init__(3, cost, None)

    def willVisit(self, bonus):
        '''
        Returns a boolean value if the noble will visit the player.
        '''
        return bonus > self.cost

class SplendorDeck(Stack):
    '''
    This class creates the Splendor's deck as a stack.
    '''
    def __init__(self, cards):
        '''
        Properties of SplendorDeck class.
        '''
        if isinstance(cards, list):
            cards = list(cards)
        super().__init__()
        while cards:
            super().push(cards.pop())
        self.shuffle()

    def shuffle(self):
        '''
        Shuffles the deck.
        '''
        cards = []
        while not super().empty():
            cards.append(super().pop())
        shuffle(cards)
        while cards:
            super().push(cards.pop())

    def deal(self):
        '''
        Removes the head node of the stack.
        '''
        return super().pop()

class SPlayer:
    '''
    This class creates the player of the game.
    '''
    def __init__(self, name):
        '''
        Properties of SPlayer class.
        '''
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
        '''
        Returns a boolean value if the a player has less than the other player's number of development cards.
        '''
        return self.getNumDevs() < other.getNumDevs()

    def addGem(self, amt, gem):
        '''
        Adds the gem to the player's property.
        '''
        self.mony.addGem(amt, gem)

    def removeGem(self, amt, gem):
        '''
        Removes the gem from the player's property.
        '''
        self.mony.removeGem(amt, gem)

    def addGold(self):
        '''
        Adds gold to the player's property.
        '''
        self.gold += 1

    def removeGold(self, amt):
        '''
        Removes gold from the player's property.
        '''
        self.gold = max(0, self.gold - max(0, amt))

    def addToHand(self, card):
        '''
        Adds the card to the player's hand.
        '''
        self.hand.append(card)

    def getHandSize(self):
        '''
        Returns the number of cards of the player.
        '''
        return len(self.hand)

    def canBuyCard(self, card):
        '''
        Returns a boolean value if the card is buyable from the field.
        Inherits the canBuy() function from the DevCard class.
        '''
        return card.canBuy(self.mony, self.bonus, self.gold)

    def canBuyFromHand(self, num):
        '''
        Returns a boolean value if the card is buyable from the player's hand.
        Inherits the canBuyCard() function from this class.
        '''
        return self.canBuyCard(self.hand[num])

    def canBeVisited(self, noble):
        '''
        Returns a boolean value if the noble will visit the player.
        Inherits the willVisit() function from the NobleCard class.
        '''
        return noble.willVisit(self.bonus)

    def buyCard(self, card):
        '''
        Gives the player the card he/she wants to buy and returns the cost of card and gold used by the player.
        '''
        cost = card.cost ^ self.bonus
        a = 0
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
        self.mony = self.mony ^ cost
        self.bonus.addGem(1, card.bonus.lower())
        self.devs[card.bonus.lower()].append(card)
        self.prestige += card.prestige
        return (cost, a)

    def getNumTokens(self):

        '''
        Returns the number of tokens the player has.
        '''
        return (self.mony.getTotal() + self.gold)

    def receiveNoble(self, noble):
        '''
        Appends the noble to the player's properties and adds prestige to the player.
        '''
        self.nobles.append(noble)
        self.prestige += noble.prestige

    def getNumDevs(self):
        '''
        Returns the number of development cards the player currently has.
        '''
        ans = 0
        for k, v in self.devs.items():
            ans += len(v)
        return ans

class GemSet:
    """
    This class creates the gems used in the game.
    Arrangement:
    D S E R O
    """
    def __init__(self, d=0, s=0, e=0, r=0, o=0):
        '''
        Properties of the GemSet class.
        '''
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
        '''
        Adds gem to the GemSet.
        '''
        i = self.trans[gem.lower()]
        self.mony[i] += max(0, amt)

    def removeGem(self, amt, gem):
        '''
        Removes gem from the GemSet.
        '''
        i = self.trans[gem.lower()]
        self.mony[i] = max(0, self.mony[i]-amt)

    def getAmt(self, gem):
        '''
        Returns the number of specified gems.
        '''
        i = self.trans[gem.lower()]
        return self.mony[i]

    def getTotal(self):
        '''
        Returns the total number of gems.
        '''
        ans = 0
        for i in self.mony:
            ans += i
        return ans

    def __str__(self):
        '''
        String representation of the gems.
        '''
        s = []
        keys = ["D", "S", "E", "R", "O"]
        for i in range(5):
            s.append(str(self.mony[i])+str(keys[i]))
        return ", ".join(s)

    
class SplendorGame:
    '''
    This class is the game itself.
    '''
    def __init__(self, numPlayers):
        '''
        Properties of SplendorGame.
        '''
        tier1 = [DevCard(1, GemSet(5,4,5,2,1), 'd') for i in range(50)]
        tier2 = [DevCard(1, GemSet(1,4,3,2,1), 'e') for i in range(50)]
        tier3 = [DevCard(1, GemSet(5,4,3,2,3), 'r') for i in range(50)]
        nobility = [NobleCard(GemSet(0,0,3,3,3)),NobleCard(GemSet(3,3,3,0,0)),NobleCard(GemSet(0,3,3,3,0)),NobleCard(GemSet(3,0,0,3,3)),NobleCard(GemSet(3,3,0,0,3)),
                   NobleCard(GemSet(4,4,0,0,0)),NobleCard(GemSet(0,4,4,0,0)),NobleCard(GemSet(4,0,0,4,0)),NobleCard(GemSet(0,0,4,4,0)),NobleCard(GemSet(0,0,0,4,4)),NobleCard(GemSet(4,0,0,0,4))]
        self.setup = {2:[4, False, 3], 3:[5, False, 4], 4:[7, True, 5]} #num per gem, can touch gold, num of nobles
        self.trans = {'d':0, 's':1, 'e':2, 'r':3, 'o':4}
        
        
        self.rules = self.setup[numPlayers]
        self.numPlayers = numPlayers
        self.gemPool = GemSet(self.rules[0], self.rules[0], self.rules[0], self.rules[0], self.rules[0])
        self.gold = 5
        self.decks = [SplendorDeck(nobility), SplendorDeck(tier3), SplendorDeck(tier2), SplendorDeck(tier1)]
        self.rows = [[self.decks[0].deal() for i in range(self.rules[2])], [self.decks[1].deal() for i in range(4)], [self.decks[2].deal() for i in range(4)], [self.decks[3].deal() for i in range(4)]]
        self.players = [SPlayer(input("Player"+str(i+1)+"'s name: ")) for i in range(self.numPlayers)]
        self.gameOver = False
        self.current = 0
        self.actionTaken = False
    
    def processTurn(self):
        '''
        Function for processing the player's turn.
        '''
        p = self.players[self.current]
        #nobles
        print("▓▓▓▓▓▓▓ " * (self.numPlayers + 1))
        toprint = ""
        for noble in self.rows[0]:
            toprint += "▓ {0} {1} ▓ ".format(noble.cost.getAmt('d'), noble.cost.getAmt('s'))
        print(toprint)
        toprint = ""
        for noble in self.rows[0]:
            toprint += "▓{0} {1} {2}▓ ".format(noble.cost.getAmt('e'), noble.cost.getAmt('r'), noble.cost.getAmt('o'))
        print(toprint)
        print("▓▓▓▓▓▓▓ " * (self.numPlayers + 1))

        print("\n")
        
        #devcards
        for i in range(1,4):
            print("░░░░░░░ " * 5)
            toprint = "░░░░░░░ "
            for card in self.rows[i]:
                toprint += "░{0}   {1}░ ".format(card.prestige, card.bonus.upper())
            print(toprint)
            toprint = "░░░{0}░░░ ".format(4-i)
            for card in self.rows[i]:
                toprint += "░ {0} {1} ░ ".format(card.cost.getAmt('d'), card.cost.getAmt('s'))
            print(toprint)
            toprint = "░░░░░░░ "
            for card in self.rows[i]:
                toprint += "░{0} {1} {2}░ ".format(card.cost.getAmt('e'), card.cost.getAmt('r'), card.cost.getAmt('o'))
            print(toprint)
            print("░░░░░░░ " * 5)

        #tokens
        print("AVAILABLE: {0}, {1}G".format(str(self.gemPool), self.gold))

        print("-" * 40)

        while not self.actionTaken:
            #playerinfo
            print("CURRENT PLAYER: " + p.name)
            print("YOU HAVE:  {0} Prestige Points".format(p.prestige))
            print("{0}, {1}G tokens".format(p.mony, p.gold).rjust(40))
            print("{0} in bonuses".format(p.bonus).rjust(40))

            reserved= ""

            for card in p.hand:
                reserved += "░{0}   {1}░ ".format(card.prestige, card.bonus.upper())
            print(reserved)
            reserved = ""
            for card in p.hand:
                reserved += "░ {0} {1} ░ ".format(card.cost.getAmt('d'), card.cost.getAmt('s'))
            print(reserved)
            reserved = ""
            for card in p.hand:
                reserved += "░{0} {1} {2}░ ".format(card.cost.getAmt('e'), card.cost.getAmt('r'), card.cost.getAmt('o'))
            print(reserved)

            #commands
            print("ENTER:      [1] to take tokens")
            print("            [2] to reserve a card")
            print("            [3] to purchase a card")
            com = int(input())
            if com > 3 or com < 0:
                print("Invalid.")
                continue
            if com == 1:
                print("You have chosen to take TOKENS.")
                print("ENTER:      [1] take 3 different tokens")
                print("            [2] take 2 same tokens")
                order = int(input())
                if order == 1:
                    gems = input("Please input 3 gems to take from [D, S, E, R, O]: ").split()
                    if len(gems) == 3 and not ('g' in gems or 'G' in gems):
                        self.take3Diff(gems[0], gems[1], gems[2])
                else:
                    gem = input("Please input gem to take (there must be 4 of that gem available) [D, S, E, R, O]: ")
                    self.take2Same(gem)
            elif com == 2:
                print("You have chosen to RESERVE.")
                row = 4 - int(input("What tier of card do you wish to reserve? [1-3]: "))
                col = int(input("Which card will you reserve? [numbered 1-4 from the left]: ")) - 1
                self.reserveCard(row, col)
            else:
                print("You have chosen to BUY.")
                print("ENTER:      [1] buy card on board")
                print("            [2] buy card from hand")
                econ = int(input())
                if econ == 1:
                    row = 4 - int(input("What tier of card do you wish to buy? [1-3]: "))
                    col = int(input("Which card will you buy? [numbered 1-4 from the left]: ")) - 1
                    self.buyCardFromBoard(row, col)
                elif econ == 2:
                    col = int(input("Which card will you reserve? [numbered 1 onwards from the left]: ")) - 1
                    self.buyCardFromHand(col)
        self.endTurn()

    def hasEnded(self):
        '''
        Returns a self property to end the game.
        '''
        return self.gameOver

    def giveGem(self, player, amt, gem):
        '''
        Gives the gem to the player.
        '''
        amt = max(0, amt)
        if self.gemPool.getAmt(gem) - amt >= 0:
            player.addGem(amt, gem)
            self.gemPool.removeGem(amt, gem)
        else:
            print("Too few gems left to do that.")

    def giveGold(self, player):
        '''
        Gives gold to the player.
        '''
        if self.gold > 0:
            player.addGold()
            self.gold -= 1

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
        '''
        Function for the player to take three different gems
        '''
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
        '''
        Function for the player to take two same gems.
        '''
        if self.gemPool.getAmt(a) >= 4:
            p = self.players[self.current]
            self.giveGem(p, 2, a)
            self.actionTaken = True
        else:
            print("There must be at least 4 tokens of that type left to do that.")

    def reserveCard(self, row, col):
        '''
        Function for the player to reserve a card from the field.
        '''
        p = self.players[self.current]
        if p.getHandSize() < 3:
            p.addToHand(self.rows[row].pop(col))
            if self.rules[1]:
                self.giveGold(p)
            self.actionTaken = True
        else:
            print("You have too many reservations.")

    def buyCardFromBoard(self, row, col):
        '''
        Function for the player to buy a card from the field/board.
        '''
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
        '''
        Function for the player to buy the card from the reserved hand.
        '''
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


while True:
    playerNum = int(input("How many players [2-4]?: "))
    
    if playerNum < 2 or playerNum > 4:
        print("Invalid number of players.")
    else:
        break
        
game = SplendorGame(playerNum)
while not game.hasEnded():
    game.processTurn()
