from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from deck import buildDeck
from models import Card, Organ, Wirus, Szczepionka, Terapia, Player, GameState

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

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
    player1 = Player(1, "player1")
    player2 = Player(2, "player2")

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

    return  render_template('gra-singleplayer.html', player1 = player1, player2 = player2)

@app.route('/zacznijGreMultiplayer')
def graMultiplayer():
    return render_template('todo.html')

@app.route('/zacznijGreHotseat')
def graHotseat():
    return render_template('todo.html')

@app.route('/wybierzKarte', methods=['POST'])
def wybierzKarte():
    global wybranaKarta

# @app.route('/zagrajKarte', methods=['POST'])
# def zagrajKarte():
#     player1_hand = request.form.get('player')

#     return  render_template('gra-singleplayer.html', player1_hand = player1.hand, player2_hand = player2.hand)

if __name__ == "__main__":
    app.run(debug=True)