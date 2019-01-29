class Card(object):
    """Одна игральная карта."""
    Ranks = ["A","K","Q","J","10","9","8","7","6","5","4","3","2"]
    Suits = ["c","d","h","s"]

    def __init__(self,rank,suit,face_up = True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up

    def __str__(self):
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep

    def flip(self):
        selfis_face_up = not self.is_face_up
        

class Hand(object):
    """Рука - набор карт на руке."""
    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<пусто>"
        return rep

    def clear(self):
        self.cards = []

    def add(self,card):
        self.cards.append(card)

    def give(self,card,other_hand):
        self.cards.remove(card)
        other_hand.add(card)


class Deck(Hand):
    """Колода игральных карт."""
    def populate(self):
        for suit in Card.Suits:
            for rank in Card.Ranks:
                self.add(Card(rank,suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self,hands,per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card,hand)
                else:
                    print("Карты закончились.")
if __name__ == "__main__":
    print("Это модуль, содержащий классы для карточных игр.")
        
        
