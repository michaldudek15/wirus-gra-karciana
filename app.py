from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from deck import buildDeck
from models import Card, Organ, Wirus, Szczepionka, Terapia, Player, GameState

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

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

@app.route('/zagrajKarte', methods=['POST'])
def zagrajKarte():
    source_card_id = request.form.get('source_card_id')
    target_card_id = request.form.get('target_card_id')

    # Weryfikacja, czy oba identyfikatory zostały przesłane
    if not source_card_id or not target_card_id:
        flash("Błąd: Nie wybrano karty źródłowej lub targetu!")
        return redirect(url_for('graSingleplayer'))

    try:
        source_card_id = int(source_card_id)
        target_card_id = int(target_card_id)
    except ValueError:
        flash("Błąd: Nieprawidłowy identyfikator karty!")
        return redirect(url_for('graSingleplayer'))

    # Znajdź kartę w ręce gracza
    selected_card = None
    for card in player1.hand:
        if card.id == source_card_id:
            selected_card = card
            break

    if not selected_card:
        flash("Błąd: Nie znaleziono karty w ręce!")
        return redirect(url_for('graSingleplayer'))

    # Sprawdź, czy wybrana karta jest organem.
    # Zakładamy, że karta organu ma atrybut 'typ' równy "organ".
    if getattr(selected_card, 'typ', None) != 'organ':
        flash("Błąd: Wybrana karta nie jest organem!")
        return redirect(url_for('graSingleplayer'))

    # Dodaj organ do ciała gracza.
    # Przykładowo, jeśli ciało gracza jest przechowywane w słowniku organsOnTable,
    # gdzie kluczem jest obiekt karty, a wartością jej status:
    player1.organsOnTable[selected_card] = selected_card.status

    # Usuń kartę z ręki gracza
    player1.hand.remove(selected_card)

    flash("Organ został dodany do ciała gracza!")
    return redirect(url_for('graSingleplayer'))
if __name__ == "__main__":
    app.run(debug=True)