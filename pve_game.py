import random

import drawing_utils
import menu
import game_functions


def launch(player_1, bot, settings_values, language):
    menu.clear_screen()
    print(f"  {language['human_v_machine']}!\n")

    board_size = settings_values['board_size']
    # Set possible input list
    possible_input = []
    for y in range(settings_values['board_size']):
        for x in range(settings_values['board_size']):
            possible_input.append(chr(65 + y) + str(x + 1))

    ship_list = game_functions.set_ship_distribution(settings_values['number_of_ships'], language)

    # Player is set up
    player_1 = game_functions.set_new_player(settings_values['board_size'], language, "bot")
    player_1['ships_left'] = settings_values['number_of_ships']
    player_1['enemy_ships_left'] = settings_values['number_of_ships']
    player_1['not_yet_tried'] = []
    player_1['not_yet_tried'].extend(possible_input)

    # Bot is set up based on its difficulty level
    bot['level'] = settings_values['bot_difficulty']

    if bot['level'] is "hard":
        bot_name = ["Smart", "Dangerous", "Cool"]
        bot['name'] = random.choice(bot_name) + " Bot"
        bot['enemy_ship_sizes'] = []
        for ships in ship_list:
            bot['enemy_ship_sizes'].append(ships['size'])

    elif bot['level'] is "normal":
        bot_name = ["Chill", "Average"]
        bot['name'] = random.choice(bot_name) + " Bot"

    else:
        bot_name = ["Silly", "Bad", "Idiot", "Slow", "Dumb"]
        bot['name'] = random.choice(bot_name) + " Bot"

    bot['board'] = game_functions.setup_new_board(board_size)
    bot['guesses'] = game_functions.setup_new_board(board_size)
    bot['not_yet_tried'] = []
    bot['not_yet_tried'].extend(possible_input)
    bot['ships_left'] = settings_values['number_of_ships']
    bot['enemy_ships_left'] = settings_values['number_of_ships']
    bot['current_target'] = []
    bot['possible_target'] = []

    menu.clear_screen()

    # Welcome message
    menu.clear_screen()
    print(
        f"  {language['welcome']}, {player_1.get('name')}!"
        f" {language['you_are_playing_against']} {bot.get('name')}! {language['start_the_fight']}!\n"
    )
    input()
    menu.clear_screen()

    # Starting the game
    # Ships placement phase

    # bot places its ship randomly
    bot = game_functions.random_ship_placement(bot, possible_input, ship_list, language)
    print(f"  {bot['name']} {language['placed_their_ships']}.\n")
    player_1 = game_functions.choose_ship_placement_methode(player_1, possible_input, ship_list, language)

    # Choose starting player randomly
    active_player = random.choice([player_1, bot])

    # Shooting phase
    while True:
        if active_player == player_1:
            # Ask for player input and check if input is possible
            player_input = game_functions.ask_input_from(player_1, possible_input, language, settings_values)

            # Option to return to main settings_menu
            if player_input == "EXIT":
                leave = menu.leave_game(language)
                if leave:
                    break
                else:
                    continue

            # Check if hit and Update the boards
            (player_1, bot) = game_functions.update_boards(player_1, bot, player_input, language)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, bot)
            if player_won:
                menu.clear_screen()
                input(f"  {active_player['name']} {language['has_won_the_game']} \n"
                      f"  {language['enter_to_go_back']}")
                break

            # Switch active player
            active_player = bot

        else:
            player_input = game_functions.bot_player_input(bot)
            print("  Bot chose " + player_input)  # To catch errors
            bot['not_yet_tried'].remove(player_input)

            # Update the boards
            (bot, player_1) = game_functions.update_boards(bot, player_1, player_input, language)
            drawing_utils.draw_boards(player_1, language)

            # Check if someone won
            player_won = game_functions.check_if_won(player_1, bot)

            if player_won:
                menu.clear_screen()
                input(f"  {active_player['name']} {language['has_won_the_game']} \n"
                      f"  {language['enter_to_go_back']}")
                break

            # Switch active player
            active_player = player_1
