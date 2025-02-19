from flask import Flask, render_template, url_for, request, redirect, flash, session, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_socketio import SocketIO
from deck import buildDeck
from models import Card, Organ, Wirus, Szczepionka, Terapia, Player, BotPlayer, GameState

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

# strona z grą hotseat z innym graczem
@app.route('/zacznijGreHotseat')
def graHotseat():
    gra = GameState()
    gra.deck = buildDeck()

    player1 = Player("player1")
    player2 = Player("player2")

    gra.addPlayer(player1)
    gra.addPlayer(player2)

    for i in range (3):
        player1.drawCard(gra.deck, gra.discardPile)
        player2.drawCard(gra.deck, gra.discardPile)

    session['gra'] = gra
    session['player1'] = player1
    session['player2'] = player2
    session['activePlayer'] = gra.activePlayer()
    session['gameMode'] = 'hotseat'

    return  render_template('graHotseat.html', player1 = player1, player2 = player2, activePlayer = gra.activePlayer())

@app.route('/zacznijGreZBotem')
def graZBotem():
    gra = GameState()
    gra.deck = buildDeck()

    player1 = Player("player1")
    bot = BotPlayer("bot")

    gra.addPlayer(player1)
    gra.addPlayer(bot)

    for i in range(3):
        player1.drawCard(gra.deck, gra.discardPile)
        bot.drawCard(gra.deck, gra.discardPile)

    session['gra'] = gra
    session['player1'] = player1
    session['player2'] = bot
    session['activePlayer'] = gra.activePlayer()
    session['gameMode'] = 'singleplayer'

    return render_template('graSingleplayer.html', player1 = player1, bot = bot, activePlayer = gra.activePlayer())

@app.route('/zacznijGreMultiplayer')
def graMultiplayer():
    return render_template('todo.html')

@app.route('/zagrajKarte', methods=['POST'])
def zagrajKarte():

    source_player_id = request.form.get('source_player_id_move')
    source_card_id   = request.form.get('source_card_id')
    target_player_id = request.form.get('target_player_id')
    target_card_id   = request.form.get('target_card_id')
    
    # print("Dane z formularza:")
    # print("Source player id:", source_player_id)
    # print("Source card id:  ", source_card_id)
    # print("Target player id:", target_player_id)
    # print("Target card id:  ", target_card_id)

    komunikat = ""

    gra = session.get('gra')
    if not gra:
        print("brak stanu gry w sesji")

    sourcePlayer = gra.players.get(source_player_id)
    targetPlayer = gra.players.get(target_player_id)

    source_card = None
    for card in sourcePlayer.hand:
        if card.cardId == source_card_id:
            source_card = card
            break
    
    organy = targetPlayer.organsOnTable.keys()

    target_card = None
    for card in organy:
        if card.cardId == target_card_id:
            target_card = card
            break

    if source_card is None:
        print("ERROR: nie znaleziono karty o id:", source_card_id)

    if isinstance(source_card, Organ):
        if (sourcePlayer.playCard(source_card, gra.deck, gra.discardPile) == -1):
            komunikat = "niedozwolony ruch"
    
    elif isinstance(source_card, Szczepionka):
        if target_card_id == "placeholder":
            komunikat = "nie wybrano celu dla szczepionki!"
        elif sourcePlayer.playCard(source_card, gra.deck, gra.discardPile, target_card, targetPlayer) == -1:
            komunikat = "niedozwolony ruch"

    elif isinstance(source_card, Wirus):
        if target_card_id == "placeholder":
            komunikat = "nie wybrano celu dla wirusa!"
        elif sourcePlayer.playCard(source_card, gra.deck, gra.discardPile, target_card, targetPlayer) == -1:
            komunikat = "niedozwolony ruch"

    if komunikat == "":
        gra.nextTurn()
        session['activePlayer'] = gra.activePlayer()

    # print(gra)
    session['gra'] = gra
    player1 = session.get('player1')
    player2 = session.get('player2')
    activePlayer = session.get('activePlayer')
    
    zwyciezca = gra.checkForWinner()

    if zwyciezca:
        komunikat = f"{zwyciezca.name} wygrał grę!"
        session.pop('gra', None)
        return render_template('game-over.html', zwyciezca=zwyciezca, komunikat=komunikat)

    if session.get('gameMode') == 'hotseat':
        return  render_template('graHotseat.html', player1 = player1, player2 = player2, komunikat = komunikat, activePlayer = activePlayer)
    elif session.get('gameMode') == 'singleplayer':
        return  render_template('graSingleplayer.html', player1 = player1, bot = player2, komunikat = komunikat, activePlayer = activePlayer)


@app.route('/wymienKarty', methods=['POST'])
def wymienKarty():
    gra = session.get('gra')
    if gra is None:
        return "Brak stanu gry w sesji", 400

    active_player = gra.activePlayer()
    if active_player is None:
        return "Nie znaleziono aktywnego gracza", 400

    first_card_id = request.form.get('first_card_id', '').strip()
    second_card_id = request.form.get('second_card_id', '').strip()
    third_card_id = request.form.get('third_card_id', '').strip()

    card_ids = [card_id for card_id in [first_card_id, second_card_id, third_card_id] if card_id]

    if not card_ids:
        print("nie wybrano kart do wymiany")

    try:
        active_player.exchangeCards(gra.deck, gra.discardPile, card_ids)
        print("karty zostały wymienione.")
        gra.nextTurn()
        session['activePlayer'] = gra.activePlayer()
    except Exception as e:
        komunikat = str(e)

    session['gra'] = gra

    zwyciezca = gra.checkForWinner()

    if zwyciezca:
        komunikat = f"{zwyciezca.name} wygrał grę!"
        session.pop('gra', None)
        return render_template('game-over.html', zwyciezca=zwyciezca, komunikat=komunikat)

    if session.get('gameMode') == 'hotseat':
        return render_template('graHotseat.html', 
                               player1=session.get('player1'),
                               player2=session.get('player2'),
                               activePlayer=session.get('activePlayer'))
    elif session.get('gameMode') == 'singleplayer':
        return render_template('graSingleplayer.html', 
                               player1=session.get('player1'),
                                bot=session.get('player2'),
                               activePlayer=session.get('activePlayer'))

socketio = SocketIO(app)
if __name__ == "__main__":
    socketio.run(app,
    host='0.0.0.0',
    port=12221,
    debug=True,
    allow_unsafe_werkzeug=True)