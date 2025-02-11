import json
from flask import Flask, render_template, url_for, request, redirect, flash, session
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
    testowaKarta3 = Organ("kość", "green", "opis")

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

    player1 = gra.players[0]
    player2 = gra.players[1]

    source_card = None
    for card in player1.hand:
        if card.cardId == source_card_id:
            source_card = card
            break

    if source_card is None:
        print("Nie znaleziono karty o id:", source_card_id)
        return "Błąd: Karta nie została znaleziona", 400

    player1.playCard(source_card, gra.deck, gra.discardPile)



    print(gra)
    return  render_template('gra-singleplayer.html', player1 = gra.players[0], player2 = gra.players[1])


# @app.route('/botZagrajKarte', methods=['POST'])
# def zagrajKarte():
#    pass

if __name__ == "__main__":
    app.run(debug=True)