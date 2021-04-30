# Setting up the Board
import settings


def setup_new_board(board_size):
    """Sets up a new board matrix filled with 0s"""
    row = ["0"] * board_size
    board = [row] * board_size
    return board


def set_new_player(board_size, other_player_name=" "):
    player = {}
    if other_player_name == " ":
        player["name"] = str(input("Wie soll der erste Spieler heißen: "))
    else:
        while True:
            player["name"] = str(input("Wie soll der zweite Spieler heißen: "))
            if player["name"] == other_player_name:
                print("Dieser Name ist schon belegt. Wählen Sie einen anderen Namen.")
                continue
            else:
                break;
    player["board"] = setup_new_board(board_size)
    player["guesses"] = setup_new_board(board_size)
    player["already_tried"] = []
    return player


def field_filling(value):
    """Sets how the Board position will be displayed"""
    if value == "0":  # empty field
        return "   "
    elif value == "S":  # ship
        return "███"
    elif value == "HS":  # hit ship
        return "▒X▒"
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

    # Spacing between the two boards
    board_spacing = "            "
    header_1_spacing = " " * (len(player["board"][0]) * 4 - len(header_1))

    # Header
    settings.clear_screen()
    print(f'{player["name"]} ist dran:')
    print(f"\n      {header_1}{header_1_spacing}{board_spacing}       {header_2}\n")
    print("      ", end=v)
    for x in range(len(player["board"][0])):
        if x < 9:
            print(f" {x + 1} ", end=v)
        else:
            print(f" {x + 1}", end=v)

    print(board_spacing + "      ", end=v)  # opponent side
    for x in range(len(player["guesses"][0])):
        if x < 9:
            print(f" {x + 1} ", end=v)
        else:
            print(f" {x + 1}", end=v)

    print("\n      ", end=v)
    for x in range(len(player["board"][0])):
        print(f"   ", end=v)

    print(board_spacing + "      ", end=v)  # opponent side
    for x in range(len(player["guesses"][0])):
        print(f"   ", end=v)

    print("\n" + h * 6, end=c)
    for x in range(len(player["board"][0])):
        print(h * 3, end=c)

    print(board_spacing + h * 6, end=c)  # opponent side
    for x in range(len(player["guesses"][0])):
        print(h * 3, end=c)

    # Field

    for y in range(len(player["board"])):
        print(f"\n {chr(65 + y)}    ", end=v)
        for x in range(len(player["board"][0])):
            field = field_filling(player["board"][y][x])
            print(field, end=v)

        print(f"{board_spacing} {chr(65 + y)}    ", end=v)  # opponent side
        for x in range(len(player["guesses"])):
            field = field_filling(player["guesses"][y][x])
            print(field, end=v)

        print("\n" + h * 6, end=c)
        for x in range(len(player["board"][0])):
            print(h * 3, end=c)

        print(board_spacing + h * 6, end=c)  # opponent side
        for x in range(len(player["guesses"][0])):
            print(h * 3, end=c)
    print("")


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
    """ Wait for player Switch"""
    settings.clear_screen()
    if active_player == player_1:
        active_player = player_2
        print(
            f'Jetzt ist {player_2["name"]} dran.\nTauschen Sie die Plätze und drücken Sie Enter wenn {player_1["name"]} nicht mehr schaut')
    else:
        active_player = player_1
        print(
            f'Jetzt ist {player_1["name"]} dran.\nTauschen Sie die Plätze und drücken Sie Enter wenn {player_2["name"]} nicht mehr schaut')
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
            player_input = str(input("Was ist hier nächster Zug:")).upper()
            print(player_input)
            if player_input in possible_input:
                if player_input in player["already_tried"]:
                    draw_boards(player)
                    print("\nSie haben schon auf dieses Feld geschossen.")
                    continue
                else:
                    player["already_tried"].append(player_input)
                    print(player["already_tried"])
                    break;
            else:
                draw_boards(player)
                print("\nDas ist keine gültige Eingabe")
                continue

        except ValueError:
            draw_boards(player)
            print("\nDas ist keine gültige Eingabe")
            continue
    return player_input


def update_boards(active_player, other_player, player_input):
    """Update the boards"""
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    elif len(player_input) == 3:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    print(active_player["guesses"])
    active_player["guesses"][y][x] = "WG"
    print(active_player["guesses"])
    other_player["board"][y][x] = "WG"
    print(other_player["board"])

    return [active_player, other_player]
