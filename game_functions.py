import random
import drawing_utils
import menu


def setup_new_board(board_size):
    """Sets up a new board matrix filled with 0s"""
    board = [["0" for i in range(board_size)] for j in range(board_size)]
    return board


def set_new_player(board_size, language, other_player_name=" "):
    """Creates a new Player with empty board and scores and asks for a name"""
    player = {}
    # Prevent completely empty name for legibility
    forbidden_names = ["", " ", "   ", "    ", "     ", "      ", "       ", "        ", "         ",
                       "          ", "           ", "            "]

    # If there is no named player yet, just asks for new name
    if other_player_name == " ":
        while True:
            player['name'] = str(input(f"  {language['name_first_player']}: "))
            if player['name'] not in forbidden_names and len(player['name']) < 13:
                break
            else:
                menu.clear_screen()
                print(f"  {language['name_player_error']}")
                continue

    # Else if a named player already exists, asks for new name and compares to other players name.
    # Only leaves input loop when the two names are different
    else:
        menu.clear_screen()
        while True:
            player['name'] = str(input(f"  {language['name_second_player']}: "))

            if player['name'] == other_player_name:
                menu.clear_screen()
                print(f"  {language['name_is_taken']}.")

            elif player['name'] not in forbidden_names and len(player['name']) < 13:
                break

            else:
                menu.clear_screen()
                print(f"  {language['name_player_error']}")

    # Set up a new empty personal board, new guesses board and empty list of tried fields
    player['board'] = setup_new_board(board_size)
    player['guesses'] = setup_new_board(board_size)
    player['already_tried'] = []

    return player


def set_ship_distribution(number_of_ships, language):
    """Sets the the amount of each ship typ"""
    # List of all possible ships, their size, name and symbol of the board
    patrol_boat1 = {'name': language['patrol_boat'], 'size': 2, 'symbol': "Pa1"}
    patrol_boat2 = {'name': language['patrol_boat'], 'size': 2, 'symbol': "Pa2"}
    patrol_boat3 = {'name': language['patrol_boat'], 'size': 2, 'symbol': "Pa3"}
    patrol_boat4 = {'name': language['patrol_boat'], 'size': 2, 'symbol': "Pa4"}
    submarine1 = {'name': language['submarine'], 'size': 3, 'symbol': "Su1"}
    submarine2 = {'name': language['submarine'], 'size': 3, 'symbol': "Su2"}
    destroyer = {'name': language['destroyer'], 'size': 3, 'symbol': "Des"}
    battleship1 = {'name': language['battleship'], 'size': 4, 'symbol': "Ba1"}
    battleship2 = {'name': language['battleship'], 'size': 4, 'symbol': "Ba2"}
    carrier = {'name': language['carrier'], 'size': 5, 'symbol': "Car"}

    # Create a list of the ships based on how many there are

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


def choose_ship_placement_methode(player, possible_input, ship_list, language):
    """Choice between randomly distributing the ships or deciding yourself"""
    menu.clear_screen()
    print(
        f"  {player['name']} {language['is_playing']}\n\n\n"
        f"   1. {language['place_ships_yourself']}\n"
        f"   2. {language['place_ships_randomly']}\n\n")

    while True:
        try:
            player_input = int(input(f"  {language['your_choice']}: "))

            # Player chooses ship placement
            if player_input == 1:
                menu.clear_screen()
                player = ship_placement(player, possible_input, ship_list, language)
                print("\n")
                break

            # Random placement of ships
            elif player_input == 2:
                menu.clear_screen()
                player = random_ship_placement(player, possible_input, ship_list, language)
                print("\n")
                break

            # Catch wrong input
            else:
                menu.clear_screen()
                print(f"  {player['name']} {language['is_playing']}\n\n\n"
                      f"   1. {language['place_ships_yourself']}\n"
                      f"   2. {language['place_ships_randomly']}")
                menu.invalid_input(language)

            # Catch wrong value input
        except ValueError:
            menu.clear_screen()
            print(f"  {player['name']} {language['is_playing']}\n\n\n"
                  f"   1. {language['place_ships_yourself']}\n"
                  f"   2. {language['place_ships_randomly']}")
            menu.invalid_input(language)
            continue
    return player


def ship_placement(player, possible_input, ship_list, language):
    """Decide where the ship are placed"""
    drawing_utils.draw_boards(player, language)
    print("\n")

    for ship in ship_list:
        while True:
            try:
                # Ask where the front of the ship should be placed
                input_ship_front = str(
                    input(
                        f"  {language['your']} {ship['name']} {language['is']} {ship['size']} {language['field_big_where_to_start']}? ")).upper()

                # Check if field exist
                if input_ship_front not in possible_input:
                    drawing_utils.draw_boards(player, language)
                    print(f"\n  {language['invalid_input']}")
                    continue

                # If the returned available space list is empty ask again
                available_spaces = check_space(input_ship_front, ship['size'], player)
                if available_spaces == []:
                    drawing_utils.draw_boards(player, language)
                    print(f"\n  {language['not_enough_space_for']} {ship['name']}")
                    continue

                # If available space list is not empty ask for placement of the back of the ship
                else:
                    # Create a list for printing out
                    placement_options_list = available_spaces[0]
                    for placement in range(1, len(available_spaces)):
                        placement_options_list = placement_options_list + ", " + available_spaces[placement]

                    # Ask for the placement of the back of the ship
                    drawing_utils.draw_boards(player, language)
                    input_ship_back = str(input(
                        f"\n\n  {language['the_front_is_on']} {input_ship_front}."
                        f" {language['where_to_put_the_back__your_choices']} {placement_options_list} : ")).upper()

                    # If the player input is in the list of available space, the boards can be updated
                    if input_ship_back in placement_options_list:
                        player = place_ship_down(player, ship, input_ship_front, input_ship_back)
                        drawing_utils.draw_boards(player, language)
                        print("\n")

                    # Else throw error message, go back and ask again
                    else:
                        drawing_utils.draw_boards(player, language)
                        print(f"\n  {language['invalid_input']}")
                        continue

                break

            except ValueError:
                drawing_utils.draw_boards(player, language)
                print(f"\n  {language['invalid_input']}")
                continue

    # Show the end position of all ships before continuing
    drawing_utils.draw_boards(player, language)
    print("\n")
    input(f"  {language['press_enter_to_continue']}")
    return player


def random_ship_placement(player, possible_input, ship_list, language):
    """Randomly distribute the ships on the board"""
    for ship in ship_list:
        while True:
            try:
                # Choose a random place on the board and check if enough space is available
                input_ship_front = random.choice(possible_input)
                available_spaces = check_space(input_ship_front, ship["size"], player)
                # If not restart the loop
                if available_spaces == []:
                    continue

                # If space is available choose randomly one of the possible positions of the list
                else:
                    input_ship_back = random.choice(available_spaces)
                    if input_ship_back in available_spaces:
                        player = place_ship_down(player, ship, input_ship_front, input_ship_back)
                        print("\n")
                break

            except ValueError:
                drawing_utils.draw_boards(player, language)
                print(f"\n  {language['invalid_input']}")
                continue

    # Show end result before continuing
    drawing_utils.draw_boards(player, language)
    print("\n")
    input(f"  {language['press_enter_to_continue']}")
    return player


def check_space(player_input, ship_size, player):
    """checks if the chosen field would allow the ship to be placed"""
    # Start with an empty list for the available space
    available_placement = []

    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    else:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    # Check if starting space is empty, if not return the empty list for available spaces
    if player['board'][y][x] != "0":
        return available_placement

    check = False
    # Check Above
    for i in range(1, ship_size):
        # It goes through all spaces above until it reaches the size of the ship, or finds a field that isn't empty
        if y + 1 - i != 0 and player['board'][y - i][x] == "0":
            check = True

        else:
            # If it finds a field that isn't empty, it stops the loop and give false as a result for the check
            check = False
            break

    # If the the check went through successfully it adds the field above to the available list
    if check is True:
        acceptable_field = chr(y + 65 - ship_size + 1) + str(x + 1)
        available_placement.append(acceptable_field)

    # Check below. Same as above
    check = False
    for i in range(1, ship_size):
        if y - 1 + i != len(player['board']) - 1 and player['board'][y + i][x] == "0":
            check = True

        else:
            check = False
            break

    if check is True:
        acceptable_field = chr(y + 65 + ship_size - 1) + str(x + 1)
        available_placement.append(acceptable_field)

    # Check left. Same as above
    check = False
    for i in range(1, ship_size):
        if x + 1 - i != 0 and player['board'][y][x - i] == "0":
            check = True

        else:
            check = False
            break

    if check is True:
        acceptable_field = chr(y + 65) + str(x + 1 - ship_size + 1)
        available_placement.append(acceptable_field)

    # Check Right. Same as above
    check = False
    for i in range(1, ship_size):
        if x - 1 + i != len(player['board']) - 1 and player['board'][y][x + i] == "0":
            check = True

        else:
            check = False
            break

    if check is True:
        acceptable_field = chr(y + 65) + str(x + 1 + ship_size - 1)
        available_placement.append(acceptable_field)

    return available_placement


def place_ship_down(player, ship, input_ship_front, input_ship_back):
    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(input_ship_front) == 2:
        front_y = ord(input_ship_front[0]) - 65
        front_x = int(input_ship_front[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    else:
        front_y = ord(input_ship_front[0]) - 65
        front_x = int(input_ship_front[1:3]) - 1

    if len(input_ship_back) == 2:
        back_y = ord(input_ship_back[0]) - 65
        back_x = int(input_ship_back[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    else:
        back_y = ord(input_ship_back[0]) - 65
        back_x = int(input_ship_back[1:3]) - 1

    # Checks if the ship is positioned horizontally and places the ship down
    if front_y == back_y:
        if front_x > back_x:
            for i in range(front_x - back_x + 1):
                player['board'][front_y][back_x + i] = ship['symbol']

        elif front_x < back_x:
            for i in range(back_x - front_x + 1):
                player['board'][front_y][front_x + i] = ship['symbol']

    # Checks if the ship is positioned vertically and places the ship down
    elif front_y != back_y:
        if front_y > back_y:
            for i in range(front_y - back_y + 1):
                player['board'][back_y + i][back_x] = ship['symbol']

        elif front_y < back_y:
            for i in range(back_y - front_y + 1):
                player['board'][front_y + i][back_x] = ship['symbol']

    return player


def ask_input_from(player, possible_input, language):
    """Ask for player input and checks against list of possible inputs and already tried"""
    drawing_utils.draw_boards(player, language)
    print("\n")
    while True:
        try:
            player_input = str(input(f"  {language['what_is_your_next_play']}: ")).upper()
            if player_input == "EXIT":
                break
            if player_input in possible_input:
                if player_input in player['already_tried']:
                    drawing_utils.draw_boards(player, language)
                    print(f"\n  {language['you_ve_already_shot_there']}.")
                    continue
                else:
                    player['already_tried'].append(player_input)
                    break
            else:
                drawing_utils.draw_boards(player, language)
                print(f"\n  {language['invalid_input']}")
                continue

        except ValueError:
            drawing_utils.draw_boards(player, language)
            print(f"\n  {language['invalid_input']}")
            continue
    return player_input


import _thread

flag = False


def countdown():
    when_to_stop = 15
    while when_to_stop > 0:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print("\rDeine Zeit: " + time_left, end="")

        time.sleep(1)
        when_to_stop -= 1

        if when_to_stop == 0:
            global flag
            flag = True


def test(board_size):
    _thread.start_new_thread(countdown(), 1)
    _thread.start_new_thread(ask_input_from(), 1)

    if flag == True:
        return random_ship_attac(board_size)


def switch_player(active_player, player_1, player_2, language):
    """Switches active player and waits for confirmation that only active player is looking"""
    menu.clear_screen()
    if active_player == player_1:
        active_player = player_2
        print(
            f"  {player_2['name']} {language['is_playing']}.\n"
            f"  {language['switch_places_and_press_enter_when']} {player_1['name']} {language['is_not_looking']}")
    else:
        active_player = player_1
        print(
            f"  {player_1['name']} {language['is_playing']}.\n"
            f"  {language['switch_places_and_press_enter_when']} {player_2['name']} {language['is_not_looking']}")
    input()
    menu.clear_screen()
    return active_player


def update_boards(active_player, other_player, player_input, language):
    """Update the boards"""

    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    else:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    # Check opponent Board and update the boards accordingly
    if other_player['board'][y][x] == "0":
        active_player['guesses'][y][x] = "WG"
        other_player['board'][y][x] = "WG"
        # Show input result on the board and display Random Confirmation Message out of the predefine list
        drawing_utils.draw_boards(active_player, language)
        print("\n  " + random.choice(language['miss_phrases']))
        input("  Press Enter to Continue")

    # If it hit, gets the name of the target, checks if the ship was destroyed and update the boards accordingly
    else:
        # Get the symbol of the last target to know the name of the ship
        last_target = other_player['board'][y][x]
        if "Pa" in last_target:
            last_target_name = language['patrol_boat']
        elif "Su" in last_target:
            last_target_name = language['submarine']
        elif "De" in last_target:
            last_target_name = language['destroyer']
        elif "Ba" in last_target:
            last_target_name = language['battleship']
        elif "Ca" in last_target:
            last_target_name = language['carrier']

        # Adds the field as a correct guess to the active player and append _hit to the field on the opponents board
        active_player['guesses'][y][x] = "CG"
        other_player['board'][y][x] += "_Hit"

        # Show input result on the board and display Random Confirmation Message out of the predefine list
        # Also check if any part of the ship is still alive
        if any(last_target in row for row in other_player['board']):
            drawing_utils.draw_boards(active_player, language)
            print("\n  " + random.choice(language['hit_phrases']), end=". ")
            print(f"  {language['you_ve_hit_an_enemy']}")
        # If no part of the ship is left it reduces the numbre of ship of the enemy by one
        else:
            other_player['ships_left'] -= 1
            active_player['enemy_ships_left'] -= 1
            drawing_utils.draw_boards(active_player, language)
            print("\n  " + random.choice(language['hit_phrases']), end=". ")
            print(f"  {language['you_ve_destroyed']} {last_target_name} {language['sunk']}!")

        input(f"  {language['press_enter_to_continue']}")

    return [active_player, other_player]


def check_if_won(player_1, player_2):
    """ Function Checks if one player is out of Ships"""
    if player_1['ships_left'] == 0 or player_2['ships_left'] == 0:
        return True
    else:
        return False
