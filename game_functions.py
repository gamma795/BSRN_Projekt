import time
import zufallsGenerator
import drawing_utils
import menu
import random

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

    # If there is no named player yet, just asks for new name
    if other_player_name == " ":
        while True:
            player["name"] = str(input("  Wie soll der erste Spieler heißen: "))
            if player["name"] not in ["", " ", "   ", "    ", "     ", "      ", "       ", "        ", "         ",
                                      "          ", "           ", "            "] and len(player["name"]) < 13:
                break
            else:
                menu.clear_screen()
                print("  Der Name darf nicht Leer sein, und darf max 12 Zeichen haben")
                continue

    # Else if a named player already exists, asks for new name and compares to other players name. Only leaves input loop when the two names are different
    else:
        menu.clear_screen()
        while True:
            player["name"] = str(input("  Wie soll der zweite Spieler heißen: "))

            if player["name"] == other_player_name:
                menu.clear_screen()
                print("  Dieser Name ist schon belegt. Wählen Sie einen anderen Namen.")

            elif player["name"] not in ["", " ", "   ", "    ", "     ", "      ", "       ", "        ", "         ",
                                        "          ", "           ", "            "] and len(player["name"]) < 13:
                break

            else:
                menu.clear_screen()
                print("  Der Name darf nicht Leer sein, und darf max 12 Zeichen haben")

    # Set up a new Empty personnal board, new guesses board and empty list of tried fields
    player["board"] = setup_new_board(board_size)
    player["guesses"] = setup_new_board(board_size)
    player["already_tried"] = []

    return player


# Gibt zurück wie viele Schiffe von jeder Größe (als dict)
def set_ship_distribution(number_of_ships):
    patrol_boat1 = {"name": "Patrouillenboot", "size": 2, "symbol": "Pa1"}  # 2 Felder groß
    patrol_boat2 = {"name": "Patrouillenboot", "size": 2, "symbol": "Pa2"}
    patrol_boat3 = {"name": "Patrouillenboot", "size": 2, "symbol": "Pa3"}
    patrol_boat4 = {"name": "Patrouillenboot", "size": 2, "symbol": "Pa4"}
    submarine1 = {"name": "U-Boot", "size": 3, "symbol": "Su1"}  # 3 Felder groß
    submarine2 = {"name": "U-Boot", "size": 3, "symbol": "Su2"}
    destroyer = {"name": "Zerstörer", "size": 3, "symbol": "Des"}  # 3 Felder groß
    battleship1 = {"name": "Schlachtschiff", "size": 4, "symbol": "Ba1"}  # 4 Felder groß
    battleship2 = {"name": "Schlachtschiff", "size": 4, "symbol": "Ba2"}
    carrier = {"name": "Flugzeugträger", "size": 5, "symbol": "Car"}  # 5 Felder groß

    # Verteilung der Schiffe

    if number_of_ships == 3:
        ship_list = [battleship1, submarine1, patrol_boat1]

    elif number_of_ships == 4:
        ship_list = [battleship1, destroyer, submarine1, patrol_boat1]

    elif number_of_ships == 5:
        ship_list = [carrier, battleship1, destroyer, submarine1, patrol_boat1]

    elif number_of_ships == 6:
        ship_list = [carrier, battleship1, destroyer, submarine1, patrol_boat1, patrol_boat2]

    elif number_of_ships == 7:
        ship_list = [carrier, battleship1, destroyer, submarine1, submarine2, patrol_boat1, patrol_boat2]

    elif number_of_ships == 8:
        ship_list = [carrier, battleship1, destroyer, submarine1, submarine2, patrol_boat1, patrol_boat2, patrol_boat3]

    elif number_of_ships == 9:
        ship_list = [carrier, battleship1, battleship2, destroyer, submarine1, submarine2, patrol_boat1, patrol_boat2,
                     patrol_boat3]

    elif number_of_ships == 10:
        ship_list = [carrier, battleship1, battleship2, destroyer, submarine1, submarine2, patrol_boat1, patrol_boat2,
                     patrol_boat3, patrol_boat4]

    return ship_list


def choose_ship_placement_methode(player, possible_input, ship_list):
    """Choice between randomly distributing the ships or deciding yourself"""
    menu.clear_screen()
    print(
        f'  {player["name"]} ist dran.\n\n')
    print("   1. Schiffe selber platzieren\n   2. Schiffe zufällig auf dem Feld verteilen\n\n")

    while True:
        try:
            player_input = int(input("  Ihre Wahl: "))

            # Player chooses ship placement
            if player_input == 1:
                menu.clear_screen()

                player = ship_placement(player, possible_input, ship_list)
                print("\n")
                break

            # Random placement of ships
            elif player_input == 2:
                menu.clear_screen()
                player = random_ship_placement(player, possible_input, ship_list)
                print("\n")
                break

            # Catch wrong input
            else:
                menu.clear_screen()
                print(
                    f'  {player["name"]} ist dran.\n\n')
                print("   1. Schiffe selber platzieren\n   2. Schiffe zufällig auf dem Feld verteilen")
                menu.invalid_input()

            # Catch wrong value input
        except ValueError:
            menu.clear_screen()
            print(
                f'  {player["name"]} ist dran.\n\n')
            print("   1. Schiffe selber platzieren\n   2. Schiffe zufällig auf dem Feld verteilen")
            menu.invalid_input()
            continue
    return player


def ship_placement(player, possible_input, ship_list):
    """Decide where the ship are placed"""
    drawing_utils.draw_boards(player)
    print("\n")
    occupied_fields = []

    for ship in ship_list:
        while True:
            try:
                input_ship_front = str(
                    input(f"  Dein {ship['name']} ist {ship['size']} Felder groß. Wo soll die Spitze liegen? ")).upper()

                if input_ship_front not in possible_input:
                    drawing_utils.draw_boards(player)
                    print("\n  Das ist keine gültige Eingabe")
                    continue

                available_spaces = check_space(input_ship_front, ship["size"], player)
                if available_spaces == []:
                    drawing_utils.draw_boards(player)
                    print(f"\n  An dieser Stelle ist nicht genug Platz für dein {ship['name']}")
                    continue

                else:
                    placement_options = available_spaces[0]
                    for placement in range(1, len(available_spaces)):
                        placement_options = placement_options + ", " + available_spaces[placement]

                    drawing_utils.draw_boards(player)
                    input_ship_back = str(input(
                        f"\n\n  Die Spitze ist bei {input_ship_front}. Wo soll das Ende des Schiffes liegen? Möglichkeiten sind {placement_options} : ")).upper()

                    if input_ship_back in placement_options:
                        player = place_ship_down(player, ship, input_ship_front, input_ship_back)
                        drawing_utils.draw_boards(player)
                        print("\n")
                    else:
                        drawing_utils.draw_boards(player)
                        print("\n  Das ist keine gültige Eingabe")
                        continue

                break;

            except ValueError:
                drawing_utils.draw_boards(player)
                print("\n  Das ist keine gültige Eingabe")
                continue

    drawing_utils.draw_boards(player)
    print("\n")
    input("  Press Enter to continue")
    return player


def random_ship_placement(player, possible_input, ship_list):
    """Randomly distribute the ships on the board"""
    for ship in ship_list:
        while True:
            try:
                input_ship_front = random.choice(possible_input)
                available_spaces = check_space(input_ship_front, ship["size"], player)
                if available_spaces == []:
                    continue

                else:
                    input_ship_back = random.choice(available_spaces)
                    if input_ship_back in available_spaces:
                        player = place_ship_down(player, ship, input_ship_front, input_ship_back)
                        print("\n")
                break;

            except ValueError:
                drawing_utils.draw_boards(player)
                print("\n  Das ist keine gültige Eingabe")
                continue

    drawing_utils.draw_boards(player)
    print("\n")
    input("  Press Enter to continue")
    return player


def check_space(player_input, ship_size, player):
    """checks if the chosen field would allow the ship to be placed"""
    available_placement = []

    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    elif len(player_input) == 3:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    if player["board"][y][x] != "0":
        return available_placement

    check = False
    # Check Above
    for i in range(1, ship_size):
        if y + 1 - i != 0 and player["board"][y - i][x] == "0":
            check = True

        else:
            check = False
            break

    if check == True:
        acceptable_field = chr(y + 65 - ship_size + 1) + str(x + 1)
        available_placement.append(acceptable_field)

    # Check below
    check = False
    for i in range(1, ship_size):
        if y - 1 + i != len(player["board"]) - 1 and player["board"][y + i][x] == "0":
            check = True

        else:
            check = False
            break

    if check == True:
        acceptable_field = chr(y + 65 + ship_size - 1) + str(x + 1)
        available_placement.append(acceptable_field)

    # Check left
    check = False
    for i in range(1, ship_size):
        if x + 1 - i != 0 and player["board"][y][x - i] == "0":
            check = True

        else:
            check = False
            break

    if check == True:
        acceptable_field = chr(y + 65) + str(x + 1 - ship_size + 1)
        available_placement.append(acceptable_field)

    # Check Right
    check = False
    for i in range(1, ship_size):
        if x - 1 + i != len(player["board"]) - 1 and player["board"][y][x + i] == "0":
            check = True

        else:
            check = False
            break

    if check == True:
        acceptable_field = chr(y + 65) + str(x + 1 + ship_size - 1)
        available_placement.append(acceptable_field)

    return available_placement


def place_ship_down(player, ship, input_ship_front, input_ship_back):
    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(input_ship_front) == 2:
        front_y = ord(input_ship_front[0]) - 65
        front_x = int(input_ship_front[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    elif len(input_ship_front) == 3:
        front_y = ord(input_ship_front[0]) - 65
        front_x = int(input_ship_front[1:3]) - 1

    if len(input_ship_back) == 2:
        back_y = ord(input_ship_back[0]) - 65
        back_x = int(input_ship_back[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    elif len(input_ship_back) == 3:
        back_y = ord(input_ship_back[0]) - 65
        back_x = int(input_ship_back[1:3]) - 1

    # Checks if the ship is positioned horizontaly and places the ship down
    if front_y == back_y:
        if front_x > back_x:
            for i in range(front_x - back_x + 1):
                player["board"][front_y][back_x + i] = ship["symbol"]

        elif front_x < back_x:
            for i in range(back_x - front_x + 1):
                player["board"][front_y][front_x + i] = ship["symbol"]

    # Checks if the ship is positioned verticaly and places the ship down
    elif front_y != back_y:
        if front_y > back_y:
            for i in range(front_y - back_y + 1):
                player["board"][back_y + i][back_x] = ship["symbol"]

        elif front_y < back_y:
            for i in range(back_y - front_y + 1):
                player["board"][front_y + i][back_x] = ship["symbol"]

    return player


# Player input to attack
def ask_input_from(player, possible_input, board_size):
    """Ask for player input and checks against list of possible inputs and already tried"""
    drawing_utils.draw_boards(player)
    print("\n")
    when_to_stop = 15

    while when_to_stop > 0:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print(time_left + "\r", end="")
        time.sleep(1)
        when_to_stop -= 1

        try:
            player_input = str(input("  Was ist Ihr nächster Zug: ")).upper()
            if player_input == "EXIT":
                break
                if player_input not in possible_input:
                    drawing_utils.draw_boards(player)
                    print("\n  Das ist keine gültige Eingabe")
                    continue
                else:
                    if player_input in player["already_tried"]:
                        drawing_utils.draw_boards(player)
                        print("\n  Sie haben schon auf dieses Feld geschossen.")
                        continue
                    else:
                        player["already_tried"].append(player_input)
                        break

        except ValueError:
            drawing_utils.draw_boards(player)
            print("\n  Das ist keine gültige Eingabe")
            continue
       return player_input
   else:
    return zufallsGenerator.random_ship_attac(board_size)

def switch_player(active_player, player_1, player_2):
    """Switches active player and waits for confirmation that only active player is lookig"""
    menu.clear_screen()
    if active_player == player_1:
        active_player = player_2
        print(
            f'  Jetzt ist {player_2["name"]} dran.\n  Tauschen Sie die Plätze und drücken Sie Enter wenn {player_1["name"]} nicht mehr schaut')
    else:
        active_player = player_1
        print(
            f'  Jetzt ist {player_1["name"]} dran.\n  Tauschen Sie die Plätze und drücken Sie Enter wenn {player_2["name"]} nicht mehr schaut')
    input()
    menu.clear_screen()
    return active_player


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
        drawing_utils.draw_boards(active_player)
        print("\n  " + random.choice(miss_phrases))
        input("  Press Enter to Continue")

    # Check opponent Board and update the boards accordingly
    else:
        last_target = other_player["board"][y][x]
        if "Pa" in last_target:
            last_target_name = "Patrouillenboot"
        elif "Su" in last_target:
            last_target_name = "U-Boot"
        elif "De" in last_target:
            last_target_name = "Zerstörer"
        elif "Ba" in last_target:
            last_target_name = "Schlachtschiff"
        elif "Ca" in last_target:
            last_target_name = "Flugzeugträger"

        active_player["guesses"][y][x] = "CG"
        other_player["board"][y][x] += "_Hit"
        # Show input result on the board and display Random Confirmation Message out of the predefine list

        if any(last_target in row for row in other_player["board"]):
            drawing_utils.draw_boards(active_player)
            print("\n  " + random.choice(hit_phrases), end=". ")
            # print(f"Sie haben das gegnerische {last_target_name} getroffen!")    # Alternative if Ship typ is to be named
            print(f"Sie haben ein gegnerisches Schiffe getroffen!")
        else:
            other_player["ships_left"] -= 1
            active_player["enemy_ships_left"] -= 1
            drawing_utils.draw_boards(active_player)
            print("\n  " + random.choice(hit_phrases), end=". ")
            print(f"Sie haben das gegnerische {last_target_name} versenkt!")

        input("  Press Enter to Continue")

    return [active_player, other_player]


# Prüft ob der Spieler gewonnen hat
def check_if_won(player_1, player_2):
    """ Function Checks if one player is out of Ships"""
    if player_1["ships_left"] == 0 or player_2["ships_left"] == 0:
        return True
    else:
        return False
