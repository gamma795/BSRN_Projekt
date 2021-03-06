import random
import drawing_utils
import menu
import counterFileNeu


def setup_new_board(board_size):
    """Sets up a new board matrix filled with 0s"""
    board = [["0" for _ in range(board_size)] for _ in range(board_size)]
    return board


def set_new_player(settings_values, language, possible_input, other_player_name=" "):
    """Creates a new Player with empty board and scores and asks for a name"""

    player = {}
    # Prevent completely empty name for legibility
    forbidden_names = ["", " ", "   ", "    ", "     ", "      ", "       ", "        ", "         ",
                       "          ", "           ", "            "]

    # If there is no named player yet or the other player is a bot, just asks for new name
    if other_player_name == "bot":
        while True:
            player['name'] = str(input(f"  {language['name_human_player']}: "))
            if player['name'] not in forbidden_names and len(player['name']) < 13:
                break
            else:
                menu.clear_screen()
                print(f"  {language['name_player_error']}")
                continue

    elif other_player_name == " ":
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

    # Set up a new empty personal board, new guesses board and a list of all he fields that have not been tried yet
    # And save how many ships both player have

    player['board'] = setup_new_board(settings_values['board_size'])
    player['guesses'] = setup_new_board(settings_values['board_size'])
    player['ships_left'] = settings_values['number_of_ships']
    player['enemy_ships_left'] = settings_values['number_of_ships']
    player['not_yet_tried'] = []
    player['not_yet_tried'].extend(possible_input)

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

    print("\n")

    print(
        f"  {player['name']}, {language['you_are_playing']}\n\n\n"
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
                print(f"  {player['name']}, {language['you_are_playing']}\n\n\n"
                      f"   1. {language['place_ships_yourself']}\n"
                      f"   2. {language['place_ships_randomly']}")
                menu.invalid_input(language)

            # Catch wrong value input
        except ValueError:
            menu.clear_screen()
            print(f"  {player['name']}, {language['you_are_playing']}\n\n\n"
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
                        f"  {language['your']} {ship['name']} {language['is']} {ship['size']} "
                        f"{language['field_big_where_to_start']}? ")).upper()

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
    if 'Bot' not in player['name']:
        drawing_utils.draw_boards(player, language)
        print("\n")
        input(f"  {language['press_enter_to_continue']}")
    return player


def input_to_coordinates(player_input):
    # Convert player input into two int x and y to check the boards at specific place (case with number 9 or lower)
    if len(player_input) == 2:
        y = ord(player_input[0]) - 65
        x = int(player_input[1]) - 1

    # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
    else:
        y = ord(player_input[0]) - 65
        x = int(player_input[1:3]) - 1

    return x, y


def check_space(player_input, ship_size, player, bot_shot=False):
    """checks if the chosen field would allow the ship to be placed"""
    # Start with an empty list for the available space
    available_placement = []

    x, y = input_to_coordinates(player_input)

    # Check if starting space is empty, if not return the empty list for available spaces
    if player['board'][y][x] != "0" and not bot_shot:
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


def ask_input_from(player, possible_input, language, settings_values):
    """Ask for player input and checks against list of possible inputs and already tried"""
    drawing_utils.draw_boards(player, language)
    print("\n")
    while True:

        try:
            if settings_values['countdown_on']:
                player_input = counterFileNeu.main(player, language)

            else:
                player_input = str(input(f"  {language['what_is_your_next_play']}: ")).upper()

            if player_input == "EXIT":
                return player_input
            if player_input in possible_input:
                if player_input not in player['not_yet_tried']:
                    drawing_utils.draw_boards(player, language)
                    print(f"\n  {language['you_ve_already_shot_there']}.")
                    continue
                else:
                    player['not_yet_tried'].remove(player_input)
                    return player_input
            else:
                drawing_utils.draw_boards(player, language)
                print(f"\n  {language['invalid_input']}")
                continue

        except ValueError:
            drawing_utils.draw_boards(player, language)
            print(f"\n  {language['invalid_input']}")
            continue


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
    if "Bot" in active_player['name']:
        bot_turn = True
    else:
        bot_turn = False

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
        last_target = "water"
        active_player['guesses'][y][x] = "WG"
        other_player['board'][y][x] = "WG"

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
    # If pvp game
    if not bot_turn:
        if last_target == "water":
            drawing_utils.draw_boards(active_player, language)
            print("\n  " + random.choice(language['miss_phrases']))

        elif any(last_target in row for row in other_player['board']):
            drawing_utils.draw_boards(active_player, language)
            print(f"\n  {random.choice(language['hit_phrases'])}. {language['you_ve_hit_an_enemy']}")

        # If no part of the ship is left it reduces the number of ship of the enemy by one
        else:
            other_player['ships_left'] -= 1
            active_player['enemy_ships_left'] -= 1

            drawing_utils.draw_boards(active_player, language)
            print(f"\n  {random.choice(language['hit_phrases'])}. "
                  f"{language['you_ve_destroyed']} {last_target_name} {language['sunk']}!")

    # If pve game
    else:
        if last_target == "water":
            drawing_utils.draw_boards(other_player, language)
            print(f"\n  {active_player['name']} {language['shot_into_water']} {player_input}")

        elif any(last_target in row for row in other_player['board']):
            drawing_utils.draw_boards(other_player, language)
            print(f"\n  {active_player['name']} {language['hit_your']} {last_target_name} {language['hit_your_2']}")
            active_player['current_target'].append(player_input)

        # If no part of the ship is left it reduces the number of ship of the enemy by one
        else:
            other_player['ships_left'] -= 1
            active_player['enemy_ships_left'] -= 1
            for x in active_player['current_target']:
                if x in active_player['possible_target']:
                    active_player['possible_target'].remove(x)
            active_player['current_target'] = []

            drawing_utils.draw_boards(other_player, language)
            print(f"\n  {active_player['name']} {language['destroyed_your']} {last_target_name} {language['sunk']}")

    input(f"  {language['press_enter_to_continue']}")

    return [active_player, other_player]


def check_if_won(player_1, player_2):
    """ Function Checks if one player is out of Ships"""
    if player_1['ships_left'] == 0 or player_2['ships_left'] == 0:
        return True
    else:
        return False


def bot_player_input(bot):
    """Choose Bot input based on its level"""
    while True:
        try:
            # Level easy: bot shots completely at random
            if bot['level'] == "easy":
                return random.choice(bot['not_yet_tried'])

            # Level normal: bot shoots at random until it hits, then hunts close to hit
            else:
                next_shot = []
                # If there is no alive target in last_shot but there are still alive ships that where hit
                # Bot chooses randomly one of the list as the next target to seek
                if bot['current_target'] == [] and bot['possible_target'] != []:
                    bot['current_target'].append(random.choice(bot['possible_target']))

                # If there was no recent hit without sinking a ship, bot shoots at random
                if bot['current_target'] == []:
                    if bot['level'] == "normal":
                        return random.choice(bot['not_yet_tried'])
                    else:
                        return smart_random_shot(bot)

                # If there was only one recent hit, Bot checks if adjacent fields are empty
                # Empty fields are added to the next_shot list
                elif len(bot['current_target']) == 1:
                    x, y = input_to_coordinates(bot['current_target'][0])
                    if x != 0 and bot['guesses'][y][x - 1] == "0":
                        acceptable_field = chr(y + 65) + str(x + 1 - 1)
                        next_shot.append(acceptable_field)

                    if x < len(bot['guesses']) - 1 and bot['guesses'][y][x + 1] == "0":
                        acceptable_field = chr(y + 65) + str(x + 1 + 1)
                        next_shot.append(acceptable_field)

                    if y != 0 and bot['guesses'][y - 1][x] == "0":
                        acceptable_field = chr(y + 65 - 1) + str(x + 1)
                        next_shot.append(acceptable_field)

                    if y < len(bot['guesses']) - 1 and bot['guesses'][y + 1][x] == "0":
                        acceptable_field = chr(y + 65 + 1) + str(x + 1)
                        next_shot.append(acceptable_field)

                # If there was more than one recent hit, the Bot looks at both end of the hit chain
                else:
                    # Transform hit list into two lists of coordinates
                    x_coordinates = []
                    y_coordinates = []

                    for i in range(len(bot['current_target'])):
                        a, b = input_to_coordinates(bot['current_target'][i])
                        x_coordinates.append(a)
                        y_coordinates.append(b)

                    # If the y coordinates are the same, ship is likely placed horizontally
                    if y_coordinates[0] == y_coordinates[1]:
                        # Checks left and right of hit chain
                        for x_value in x_coordinates:
                            if x_value != 0 and bot['guesses'][y_coordinates[0]][x_value - 1] == "0":
                                acceptable_field = chr(y_coordinates[0] + 65) + str(x_value + 1 - 1)
                                next_shot.append(acceptable_field)

                            if x_value != len(bot['guesses'][0]) - 1 \
                                    and bot['guesses'][y_coordinates[0]][x_value + 1] == "0":
                                acceptable_field = chr(y_coordinates[0] + 65) + str(x_value + 1 + 1)
                                next_shot.append(acceptable_field)

                    # If the y coordinates are the same, ship is likely placed vertically
                    else:
                        # Checks above and below hit chain
                        for y_value in y_coordinates:
                            if y_value != 0 and bot['guesses'][y_value - 1][x_coordinates[0]] == "0":
                                acceptable_field = chr(y_value - 1 + 65) + str(x_coordinates[0] + 1)
                                next_shot.append(acceptable_field)

                            if y_value != len(bot['guesses']) - 1 \
                                    and bot['guesses'][y_value + 1][x_coordinates[0]] == "0":
                                acceptable_field = chr(y_value + 1 + 65) + str(x_coordinates[0] + 1)
                                next_shot.append(acceptable_field)

                print(f"  Current Target: {bot['current_target']}")  # To catch errors
                print(f"  Possible shot found : {next_shot}")
                if next_shot != []:
                    return random.choice(next_shot)

                # If the next_shot list comes out empty while the current target is still alive, Bot can assume that
                # each part of the target belong to a different ship and takes one randomly as next Target
                else:
                    for field in bot['current_target']:
                        bot['possible_target'].append(field)
                bot['current_target'] = []
                bot['current_target'].append(random.choice(bot['possible_target']))
                continue

            # Level Hard: to be implemented

        except ValueError:
            continue


def smart_random_shot(bot):
    """Check what the smallest player ship is and looks for the ideal hunting grid accordingly"""

    # If the smallest ship is 2 field long there are only 2 possible hunting grid
    if 2 in bot['enemy_ship_sizes']:
        hunting_grid_00 = []
        hunting_grid_01 = []

        # Checks every fields, and adds the empty one to the grid its part of
        for y in range(len(bot['guesses'])):
            for x in range(len(bot['guesses'])):
                if bot['guesses'][y][x] == "0":
                    if (y % 2 == 0 and x % 2 == 0) or (y % 2 == 1 and x % 2 == 1):
                        hunting_grid_00.append(chr(65 + y) + str(x + 1))
                    else:
                        hunting_grid_01.append(chr(65 + y) + str(x + 1))

        # Finally, it checks which list is the smallest of the 2, and sets it as our hunting grid
        # One Grid is chosen at random to reduce predicting possibilities
        hunting_grid = random.choice([hunting_grid_01, hunting_grid_00])
        if len(hunting_grid) > len(hunting_grid_01):
            hunting_grid = hunting_grid_01
        elif len(hunting_grid) > len(hunting_grid_00):
            hunting_grid = hunting_grid_00

    # If the smallest ship is already sunk, the next smallest one is 3 field long
    else:
        # This gives us 6 possible grids of diagonal lines spaced by 2 fields
        # Named based on their first position in the x=0 column and wherever the diagonal goes up or down from there
        hunting_grid_0_up = []
        hunting_grid_0_down = []
        hunting_grid_1_up = []
        hunting_grid_1_down = []
        hunting_grid_2_up = []
        hunting_grid_2_down = []
        possible_grids = [hunting_grid_0_up,
                          hunting_grid_0_down,
                          hunting_grid_1_up,
                          hunting_grid_1_down,
                          hunting_grid_2_up,
                          hunting_grid_2_down]
        # Each field is checked and the empty ones are added to their corresponding grid
        for y in range(len(bot['guesses'])):
            for x in range(len(bot['guesses'])):
                if bot['guesses'][y][x] == "0":
                    if x % 3 == 0:
                        if y % 3 == 0:
                            hunting_grid_0_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_0_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 1:
                            hunting_grid_1_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_1_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 2:
                            hunting_grid_2_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_2_down.append(chr(65 + y) + str(x + 1))

                    elif x % 3 == 1:
                        if y % 3 == 0:
                            hunting_grid_1_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_2_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 1:
                            hunting_grid_2_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_0_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 2:
                            hunting_grid_0_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_1_down.append(chr(65 + y) + str(x + 1))

                    elif x % 3 == 2:
                        if y % 3 == 0:
                            hunting_grid_2_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_1_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 1:
                            hunting_grid_0_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_2_down.append(chr(65 + y) + str(x + 1))
                        elif y % 3 == 2:
                            hunting_grid_1_up.append(chr(65 + y) + str(x + 1))
                            hunting_grid_0_down.append(chr(65 + y) + str(x + 1))

        # A possible grid is chosen at random and all grid are compared to each other to find the smallest
        hunting_grid = random.choice(possible_grids)
        for grid in possible_grids:
            if len(grid) < len(hunting_grid):
                hunting_grid = grid

    # Once the smallest grid is found (i.e. the one with the least field left to check), one field is chosen at random
    return random.choice(hunting_grid)
