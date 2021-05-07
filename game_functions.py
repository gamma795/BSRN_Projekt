import random

import settings

# List of phrases in case of hit or miss
miss_phrases = ["Daneben", "Ein Schuss ins Wasser", "Nicht getroffen", "Du Dödel. Voll verfehlt"]
hit_phrases = ["Volltreffer", "Hit", "Yippee-ki-yay M*****F*****"]


def setup_new_board(board_size):
    """Sets up a new board matrix filled with 0s"""
    board = [["0" for i in range(board_size)] for j in range(board_size)]
    return board


def set_new_player(board_size, other_player_name=" "):
    """Creates a new Player with empty board and scores and asks for a name"""
    player = {}

    # If there is no named player yet, just ask for new name
    if other_player_name == " ":
        player["name"] = str(input("  Wie soll der erste Spieler heißen: "))

    # Else if a named player already exists, ask for new name and compares to other players name
    else:
        while True:
            player["name"] = str(input("  Wie soll der zweite Spieler heißen: "))
            if player["name"] == other_player_name:
                print("  Dieser Name ist schon belegt. Wählen Sie einen anderen Namen.")

            # Only leaves input loop when the two names are different
            else:
                break;

    # Set up a new Empty personnal board, new guesses board and empty list of tried fields
    player["board"] = setup_new_board(board_size)
    player["guesses"] = setup_new_board(board_size)
    player["already_tried"] = []

    return player


def field_filling(value):
    """Sets how the Board position will be displayed and translates board info into graphics"""
    if value == "0":  # empty field
        return "   "
    elif value == "S":  # ship
        return "███"
    elif value == "HS":  # hit ship
        return "▒X▒"
    elif value == "SS":  # sunk ship
        return "░X░"
    elif value == "WG":  # wrong guess
        return " O "
    elif value == "CG":  # correct guess
        return " X "


def draw_boards(player):
    """Draws both the players board and their guess-board side-by-side"""
    # Unicode Symbols for grid
    v = "│"
    h = "─"
    c = "┼"
    re = "┤"
    ce = "┴"
    co = "┘"

    # Titels of the boards
    header_1 = "Ihr Spielfeld"
    header_2 = "Das Spielfeld des Gegners"

    # Spacing between the two boards depended on titel length
    board_spacing = "            "
    header_1_spacing = " " * (len(player["board"][0]) * 4 - len(header_1))

    # Print the Titels
    settings.clear_screen()
    print(f'   {player["name"]} ist dran:')
    print(f"\n        {header_1}{header_1_spacing}{board_spacing}       {header_2}\n")

    # Active player header
    print("        ", end=v)
    for x in range(len(player["board"][0])):
        if x < 9:
            print(f" {x + 1} ", end=v)
        else:
            print(f" {x + 1}", end=v)

    # Opponents side header
    print(board_spacing + "      ", end=v)
    for x in range(len(player["guesses"][0])):
        if x < 9:
            print(f" {x + 1} ", end=v)
        else:
            print(f" {x + 1}", end=v)

    # Active player header spacing
    print("\n        ", end=v)
    for x in range(len(player["board"][0])):
        print(f"   ", end=v)

    # Opponents side header spacing
    print(board_spacing + "      ", end=v)
    for x in range(len(player["guesses"][0])):
        print(f"   ", end=v)

    # Active player first horizontal line
    print("\n  " + h * 6, end=c)
    for x in range(len(player["board"][0])):
        print(h * 3, end=c)

    # Opponents side first horizontal line
    print(board_spacing + h * 6, end=c)
    for x in range(len(player["guesses"][0])):
        print(h * 3, end=c)

    # Active player start the rest of the board
    for y in range(len(player["board"])):
        print(f"\n   {chr(65 + y)}    ", end=v)
        for x in range(len(player["board"][0])):
            field = field_filling(player["board"][y][x])
            print(field, end=v)

        # Opponents side start the rest of the board
        print(f"{board_spacing} {chr(65 + y)}    ", end=v)
        for x in range(len(player["guesses"])):
            field = field_filling(player["guesses"][y][x])
            print(field, end=v)

        print("\n  " + h * 6, end=c)
        for x in range(len(player["board"][0])):
            print(h * 3, end=c)

        print(board_spacing + h * 6, end=c)  # opponent side
        for x in range(len(player["guesses"][0])):
            print(h * 3, end=c)
    print("")


# This function unnecessary for now
def draw_one_board(board):
    """Display only one chosen board"""
    # Header
    print("      ", end="|")
    for x in range(len(board[0])):
        print(f" {x + 1} ", end="|")
    print("\n      ", end="|")
    for x in range(len(board[0])):
        print(f"   ", end="|")
    print("\n------", end="+")
    for x in range(len(board[0])):
        print(f"---", end="+")

    # Field

    for y in range(len(board)):
        print(f"\n {chr(65 + y)}    ", end="|")
        for x in range(len(board[0])):
            field = field_filling(board[y][x])
            print(field, end="|")
        print("\n------", end="+")
        for x in range(len(board[0])):
            print(f"---", end="+")
    print("")


def switch_player(active_player, player_1, player_2):
    """Switches active player and waits for confirmation that only active player is lookig"""
    settings.clear_screen()
    if active_player == player_1:
        active_player = player_2
        print(
            f'  Jetzt ist {player_2["name"]} dran.\n  Tauschen Sie die Plätze und drücken Sie Enter wenn {player_1["name"]} nicht mehr schaut')
    else:
        active_player = player_1
        print(
            f'  Jetzt ist {player_1["name"]} dran.\n  Tauschen Sie die Plätze und drücken Sie Enter wenn {player_2["name"]} nicht mehr schaut')
    input()
    settings.clear_screen()
    return active_player


# Player input to attack
def ask_input_from(player, possible_input):
    """Ask for player input and checks against list of possible inputs and already tried"""
    draw_boards(player)
    print("\n")
    while True:
        try:
            player_input = str(input("  Was ist hier nächster Zug: ")).upper()
            if player_input == "EXIT":
                break;
            if player_input in possible_input:
                if player_input in player["already_tried"]:
                    draw_boards(player)
                    print("\n  Sie haben schon auf dieses Feld geschossen.")
                    continue
                else:
                    player["already_tried"].append(player_input)
                    print(player["already_tried"])
                    break;
            else:
                draw_boards(player)
                print("\n  Das ist keine gültige Eingabe")
                continue

        except ValueError:
            draw_boards(player)
            print("\n  Das ist keine gültige Eingabe")
            continue
    return player_input


# Methode zum Setzen von Schiffen
def ask_input_for_ship(player, possible_input, ship, feld, zahl_der_felder):
    """Ask for player input to set a ship and checks against list of possible inputs and already tried"""
    draw_boards(player)
    print("\n")
    while True:
        try:
            # Gibt an welcher Teil von Schiff z.B 2/3
            print("  Schiff %d Feld %d/%d " % (ship, (feld + 1), (zahl_der_felder)))

            # Nimmt Input und kontrolliert
            player_input = str(input("  Setze ein Schiff: ")).upper()
            if player_input == "EXIT":
                break;
            if player_input in possible_input:
                if player_input in player["already_tried"]:
                    draw_boards(player)
                    print("\n  Dieses Feld ist bereits besetzt.")
                    continue
                else:
                    player["already_tried"].append(player_input)
                    print(player["already_tried"])
                    break;
            else:
                draw_boards(player)
                print("\n  Das ist keine gültige Eingabe")
                continue

        except ValueError:
            draw_boards(player)
            print("\n  Das ist keine gültige Eingabe")
            continue
    return player_input


def update_boards(active_player, other_player, player_input):
    """Update the boards"""

    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    elif len(player_input) == 3:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    # Check opponent Board and update the boards accordingly
    if other_player["board"][y][x] == "0":
        active_player["guesses"][y][x] = "WG"
        other_player["board"][y][x] = "WG"
        # Show input result on the board and display Random Confirmation Message out of the predefine list
        draw_boards(active_player)
        print("\n  " + random.choice(miss_phrases))
        input("  Press Enter to Continue")

    # Check opponent Board and update the boards accordingly
    if other_player["board"][y][x] == "S":
        active_player["guesses"][y][x] = "CG"
        other_player["board"][y][x] = "HS"
        # Show input result on the board and display Random Confirmation Message out of the predefine list
        draw_boards(active_player)
        print("\n  " + random.choice(hit_phrases))
        input("  Press Enter to Continue")

    return [active_player, other_player]


# Prüft ob der Spieler gewonnen hat
def check_if_won(player_1_numer_of_ships,
                 player_2_numer_of_ships):  # , player_1_numer_of_ships, player_2_numer_of_ships):
    """ Function Checks if one player is out of Ships"""
    if player_1_numer_of_ships == 0 or player_2_numer_of_ships == 0:
        return True
    else:
        return False


# Fragt nach wie viele Schiffe man setzen will
def number_of_ships():
    while True:
        ships_num = int(input("  Wie viele Schiffe wollen Sie platzieren:"))
        if ships_num >= 3 and ships_num < 6:
            break
        else:
            print("  Sie müssen mindestens 3 und maximal 5 Schiffe platzieren:")
    return ships_num


# Gibt zurück wie viele Schiffe von jeder Größe (als dict)
def set_ship_distribution(number_of_ships):
    small_ship = 0  # 2 Felder groß
    medium_ship = 0  # 3 Felder groß
    big_ship = 0  # 4 Felder groß

    # Verteilung der Schiffe auf groß, klein und mittelgroß

    if number_of_ships == 3:
        small_ship = 1
        medium_ship = 1
        big_ship = 1

    elif number_of_ships == 4:
        small_ship = 2
        medium_ship = 1
        big_ship = 1

    elif number_of_ships == 5:
        small_ship = 2
        medium_ship = 2
        big_ship = 1

    shiffs_verteilung = {
        "smal": small_ship,
        "medium": medium_ship,
        "big": big_ship

    }
    return shiffs_verteilung


# Gibt die Zahl der Felder zurück, die ein Schiff hat
def ret_ship_len(key):
    if key == "smal":
        ret = 2
    elif key == "medium":
        ret = 3
    # "big"
    else:
        ret = 4

    return ret


# Diese Funktion gib die Anzahl aller 'S' in einer Liste
# Wichtig um die Zahl aller Schiffe einer Person auszugeben

def list_len(liste_mit_allen_schiffen):
    schiffe_gesamtzahl = 0

    for zeilen in range(len(liste_mit_allen_schiffen)):
        for spalten in range(len(liste_mit_allen_schiffen)):

            if liste_mit_allen_schiffen[zeilen][spalten] == "S":
                schiffe_gesamtzahl += 1

    return schiffe_gesamtzahl


# Prüft ob Eingabe ein Treffer im Feld vom Gegner ist
# Gibt aktuelle Zahl der aktiven gegnerischen Schiffe zurück
def check_if_hit(active_player_input, other_player, player_numer_of_ships):
    if len(active_player_input) == 2:
        # y = Buchstabe
        # x = Zahl

        y = ord(active_player_input[0]) - 65
        x = int(active_player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    elif len(active_player_input) == 3:
        y = ord(active_player_input[0]) - 65
        x = int(active_player_input[1:3]) - 1

        # Check opponent Board and update the boards accordingly
    if other_player["board"][y][x] == "0":
        pass

    # Check opponent Board and update the boards accordingly
    if other_player["board"][y][x] == "S" or other_player["board"][y][x] == "HS":
        return player_numer_of_ships - 1
    else:
        return player_numer_of_ships
