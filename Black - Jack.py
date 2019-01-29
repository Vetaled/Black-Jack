import games,cards

class BJ_Card(cards.Card):
    """Карта для игры в упрощенный Блек-джек."""
    ace_value = 1
    
    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.Ranks.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(cards.Deck):
    """Колода для игры в упрощенный Блек-джек."""
    def populate(self):
        for rank in BJ_Card.Ranks:
            for suit in BJ_Card.Suits:
                self.cards.append(BJ_Card(rank,suit))


class BJ_Hand(cards.Hand):
    """Рука - набор карт Блек-джек у одного игрока. """
    def __init__(self,name):
        super(BJ_Hand,self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand,self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        #если у одной карты значение None , то и у всех остальных тоже
        for card in self.cards:
            if not card.value:
                return None
        #суммирует очки, считая каждый туз за 1 очко
        t = 0
        for card in self.cards:
            t += card.value

        #определяет есть ли тузы у игрока
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ace_value:
                contains_ace = True
        #если на руках есть туз и сумма очков не превышает 11. будем считать туз за 11 очков
        if contains_ace and t <=11:
            #прибавить нужно лишь 10 , потому что 1 вошла в общую сумму пунктом выше
            t+=10
        return t


    def is_busted(self):
        return self.total > 21

    
class BJ_Player(BJ_Hand):
    """Игрок в упрощенном Блек-джеке."""
    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + " - будете брать ещё карты.(y/n): ")
        return response == "y"

    def bust(self):
        print(self.name , "перебор.")
        self.lose()

    def lose(self):
        print(self.name , "проиграл.")

    def win(self):
        print(self.name , "выиграл.")

    def push(self):
        print(self.name , "сыграл с компьютером вничью.")


class BJ_Dealer(BJ_Hand):
    """Дилер в игре Блек-джек"""
    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "перебрал")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BJ_Game(object):
    """Игра в упрощенный Блек-джек"""
    def __init__(self,names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)
        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self,player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        #сдача всем по 2 карты
        self.deck.deal(self.players + [self.dealer],per_hand = 2)
        self.dealer.flip_first_card()#первая карта  переворачивается рубашкой вверх
        for player in self.players:
            print(player)
        print(self.dealer)
        #сдача дополнительных карт
        for player in self.players:
            self.__additional_cards(player)
        self.dealer.flip_first_card() #первая карта дилера открывается
        if not self.still_playing:
            print(self.dealer)#все игроки перебрали, покажем только руку диллера
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                #выигрывают все кто еще остались
                for player in self.still_playing:
                    player.win()
            else:
                #сравниваем очки дилера и оставшихся игроков
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                    elif player.total < self.dealer.total:
                        player.lose()
                    else:
                        player.push()
        #удаление всех карт
        for player in self.players:
            player.clear()
        self.dealer.clear()

def main():
    print("\t\t Добро пожаловать за игровой стол упрощенного Блек-Джека\n")
    names = []
    number = games.ask_number("Сколько всего игроков(1 - 7): ",low = 1, high = 8)
    for i in range(number):
        name = input("Введите имя игрока: ")
        names.append(name)
        print()
    game = BJ_Game(names)
    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nХотите сыграть еще раз?\n")
        main()
    input("\n\n Нажмите Enter, чтобы выйти.")
    
main()
