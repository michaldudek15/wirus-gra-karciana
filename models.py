import uuid

class Card:
    "Bazowa klasa reprezentująca kartę."
    def __init__(self, name: str, description: str):
        self.cardId = str(uuid.uuid4())
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
    def __init__(self, name: str):
        self.playerId = str(uuid.uuid4())
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
    
    def discardCardsFromHand(self, deck: list, discardPile: list, *cards):
        "Odrzuć karty na stos kart odrzuconych."
        for card in cards:
            discardPile.append(card)
            self.hand.remove(card)
            self.drawCard(deck)

    def playCard(self, card: Card, deck: list, discardPile: list, target=None):
        "Zagraj kartę z ręki."
        if card not in self.hand:
            raise ValueError(f"Karta {card.name} nie znajduje się w ręce gracza!")

        result = 0

        if isinstance(card, Organ):
            # Iterujemy po istniejących kluczach w organsOnTable
            for existing_key in self.organsOnTable.keys():
                # Jeśli klucz to obiekt posiadający atrybut 'name'
                if hasattr(existing_key, "name"):
                    if existing_key.name == card.name:
                        print("1.Organ {card.name} już znajduje się na stole gracza {self.name}!")
                        result = -1
                else:
                    # Jeśli klucz jest stringiem, porównujemy bezpośrednio
                    if existing_key == card.name:
                        print("2.Organ {card.name} już znajduje się na stole gracza {self.name}!")
                        result = -1
            # Jeśli nie znaleziono duplikatu, dodajemy obiekt jako klucz
            if (result == 0):
                self.hand.remove(card)
                self.organsOnTable[card] = "sterylny"
                print(f"{self.name} zagrał organ {card.name}.")
                self.drawCard(deck)
        
        # TODO
        elif isinstance(card, Szczepionka):
            print("ZAGRANIE SZCZEPIONKI\n")

        # TODO
        elif isinstance(card, Wirus):
            print("ZAGRANIE WIRUSA\n")

        # TODO
        elif isinstance(card, Terapia):
            print("ZAGRANIE TERAPII\n")

        return result

    def __repr__(self):
        return (f"Player(playerId={self.playerId}, name={self.name}, "
                f"hand={[card.name for card in self.hand]})")


class GameState:
    "Klasa reprezentująca aktualny stan gry."
    def __init__(self):
        self.gameId = str(uuid.uuid4())
        self.players = {}
        self.currentPlayerId = 0
        self.deck = []  
        self.discardPile = []

    def nextTurn(self):
        self.currentPlayerId = (self.currentPlayerId + 1) % len(self.players)

    def addPlayer(self, player: Player):
        self.players[player.playerId] = player

    def __repr__(self):
        return (
            f"GameState(\n"
            # f"  Aktualny gracz: {self.players.get[self.currentPlayerId].name if self.players else 'None'},\n"
            f"  Gracze: {[player.name for player in self.players.values()]},\n"
            f"  Organy: {[player.organsOnTable for player in self.players.values()]} \n"
            f"  Rozmiar talii: {len(self.deck)},\n"
            f"  Rozmiar stosu kart odrzuconych: {len(self.discardPile)},\n"
            f")"
        )
