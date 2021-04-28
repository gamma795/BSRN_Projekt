import random

#Spielmodus wählen

# def spieler_modus():

#     print()
#     text = "Einzelspieler-(e) oder Mehrspielermodus(m) ?\nBitte 'e' oder 'm' eingeben: "
#     modus = input(text).lower()
#     print(modus)

#     if modus == "m":
#         print("Mehrspielermodus gestartet!!")

#     elif modus == "e":
#         print("Einzelspielermodus gestartet!!")

#     else:
#         print("Eingabe ungültig")


#Spielfeldgröße wählen

# def spielfeld_zeilen():
#     zeilen = input("Wieviele Zeilen soll das Spielfeld haben: ")
#     return zeilen


# def spielfeld_spalten():
#     spalten = input("Wieviele Spalten soll das Spielfeld haben: ")
#     return spalten


# Spielfeld erstellen
spielfeld = []
begrenzung = 5
for x in range(0, begrenzung):
    spielfeld.append(["O"] * 5)


# def spielfeld_größe():
#     zeilen = 4  # int(spielfeld_zeilen())
#     spalten = 4  # int(spielfeld_spalten())

#     # leere liste
#     liste_oberhalb = []
#     print()

#     # auffüllen der liste mit zahlen, der spaltenlänge
#     for x in range(spalten + 1):
#         if x == 0:
#             x = "# "

#         liste_oberhalb.append(str(x))
#     print("    ".join(liste_oberhalb))

#     trenn_zeile = ["------" * spalten]
#     print("".join(trenn_zeile))

#     liste = ["A|"] + ["O"] * (spalten)

#     for elm in range(zeilen):
#         print("    ".join(liste))
#     print()



def spielfeld_ausgeben(spielfeld):

    print()
    for zeilen in spielfeld:
       
        print("    ".join(zeilen))
    print()


def random_zeile_setzen():

    ran_zeile = random.randint(1, 5)
    return ran_zeile


def random_spalte_setzen():

    ran_spalten = random.randint(1, 5)
    return ran_spalten

def benutzer_angriff_zeile():
    zeile = input("Gib Zeile an: ")
    return zeile

def benutzer_angriff_spalte():
    spalte = input("Gib Spalte an: ")
    return spalte


flag_check = False

def schiff_beschießen(spielfeld):
    print("Angriff")

    #Zufällig generiert
    schiffs_zeile = random_zeile_setzen()
    #print(schiffs_zeile)

    schiffs_spalte = random_spalte_setzen()
    #print(schiffs_spalte)

    #Benutzereinagen
    zeilen_angabe = int(benutzer_angriff_zeile())
    spalten_angabe = int(benutzer_angriff_spalte())

    global flag_check

    if zeilen_angabe == schiffs_zeile and spalten_angabe == schiffs_spalte:
        print("TREFFER")
        flag_check = True
        spielfeld[zeilen_angabe - 1][spalten_angabe - 1] = "T"
        spielfeld_ausgeben(spielfeld)
    else:
        # if zeilen_angabe not in range(begrenzung) or spalten_angabe not in (begrenzung):
        #     print("Das war außerhalb der Spielfeldes")
        # else:
            print("FLOP")
            spielfeld[zeilen_angabe - 1][spalten_angabe - 1] = "X"
            spielfeld_ausgeben(spielfeld)
            print("-----------------------------")

#spielfeld_größe()

# print(spielfeld_zeilen())
# print(spielfeld_spalten())

# spieler_modus()


#schiff_beschießen(spielfeld)

x = 4
spielfeld_ausgeben(spielfeld)
while x > 0 and flag_check is not True:
    
    schiff_beschießen(spielfeld)
    x -=1

    if flag_check == True:
        x = 0
        break


if x < 1 and flag_check is not True:
    print("Du hast verloren")
else:
    print("Du hast gewonnen")




