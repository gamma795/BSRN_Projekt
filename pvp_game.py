import random
import settings
import game_functions


def launch(player_1, player_2, board_size):
    settings.clear_screen()

    print("  Mensch gegen Mensch\n")
    # Create the 2 players with empty boards
    player_1 = game_functions.set_new_player(board_size)
    player_2 = game_functions.set_new_player(board_size, player_1["name"])

    # Test Ship placement. To be replaced with function to choose Ship positions
    player_1["board"][0][0] = "S"
    player_1["board"][0][1] = "S"
    player_2["board"][1][1] = "S"
    player_2["board"][1][2] = "S"
    # Test ship placement.

    # Welcome message
    settings.clear_screen()
    print(f"  Willkommen, {player_1.get('name')} und {player_2.get('name')}! Möge die Schlacht beginnen!\n")

    # Set possible input list
    possible_input = []
    for y in range(board_size):
        for x in range(board_size):
            possible_input.append(chr(65 + y) + str(x + 1))

    # Choose starting player randomly
    active_player = random.choice([player_1, player_2])

    # Starting the game
    print(
        f'  {active_player["name"]} fägt an. Drücken Sie ENTER wenn nur noch {active_player["name"]} am Computer ist:')
    input()  # Wait for input before starting

    while True:
        if active_player == player_1:

            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_1, possible_input)

            # Option to return to main menu
            if player_input == "EXIT":
                break;

            # Update the boards
            (player_1, player_2) = game_functions.update_boards(player_1, player_2, player_input)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)
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

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, player_2)
            if player_won == True:
                settings.clear_screen()
                input(f'  {active_player["name"]} hat gewonnen! \n  Drücke Enter um zurück zum Hauptmenu zu kommen')
                break;

            # Switch active player
            active_player = game_functions.switch_player(active_player, player_1, player_2)
