import json
from flask import Flask, render_template, url_for, request, redirect, flash, session, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from deck import buildDeck
from models import Card, Organ, Wirus, Szczepionka, Terapia, Player, GameState

app = Flask(__name__)
app.config['SECRET_KEY'] = 'slodkiekotki'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.secret_key = 'tajny_klucz'  # potrzebne do użycia flash()

# strona tytułowa
@app.route('/')
def index():
    return render_template('index.html')

# strona z instrukcją z PDF
@app.route('/instrukcja')
def instrukcja():
    pdf_url = url_for('static', filename='pdf/wirus-instrukcja.pdf')
    return  render_template('instrukcja.html', pdf_url=pdf_url)

# strona z grą singleplayer z jednym botem
@app.route('/zacznijGreSingleplayer')
def graSingleplayer():
    gra = GameState()
    gra.deck = buildDeck()

    player1 = Player("player1")
    player2 = Player("player2")

    testowaKarta1 = Organ("serce", "red", "opis")
    testowaKarta2 = Organ("mózg", "blue", "opis")
    testowaKarta3 = Organ("kość", "yellow", "opis")

    gra.addPlayer(player1)
    gra.addPlayer(player2)

    player1.drawCard(gra.deck)
    player1.drawCard(gra.deck)
    player1.drawCard(gra.deck)

    player2.drawCard(gra.deck)
    player2.drawCard(gra.deck)
    player2.drawCard(gra.deck)

    player1.organsOnTable[testowaKarta1] = testowaKarta1.status
    player1.organsOnTable[testowaKarta2] = testowaKarta2.status
    player2.organsOnTable[testowaKarta3] = testowaKarta3.status

    session['gra'] = gra
    session['player1'] = player1
    session['player2'] = player2
    return  render_template('gra-singleplayer.html', player1 = player1, player2 = player2)

@app.route('/zacznijGreMultiplayer')
def graMultiplayer():
    return render_template('todo.html')

@app.route('/zacznijGreHotseat')
def graHotseat():
    return render_template('todo.html')

@app.route('/zagrajKarte', methods=['POST'])
def zagrajKarte():
# Pobranie danych z formularza
    source_player_id = request.form.get('source_player_id')
    source_card_id   = request.form.get('source_card_id')
    target_player_id = request.form.get('target_player_id')
    target_card_id   = request.form.get('target_card_id')
    
    print("Dane z formularza:")
    print("Source player id:", source_player_id)
    print("Source card id:  ", source_card_id)
    print("Target player id:", target_player_id)
    print("Target card id:  ", target_card_id)

    gra = session.get('gra')
    if not gra:
        print ("brak stanu gry w sesji")

    sourcePlayer = gra.players.get(source_player_id)
    targetPlayer = gra.players.get(target_player_id)

    source_card = None
    for card in sourcePlayer.hand:
        if card.cardId == source_card_id:
            source_card = card
            break

    if source_card is None:
        print("Nie znaleziono karty o id:", source_card_id)
        return "Błąd: Karta nie została znaleziona", 400

    if (sourcePlayer.playCard(source_card, gra.deck, gra.discardPile) == -1):
        komunikat = "niedozwolony ruch"
    else:
        komunikat = ""


    print(gra)
    session['gra'] = gra
    player1 = session.get('player1')
    player2 = session.get('player2')
    
    return  render_template('gra-singleplayer.html', player1 = player1, player2 = player2, komunikat = komunikat)

@app.route('/wymienKarty', methods=['POST'])
def wymienKarty():
    source_player_id = request.form.get('source_player_id')
    first_card_id   = request.form.get('first_card_id')
    second_card_id = request.form.get('second_card_id')
    third_card_id   = request.form.get('third_card_id')

    gra = session.get('gra')
    if not gra:
        flash("Brak stanu gry w sesji!", "error")
        return redirect(url_for('graSingleplayer'))
    
        # Pobierz gracza, który chce wymienić karty
    sourcePlayer = gra.players.get(source_player_id)
    if not sourcePlayer:
        flash("Nie znaleziono gracza o podanym id!", "error")
        return redirect(url_for('graSingleplayer'))
    
    # Budujemy listę identyfikatorów kart do wymiany
    card_ids = [first_card_id, second_card_id, third_card_id]
    cards_to_exchange = []
    for cid in card_ids:
        if cid:  # Jeśli pole nie jest puste
            # Wyszukujemy kartę w ręce gracza o podanym cardId
            card = next((c for c in sourcePlayer.hand if c.cardId == cid), None)
            if not card:
                flash(f"Karta o id {cid} nie znajduje się w ręce gracza!", "error")
                return redirect(url_for('graSingleplayer'))
            cards_to_exchange.append(card)
    
    # Wykonaj wymianę kart (odrzuć wybrane karty, dobierz nowe)
    sourcePlayer.discardCardsFromHand(gra.deck, gra.discardPile, *cards_to_exchange)
    
    # Zaktualizuj stan gry w sesji
    print(gra)
    session['gra'] = gra
    player1 = session.get('player1')
    player2 = session.get('player2')    
    return  render_template('gra-singleplayer.html', player1 = player1, player2 = player2)

# @app.route('/botZagrajKarte', methods=['POST'])
# def zagrajKarte():
#    pass

if __name__ == "__main__":
    app.run(debug=True)