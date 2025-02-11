from models import Organ, Wirus, Szczepionka, Terapia
import random

def buildDeck():
    "Tworzy i zwraca potasowaną talię kart."
    deck = []

    deck.append(Organ(name=f"serce", color="red", description="organ serca"))
    deck.append(Organ(name=f"serce", color="red", description="organ serca"))
    deck.append(Organ(name=f"serce", color="red", description="organ serca"))
    deck.append(Organ(name=f"serce", color="red", description="organ serca"))
    deck.append(Organ(name=f"serce", color="red", description="organ serca"))

    deck.append(Organ(name=f"żołądek", color="green", description="organ żołądka"))
    deck.append(Organ(name=f"żołądek", color="green", description="organ żołądka"))
    deck.append(Organ(name=f"żołądek", color="green", description="organ żołądka"))
    deck.append(Organ(name=f"żołądek", color="green", description="organ żołądka"))
    deck.append(Organ(name=f"żołądek", color="green", description="organ żołądka"))

    deck.append(Organ(name=f"mózg", color="blue", description="organ mózgu"))
    deck.append(Organ(name=f"mózg", color="blue", description="organ mózgu"))
    deck.append(Organ(name=f"mózg", color="blue", description="organ mózgu"))
    deck.append(Organ(name=f"mózg", color="blue", description="organ mózgu"))
    deck.append(Organ(name=f"mózg", color="blue", description="organ mózgu"))

    deck.append(Organ(name=f"kość", color="yellow", description="organ kości"))
    deck.append(Organ(name=f"kość", color="yellow", description="organ kości"))
    deck.append(Organ(name=f"kość", color="yellow", description="organ kości"))
    deck.append(Organ(name=f"kość", color="yellow", description="organ kości"))
    deck.append(Organ(name=f"kość", color="yellow", description="organ kości"))

    deck.append(Organ(name=f"organ", color="joker", description="organ joker"))

    deck.append(Wirus(name=f"wirus", color="red", description="red wirus"))
    deck.append(Wirus(name=f"wirus", color="red", description="red wirus"))
    deck.append(Wirus(name=f"wirus", color="red", description="red wirus"))
    deck.append(Wirus(name=f"wirus", color="red", description="red wirus"))

    deck.append(Wirus(name=f"wirus", color="green", description="green wirus"))
    deck.append(Wirus(name=f"wirus", color="green", description="green wirus"))
    deck.append(Wirus(name=f"wirus", color="green", description="green wirus"))
    deck.append(Wirus(name=f"wirus", color="green", description="green wirus"))

    deck.append(Wirus(name=f"wirus", color="blue", description="blue wirus"))
    deck.append(Wirus(name=f"wirus", color="blue", description="blue wirus"))
    deck.append(Wirus(name=f"wirus", color="blue", description="blue wirus"))
    deck.append(Wirus(name=f"wirus", color="blue", description="blue wirus"))

    
    deck.append(Wirus(name=f"wirus", color="yellow", description="yellow wirus"))
    deck.append(Wirus(name=f"wirus", color="yellow", description="yellow wirus"))
    deck.append(Wirus(name=f"wirus", color="yellow", description="yellow wirus"))
    deck.append(Wirus(name=f"wirus", color="yellow", description="yellow wirus"))

    deck.append(Wirus(name=f"wirus", color="joker", description="wirus joker"))

    deck.append(Szczepionka(name=f"szczepionka", color="red", description="czerwona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="red", description="czerwona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="red", description="czerwona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="red", description="czerwona szczepionka"))

    deck.append(Szczepionka(name=f"szczepionka", color="green", description="zielona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="green", description="zielona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="green", description="zielona szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="green", description="zielona szczepionka"))

    deck.append(Szczepionka(name=f"szczepionka", color="blue", description="niebieska szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="blue", description="niebieska szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="blue", description="niebieska szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="blue", description="niebieska szczepionka"))

    deck.append(Szczepionka(name=f"szczepionka", color="yellow", description="żółta szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="yellow", description="żółta szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="yellow", description="żółta szczepionka"))
    deck.append(Szczepionka(name=f"szczepionka", color="yellow", description="żółta szczepionka"))

    deck.append(Szczepionka(name=f"szczepionka", color="joker", description="szczepionka joker"))
    deck.append(Szczepionka(name=f"szczepionka", color="joker", description="szczepionka joker"))
    deck.append(Szczepionka(name=f"szczepionka", color="joker", description="szczepionka joker"))
    deck.append(Szczepionka(name=f"szczepionka", color="joker", description="szczepionka joker"))

    # deck.append(Terapia(name="przeszczep", description="Zamień organ pomiędzy ciałami dwóch graczy. Nie ma znaczenia czy organy są tego samego koloru, czy są zdrowe, zarażone, czy zaszczepione. Po prostu zamień wybrany organ z innym, chyba że organ jest uodporniony, albo spowoduje to posiadanie przez gracza dwóch takich samych organów."))
    # deck.append(Terapia(name="przeszczep", description="Zamień organ pomiędzy ciałami dwóch graczy. Nie ma znaczenia czy organy są tego samego koloru, czy są zdrowe, zarażone, czy zaszczepione. Po prostu zamień wybrany organ z innym, chyba że organ jest uodporniony, albo spowoduje to posiadanie przez gracza dwóch takich samych organów."))

    # deck.append(Terapia(name="złodziej organów", description="Ukradnij kartę organu z ciała innego gracza i umieść go w swoim ciele. Możesz skraść zdrowy, zaszczepiony lub zarażony organ, każdy - poza uodpornionym. Pamiętaj, że nie możesz mieć dwóch organów tego samego koloru."))
    # deck.append(Terapia(name="złodziej organów", description="Ukradnij kartę organu z ciała innego gracza i umieść go w swoim ciele. Możesz skraść zdrowy, zaszczepiony lub zarażony organ, każdy - poza uodpornionym. Pamiętaj, że nie możesz mieć dwóch organów tego samego koloru."))
    # deck.append(Terapia(name="złodziej organów", description="Ukradnij kartę organu z ciała innego gracza i umieść go w swoim ciele. Możesz skraść zdrowy, zaszczepiony lub zarażony organ, każdy - poza uodpornionym. Pamiętaj, że nie możesz mieć dwóch organów tego samego koloru."))

    # deck.append(Terapia(name="epidemia", description="Przenieś tyle wirusów, ile możesz ze swoich zarażonych organów na organy innych graczy. Nie możesz użyć karty epidemii na zaszczepione lub zainfekowane organy. Zarażać możesz tylko zdrowe organy."))
    # deck.append(Terapia(name="epidemia", description="Przenieś tyle wirusów, ile możesz ze swoich zarażonych organów na organy innych graczy. Nie możesz użyć karty epidemii na zaszczepione lub zainfekowane organy. Zarażać możesz tylko zdrowe organy."))
    # deck.append(Terapia(name="epidemia", description="Przenieś tyle wirusów, ile możesz ze swoich zarażonych organów na organy innych graczy. Nie możesz użyć karty epidemii na zaszczepione lub zainfekowane organy. Zarażać możesz tylko zdrowe organy."))

    # deck.append(Terapia(name="rękawica lateksowa", description="Wszyscy gracze, oprócz posiadacza karty rękawicy lateksowej, odrzucają karty z ręki na stos kart odrzuconych. W swojej turze gracze ci przechodzą od razu do fazy 2. gry, czyli dobierają 3 karty."))

    # deck.append(Terapia(name="błąd lekarski", description="Wymień całe swoje ciało z ciałem innego gracza, łącznie z organami, wirusami, szczepionkami, a nawet uodpornionymi organami. Nie ma znaczenia ile kart na stole mają gracze, pomiędzy którymi zachodzi wymiana (mogą nawet nie mieć żadnej)."))

    random.shuffle(deck)

    return deck