import languages
import pve_game
import pvp_game
import menu

# Settings defaults values
# could import statistic from existing file instead if we implement this feature
language = languages.deutsch
settings_values = {'board_size': 7, 'number_of_ships': 10, 'bot_difficulty': "normal", 'countdown_on': True}
player_1 = {'name': "Player 1", 'score': 0}
player_2 = {'name': "Player 2", 'score': 0}

# Start settings_menu
menu.clear_screen()
menu.show_main_menu(language)
print("\n")

# Locked in this loop until quit option is select and "break;" or "exit()" is reached
while True:
    try:
        main_menu_input = int(input(f"  {language['your_choice']}: "))

        # Opening Game typ settings_menu and choosing between "PvP", "PvE", and "Go back"
        if main_menu_input == 1:
            menu.clear_screen()
            number_of_human_players = menu.game_typ(language)

            # Start game against bot
            if number_of_human_players == 1:
                pve_game.launch(player_1, player_2, settings_values, language)
                menu.show_main_menu(language)
                print("\n")

            # Start game against human
            elif number_of_human_players == 2:
                pvp_game.launch(player_1, player_2, settings_values, language)
                menu.show_main_menu(language)
                print("\n")

            # Go back to main settings_menu
            elif number_of_human_players == 3:
                menu.clear_screen()
                menu.show_main_menu(language)
                print("\n")

        # Open settings_menu
        elif main_menu_input == 2:
            menu.clear_screen()
            settings_values, language = menu.settings_menu(settings_values, language)
            menu.clear_screen()
            menu.show_main_menu(language)
            print("\n")

        # Leave game
        elif main_menu_input == 3:
            menu.clear_screen()
            print(f"  {language['bye']}\n")
            input()
            exit()

        # Catch wrong input
        else:
            menu.show_main_menu(language)
            menu.invalid_input(language)

    # Catch wrong value input
    except ValueError:
        menu.show_main_menu(language)
        menu.invalid_input(language)
        continue
