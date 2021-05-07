import random
import settings
import game_functions


def launch(player_1, player_2, board_size):
    settings.clear_screen()

    print("  Mensch gegen Mensch\n")
    # Create the 2 players with empty boards
    player_1 = game_functions.set_new_player(board_size)
    player_2 = game_functions.set_new_player(board_size, player_1["name"])

    # Set possible input list
    possible_input = []
    for y in range(board_size):
        for x in range(board_size):
            possible_input.append(chr(65 + y) + str(x + 1))

    settings.clear_screen()
    ship_num = game_functions.number_of_ships()
    shiff_verteilung = game_functions.set_ship_distribution(ship_num)
    settings.clear_screen()

    print("Spieler 1\n-------------------")
    ship = 1
    x = True
    while x == True:

        for key in shiff_verteilung:

            if key == "smal":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]
            elif key == "medium":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]
            elif key == "big":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]

            for schiff_count in range(zahl_der_schiffe):
                for feld in range(zahl_der_felder):

                    # Ask for player input and check if input is possible
                    player_input = game_functions.ask_input_for_ship(player_1, possible_input, ship, feld,
                                                                     zahl_der_felder)

                    # Y=Buchstabe
                    # X=Zahl

                    if len(player_input) == 2:
                        y_achse = ord(player_input[0]) - 65
                        x_achse = int(player_input[1]) - 1

                        # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
                    elif len(player_input) == 3:
                        y_achse = ord(player_input[0]) - 65
                        x_achse = int(player_input[1:3]) - 1

                    player_1["board"][y_achse][x_achse] = "S"

                    if key == "big":
                        x = False

                    if feld == zahl_der_felder - 1:
                        ship += 1
                        print()
                        print()
                        break
                    print()

        ship += 1

    print("Spieler 2\n-------------------")

    settings.clear_screen()
    ship = 1
    x = True
    while x == True:

        for key in shiff_verteilung:

            if key == "smal":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]
            elif key == "medium":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]
            elif key == "big":
                zahl_der_felder = game_functions.ret_ship_len(key)
                zahl_der_schiffe = shiff_verteilung[key]

            for schiff_count in range(zahl_der_schiffe):
                for feld in range(zahl_der_felder):

                    # Ask for player input and check if input is possible
                    player_input = game_functions.ask_input_for_ship(player_2, possible_input, ship, feld,
                                                                     zahl_der_felder)

                    # Y=Buchstabe
                    # X=Zahl

                    if len(player_input) == 2:
                        y_achse = ord(player_input[0]) - 65
                        x_achse = int(player_input[1]) - 1

                        # Convert player input into two int x and y to check the boards at specific place (case with number 10 or higher)
                    elif len(player_input) == 3:
                        y_achse = ord(player_input[0]) - 65
                        x_achse = int(player_input[1:3]) - 1

                    player_2["board"][y_achse][x_achse] = "S"

                    if key == "big":
                        x = False

                    if feld == zahl_der_felder - 1:
                        ship += 1
                        print()
                        print()
                        break
                    print()

        ship += 1

    # Test ship placement.

    # Welcome message
    settings.clear_screen()
    print(f"  Willkommen, {player_1.get('name')} und {player_2.get('name')}! Möge die Schlacht beginnen!\n")

    # Choose starting player randomly
    active_player = random.choice([player_1, player_2])

    # Starting the game
    print(
        f'  {active_player["name"]} fägt an. Drücken Sie ENTER wenn nur noch {active_player["name"]} am Computer ist:')
    input()  # Wait for input before starting

    # Anzahl der aktiven Schiffsteile
    player1_active_ships = game_functions.list_len(player_1["board"])
    player2_active_ships = game_functions.list_len(player_2["board"])

    while True:
        if active_player == player_1:

            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_1, possible_input)

            # Option to return to main menu
            if player_input == "EXIT":
                break;

            # Update the boards
            (player_1, player_2) = game_functions.update_boards(player_1, player_2, player_input)

            # Check if hit
            player1_active_ships = game_functions.check_if_hit(player_input, player_2, player1_active_ships)

            # Check if someone won
            player_won = game_functions.check_if_won(player1_active_ships, player2_active_ships)

            if player_won == True:
                settings.clear_screen()
                input(f'  {active_player["name"]} hat gewonnen! \n  Drücke Enter um zurück zum Hauptmenu zu kommen')
                break;

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2)

        else:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_2, possible_input)

            # Option to return to main menu
            if player_input == "EXIT":
                break;

            # Update the boards
            (player_2, player_1) = game_functions.update_boards(player_2, player_1, player_input)

            # Check if hit
            player2_active_ships = game_functions.check_if_hit(player_input, player_1, player2_active_ships)

            # Check if someone won
            player_won = game_functions.check_if_won(player1_active_ships,
                                                     player2_active_ships)

            if player_won == True:
                settings.clear_screen()
                input(f'  {active_player["name"]} hat gewonnen! \n  Drücke Enter um zurück zum Hauptmenu zu kommen')
                break;

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2)
