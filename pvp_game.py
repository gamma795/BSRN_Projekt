import random
import menu
import game_functions


def launch(player_1, player_2, settings_values):
    menu.clear_screen()
    print("  Mensch gegen Mensch\n")

    # Create the 2 players with empty boards
    player_1 = game_functions.set_new_player(settings_values["board_size"])
    player_1["ships_left"] = settings_values["number_of_ships"]
    player_1["enemy_ships_left"] = settings_values["number_of_ships"]

    player_2 = game_functions.set_new_player(settings_values["board_size"], player_1["name"])
    player_2["ships_left"] = settings_values["number_of_ships"]
    player_2["enemy_ships_left"] = settings_values["number_of_ships"]

    # Set possible input list
    possible_input = []
    for y in range(settings_values["board_size"]):
        for x in range(settings_values["board_size"]):
            possible_input.append(chr(65 + y) + str(x + 1))

    menu.clear_screen()
    ship_list = game_functions.set_ship_distribution(settings_values["number_of_ships"])

    # Welcome message
    menu.clear_screen()
    print(f"  Willkommen, {player_1.get('name')} und {player_2.get('name')}! Möge die Schlacht beginnen!\n")

    # Choose starting player randomly
    active_player = random.choice([player_1, player_2])

    # Starting the game
    print(
        f'  {active_player["name"]} fägt an. Drücken Sie ENTER wenn nur noch {active_player["name"]} am Computer ist:')
    input()  # Wait for input before starting

    # Ships placement phase

    if active_player == player_1:
        player_1 = game_functions.choose_ship_placement_methode(player_1, possible_input, ship_list)
        menu.clear_screen()
        print(
            f'  {player_2["name"]} ist dran. Drücken Sie ENTER wenn nur noch {player_2["name"]} am Computer ist:')
        input()
        player_2 = game_functions.choose_ship_placement_methode(player_2, possible_input, ship_list)
    elif active_player == player_2:
        player_2 = game_functions.choose_ship_placement_methode(player_2, possible_input, ship_list)
        menu.clear_screen()
        print(
            f'  {player_1["name"]} ist dran. Drücken Sie ENTER wenn nur noch {player_1["name"]} am Computer ist:')
        input()
        player_1 = player_1 = game_functions.choose_ship_placement_methode(player_1, possible_input, ship_list)

    menu.clear_screen()
    print(
        f'  {active_player["name"]} ist dran. Drücken Sie ENTER wenn nur noch {active_player["name"]} am Computer ist:')
    input()

    while True:
        if active_player == player_1:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_1, possible_input)

            # Option to return to main settings_menu
            if player_input == "EXIT":
                leave = menu.leave_game()
                if leave == True:
                    break;
                else:
                    continue

            # Check if hit and Update the boards
            (player_1, player_2) = game_functions.update_boards(player_1, player_2, player_input)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)
            if player_won == True:
                menu.clear_screen()
                input(f'  {active_player["name"]} hat gewonnen! \n  Drücke Enter um zurück zum Hauptmenu zu kommen')
                break;

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2)


        else:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_2, possible_input)

            # Option to return to main menu
            if player_input == "EXIT":
                leave = menu.leave_game()
                if leave == True:
                    break;
                else:
                    continue

            # Update the boards
            (player_2, player_1) = game_functions.update_boards(player_2, player_1, player_input)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)

            if player_won == True:
                menu.clear_screen()
                input(f'  {active_player["name"]} hat gewonnen! \n  Drücke Enter um zurück zum Hauptmenu zu kommen')
                break;

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2)
