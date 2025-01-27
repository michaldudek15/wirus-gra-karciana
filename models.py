class Card:
    "Bazowa klasa reprezentująca kartę."
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, description={self.description})"

class Organ(Card):
    "Klasa reprezentująca organ."
    def __init__(self, name: str, color: str, description: str):
        super().__init__(name, description)
        self.color = color
        self.status = "sterylny"

    def __repr__(self):
        return (f"Organ(name={self.name}, color={self.color}, "
                f"status={self.status}, description={self.description})")

class Wirus(Card):
    "Klasa reprezentująca wirusa."
    def __init__(self, name: str, color: str, description: str):
        super().__init__(name, description)
        self.color = color

    def __repr__(self):
        return f"Wirus(name={self.name}, color={self.color}, description={self.description})"

class Szczepionka(Card):
    "Klasa reprezentująca szczepionkę."
    def __init__(self, name: str, color: str, description: str):
        super().__init__(name, description)
        self.color = color

    def __repr__(self):
        return f"Szczepionka(name={self.name}, color={self.color}, description={self.description})"
    
class Terapia(Card):
    "Klasa reprezentująca kartę terapii."
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    
    def __repr__(self):
        return f"Terapia(name={self.name}, description={self.description})"
    
class Player:
    "Klasa reprezentująca gracza."
    def __init__(self, player_id: int, name: str):
        self.player_id = player_id
        self.name = name
        self.hand = []  # Lista kart w ręce
        self.organsOnTable = {}  # Słownik: nazwa organu -> status

    def printCardsOnHand(self):
        "Wyświelt karty z ręki."
        indeks = 0
        for karta in self.hand:
            print(indeks, "–", karta)
            indeks += 1

    def drawCard(self, deck: list):
        "Dobierz kartę z talii do ręki gracza."
        if not deck:
            raise ValueError("Talia jest pusta!")
        card = deck.pop()
        self.hand.append(card)
        return card
    
    def discardCardFromHand(self, card: Card, deck: list, discardPile: list):
        "Odrzuć kartę na stos kart odrzuconych."
        discardPile.append(card)
        self.hand.remove(card)
        self.drawCard(deck)

    def playCard(self, card: Card, deck: list, discardPile: list, target=None):
        "Zagraj kartę z ręki."
        if card not in self.hand:
            raise ValueError(f"Karta {card.name} nie znajduje się w ręce gracza!")

        self.hand.remove(card)

        if isinstance(card, Organ):
            if card.name in self.organsOnTable:
                raise ValueError(f"Organ {card.name} już znajduje się na stole gracza {self.name}!")
            self.organsOnTable[card.name] = "sterylny"
            print(f"{self.name} zagrał organ {card.name}.")
        
        # TODO
        elif isinstance(card, Szczepionka):
            print("ZAGRANIE SZCZEPIONKI\n")

        # TODO
        elif isinstance(card, Wirus):
            print("ZAGRANIE WIRUSA\n")

        # TODO
        elif isinstance(card, Terapia):
            print("ZAGRANIE TERAPII\n")

        self.drawCard(deck)

    def __repr__(self):
        return (f"Player(player_id={self.player_id}, name={self.name}, "
                f"hand={[card.name for card in self.hand]})")


class GameState:
    "Klasa reprezentująca aktualny stan gry."
    def __init__(self):
        self.players = []
        self.currentPlayerId = 0
        self.deck = []  
        self.discardPile = []

    def nextTurn(self):
        self.currentPlayerId = (self.currentPlayerId + 1) % len(self.players)

    def addPlayer(self, player: Player):
        self.players.append(player)

    def __repr__(self):
        return (
            f"GameState(\n"
            f"  Aktualny gracz: {self.players[self.currentPlayerId].name if self.players else 'None'},\n"
            f"  Gracze: {[player.name for player in self.players]},\n"
            f"  Organy: {[player.organsOnTable for player in self.players]} \n"
            f"  Rozmiar talii: {len(self.deck)},\n"
            f"  Rozmiar stosu kart odrzuconych: {len(self.discardPile)},\n"
            f")"
        )
