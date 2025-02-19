import uuid, random

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
        self.hand = []
        self.organsOnTable = {}

    def printCardsOnHand(self):
        "Wyświelt karty z ręki."
        indeks = 0
        for karta in self.hand:
            print(indeks, "–", karta)
            indeks += 1

    def drawCard(self, deck: list, discardPile: list):
        """
        Dobiera kartę z talii do ręki gracza.
        Jeśli talia jest pusta, uzupełnia ją z odrzuconych i przetasowuje.
        """
        if not deck:
            if not discardPile:
                print("ERROR: talia jest pusta, brak kart do doboru!")
            deck.extend(discardPile)
            discardPile.clear()
            random.shuffle(deck)
            print("Talia została uzupełniona ze stosu odrzuconych i przetasowana.")
        card = deck.pop()
        self.hand.append(card)
        return card
    
    def exchangeCards(self, deck: list, discardPile: list, card_ids: list):
        """
        Wymienia karty z ręki na podstawie podanej listy identyfikatorów.
        Dla każdej karty:
         - usuwa kartę z ręki,
         - dodaje ją do stosu kart odrzuconych,
         - dobiera nową kartę z talii.
        """
        cards_to_exchange = []
        for card_id in card_ids:
            for card in self.hand:
                if card.cardId == card_id:
                    cards_to_exchange.append(card)
                    break

        for card in cards_to_exchange:
            discardPile.append(card)
            self.hand.remove(card)
            self.drawCard(deck, discardPile)

    def playCard(self, card: Card, deck: list, discardPile: list, target=None, targetPlayer=None):
        "Zagraj kartę z ręki."
        if card not in self.hand:
            print("ERROR: karta {card.name} nie znajduje się w ręce gracza!")

        result = 0

        if isinstance(card, Organ):
            for existing_key in self.organsOnTable.keys():
                if hasattr(existing_key, "name"):
                    if existing_key.name == card.name:
                        print("1.Organ {card.name} już znajduje się na stole gracza {self.name}!")
                        result = -1
                else:
                    if existing_key == card.name:
                        print("2.Organ {card.name} już znajduje się na stole gracza {self.name}!")
                        result = -1
            if (result == 0):
                self.hand.remove(card)
                self.organsOnTable[card] = "sterylny"
                print(f"{self.name} zagrał organ {card.name}.")
                self.drawCard(deck, discardPile)
        
        elif isinstance(card, Szczepionka):
            if target is None:
                print("Nie wybrano celu dla szczepionki!")
                return -1

            if not isinstance(target, Organ):
                print("Cel nie jest organem!")
                return -1

            tableOwner = self if targetPlayer is None else targetPlayer

            if target not in tableOwner.organsOnTable:
                print("ERROR: organ {target.name} nie znajduje się na stole gracza {tableOwner.name}!")
                return -1

            if card.color != 'joker' and target.color != 'joker' and card.color != target.color:
                print(f"Szczepionkę koloru {card.color} można zagrać tylko na organ o kolorze {card.color}!")
                return -1

            current_status = tableOwner.organsOnTable[target]

            if current_status == "uodporniony":
                print("Szczepionki nie można zagrać na uodporniony organ!")
                return -1

            if current_status == "sterylny":
                new_status = "zaszczepiony"
            elif current_status == "zaszczepiony":
                new_status = "uodporniony"
            elif current_status == "zawirusowany":
                new_status = "sterylny"
            else:
                print("Nieznany status organu!")
                return -1

            tableOwner.organsOnTable[target] = new_status
            target.status = new_status

            self.hand.remove(card)
            discardPile.append(card)
            self.drawCard(deck, discardPile)

            print(f"{self.name} zagrał szczepionkę na organ {target.name} gracza {tableOwner.name}. Organ zmienił status z {current_status} na {new_status}.")
            return 0

        elif isinstance(card, Wirus):
                    
            if target is None:
                print("Nie wybrano celu dla wirusa!")
                return -1

            if not isinstance(target, Organ):
                print("Cel nie jest organem!")
                return -1

            tableOwner = self if targetPlayer is None else targetPlayer

            if target not in tableOwner.organsOnTable:
                print(f"Organ {target.name} nie znajduje się na stole gracza {tableOwner.name}!")
                return -1

            if card.color != 'joker' and target.color != 'joker' and card.color != target.color:
                print(f"Wirusa koloru {card.color} można zagrać tylko na organ o kolorze {card.color}!")
                return -1

            current_status = tableOwner.organsOnTable[target]

            if current_status == "uodporniony":
                print("Wirusa nie można zagrać na uodporniony organ!")
                return -1

            if current_status == "zaszczepiony":
                new_status = "sterylny"
                tableOwner.organsOnTable[target] = new_status
                target.status = new_status
                print(f"Organ {target.name} gracza {tableOwner.name} zmienił status z {current_status} na {new_status} pod wpływem wirusa.")
            elif current_status == "sterylny":
                new_status = "zawirusowany"
                tableOwner.organsOnTable[target] = new_status
                target.status = new_status
                print(f"Organ {target.name} gracza {tableOwner.name} zmienił status z {current_status} na {new_status} pod wpływem wirusa.")
            elif current_status == "zawirusowany":
                tableOwner.organsOnTable.pop(target)
                discardPile.append(target)
                print(f"Organ {target.name} gracza {tableOwner.name} został usunięty ze stołu pod wpływem wirusa.")
            else:
                print("Nieznany status organu!")
                return -1

            self.hand.remove(card)
            discardPile.append(card)
            self.drawCard(deck, discardPile)

            print(f"{self.name} zagrał wirusa na organ {target.name} gracza {tableOwner.name}.")
            return 0

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
        self.currentPlayerIndex = 0
        self.deck = []  
        self.discardPile = []

    def activePlayer(self):
        players_list = list(self.players.values())
        if not players_list:
            return None
        return players_list[self.currentPlayerIndex]

    def nextTurn(self):
        winner = self.checkForWinner()
        if winner:
            print(f"🎉 Gra zakończona! Zwycięzca: {winner.name} 🎉")
            return
        
        self.currentPlayerIndex = (self.currentPlayerIndex + 1) % len(self.players)
        
        current_player = self.activePlayer()
        print(f"🕹️ Ruch gracza: {current_player.name}")

        if isinstance(current_player, BotPlayer):
            current_player.makeMove(self)
            self.nextTurn()

    def addPlayer(self, player: Player):
        self.players[player.playerId] = player

    def checkForWinner(self):
        for player in self.players.values():
            valid_organs = [
                organ for organ, status in player.organsOnTable.items() 
                if status in {"sterylny", "zaszczepiony", "uodporniony"}
            ]
            if len(valid_organs) >= 4:
                print(f"🎉 Gracz {player.name} wygrał! 🎉")
                self.winner = player
                return player
        return None      

    def refillDeck(self):
        """
        Jeśli talia (deck) jest pusta, przetasowuje karty ze stosu odrzuconych (discardPile)
        i dodaje je do talii, aby można było dalej dobierać karty.
        """
        if not self.deck:
            if not self.discardPile:
                print("ERROR: brak kart do przetasowania: zarówno talia, jak i stos odrzuconych są puste!")
            self.deck.extend(self.discardPile)
            self.discardPile.clear()
            random.shuffle(self.deck)
            print("Talia została uzupełniona ze stosu odrzuconych i przetasowana.")

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

class BotPlayer(Player):
    def __init__(self, name="Bot"):
        super().__init__(name)

    def makeMove(self, gameState: GameState):
        if not self.hand:
            print("Bot nie ma kart w ręce! Dobiera nową kartę.")
            self.drawCard(gameState.deck, gameState.discardPile)
            return
        
        if gameState.checkForWinner():
            return

        # 1. próba zagrania Organu
        for card in self.hand:
            if isinstance(card, Organ):
                if all(existing_card.name != card.name for existing_card in self.organsOnTable.keys()):
                    print(f"🤖 Bot zagrywa Organ: {card.name}")
                    result = self.playCard(card, gameState.deck, gameState.discardPile)
                    if result == 0:
                        if gameState.checkForWinner():
                            return
                        return

        # 2. próba zagrania wirusa
        opponent = next(p for p in gameState.players.values() if p != self)
        if opponent.organsOnTable:
            for card in self.hand:
                if isinstance(card, Wirus):
                    allowed_targets = [
                        organ for organ in opponent.organsOnTable.keys()
                        if (card.color == 'joker' or organ.color == 'joker' or organ.color == card.color)
                    ]
                    if allowed_targets:
                        target = random.choice(allowed_targets)
                        print(f"🤖 Bot zagrywa Wirusa {card.name} na Organ {target.name} gracza {opponent.name}")
                        result = self.playCard(card, gameState.deck, gameState.discardPile, target, opponent)
                        if result == 0:
                            if gameState.checkForWinner():
                                return
                            return

        # 3. próba zagrania szczepionki
        for card in self.hand:
            if isinstance(card, Szczepionka):
                own_organs = list(self.organsOnTable.keys())
                if own_organs:
                    allowed_targets = [
                        organ for organ in own_organs
                        if (card.color == 'joker' or organ.color == 'joker' or organ.color == card.color)
                    ]
                    if allowed_targets:
                        target = random.choice(allowed_targets)
                        print(f"🤖 Bot zagrywa Szczepionkę {card.name} na Organ {target.name}")
                        result = self.playCard(card, gameState.deck, gameState.discardPile, target)
                        if result == 0:
                            if gameState.checkForWinner():
                                return
                            return

        # 4. wymiana kart
        num_cards_to_discard = min(3, len(self.hand))
        cards_to_discard = random.sample(self.hand, num_cards_to_discard)

        for card_to_discard in cards_to_discard:
            print(f"🤖 Bot nie ma dobrego ruchu – odrzuca kartę {card_to_discard.name}")
            self.hand.remove(card_to_discard)
            gameState.discardPile.append(card_to_discard)

        for i in range(num_cards_to_discard):
            self.drawCard(gameState.deck, gameState.discardPile)

        if gameState.checkForWinner():
            return