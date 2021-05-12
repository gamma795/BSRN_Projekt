import random
import menu
import game_functions


def launch(player_1, player_2, settings_values, language):
    menu.clear_screen()
    print("  \n")

    # Create the 2 players with empty boards
    player_1 = game_functions.set_new_player(settings_values["board_size"], language)
    player_1["ships_left"] = settings_values["number_of_ships"]
    player_1["enemy_ships_left"] = settings_values["number_of_ships"]

    player_2 = game_functions.set_new_player(settings_values["board_size"], language, player_1["name"])
    player_2["ships_left"] = settings_values["number_of_ships"]
    player_2["enemy_ships_left"] = settings_values["number_of_ships"]

    # Set possible input list
    possible_input = []
    for y in range(settings_values["board_size"]):
        for x in range(settings_values["board_size"]):
            possible_input.append(chr(65 + y) + str(x + 1))

    menu.clear_screen()
    ship_list = game_functions.set_ship_distribution(settings_values["number_of_ships"], language)

    # Welcome message
    menu.clear_screen()
    print(
        f"  {language['welcome']}, {player_1.get('name')} {language['and']} {player_2.get('name')}! {language['start_the_fight']}!\n")

    # Choose starting player randomly
    active_player = random.choice([player_1, player_2])

    # Starting the game
    # Ships placement phase

    if active_player == player_1:
        print(
            f'  {player_1["name"]} {language["is_playing_look_away"]} {player_1["name"]} {language["is_at_the_screen"]}:')
        input()
        player_1 = game_functions.choose_ship_placement_methode(player_1, possible_input, ship_list, language)
        menu.clear_screen()
        print(
            f'  {player_2["name"]} {language["is_playing_look_away"]} {player_2["name"]} {language["is_at_the_screen"]}:')
        input()
        player_2 = game_functions.choose_ship_placement_methode(player_2, possible_input, ship_list, language)
    elif active_player == player_2:
        print(
            f'  {player_2["name"]} {language["is_playing_look_away"]} {player_2["name"]} {language["is_at_the_screen"]}:')
        input()
        player_2 = game_functions.choose_ship_placement_methode(player_2, possible_input, ship_list, language)
        menu.clear_screen()
        print(
            f'  {player_1["name"]} {language["is_playing_look_away"]} {player_1["name"]} {language["is_at_the_screen"]}:')
        input()
        player_1 = game_functions.choose_ship_placement_methode(player_1, possible_input, ship_list, language)

    menu.clear_screen()
    print(
        f'  {active_player["name"]} {language["is_playing_look_away"]} {active_player["name"]} {language["is_at_the_screen"]}: ')
    input()

    while True:
        if active_player == player_1:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_1, possible_input, language)

            # Option to return to main settings_menu
            if player_input == "EXIT":
                leave = menu.leave_game(language)
                if leave:
                    break
                else:
                    continue

            # Check if hit and Update the boards
            (player_1, player_2) = game_functions.update_boards(player_1, player_2, player_input, language)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)
            if player_won:
                menu.clear_screen()
                input(f'  {active_player["name"]} {language["has_won_the_game"]} \n  {language["enter_to_go_back"]}')
                break

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2, language)

        else:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_2, possible_input, language)

            # Option to return to main menu
            if player_input == "EXIT":
                leave = menu.leave_game(language)
                if leave:
                    break
                else:
                    continue

            # Update the boards
            (player_2, player_1) = game_functions.update_boards(player_2, player_1, player_input, language)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)

            if player_won:
                menu.clear_screen()
                input(f'  {active_player["name"]} {language["has_won_the_game"]} \n  {language["enter_to_go_back"]}')
                break

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2, language)
