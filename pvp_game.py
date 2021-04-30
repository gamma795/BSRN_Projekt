import random
import settings
import game_functions


def launch(player_1, player_2, board_size):
    settings.clear_screen()

    print("  Mensch gegen Mensch\n")
    player_1 = game_functions.set_new_player(board_size)
    player_2 = game_functions.set_new_player(board_size, player_1["name"])
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
    print(f'  {active_player["name"]} fägt an. Drücken Sie ENTER wenn nur noch {active_player["name"]} am Computer ist:')
    input()
    while True:
        if active_player == player_1:
            player_input = game_functions.ask_input_from(player_1, possible_input)
            if player_input == "EXIT":
                break;
            (player_1, player_2) = game_functions.update_boards(player_1, player_2, player_input)
            active_player = game_functions.switch_player(active_player, player_1, player_2)

        else:
            player_input = game_functions.ask_input_from(player_2, possible_input)
            if player_input == "EXIT":
                break;
            (player_2, player_1) = game_functions.update_boards(player_2, player_1, player_input)
            active_player = game_functions.switch_player(active_player, player_1, player_2)
