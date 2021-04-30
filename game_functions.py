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


# Player input
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


def check_if_won(player_1, player_2):
    """ Function Checks if one player is out of Ships"""
    if any('S' in row for row in player_1["board"]) and any('S' in row for row in player_2["board"]):
        return False
    else:
        return True
