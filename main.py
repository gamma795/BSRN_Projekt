import pve_game
import pvp_game
import settings
import game_functions

# Settings defaults values
# could import statistic from existing file instead if we implement this feature
board_size = 10
player_1 = {"name": "Player 1", "score": 0}
player_2 = {"name": "Player 2", "score": 0}


def show_main_menu():
    """Shows the options from the main menu"""
    settings.clear_screen()
    print("  Wilkommen bei SCHIFFEVERSENKEN-2021 \n")
    print("  Was wollen Sie tun:\n\n   1: Spiel starten \n   2: Spielfeldgröße ändern \n   3: Spiel verlassen")


# Start menu
settings.clear_screen()
show_main_menu()
print("\n")

# Locked in this loop until quit option is select and "break;" or "exit()" is reached
while True:
    try:
        main_menu_input = int(input("  Ihre Wahl: "))

        # Opening Game typ menu and choosing between "PvP", "PvE", and "Go back"
        if main_menu_input == 1:
            settings.clear_screen()
            number_of_human_players = settings.game_typ()

            # Start game against bot
            if number_of_human_players == 1:
                pve_game.launch(player_1, player_2, board_size)
                show_main_menu()
                print("\n")

            # Start game against humain
            elif number_of_human_players == 2:
                pvp_game.launch(player_1, player_2, board_size)
                show_main_menu()
                print("\n")

            # Go back to main menu
            elif number_of_human_players == 3:
                settings.clear_screen()
                show_main_menu()
                print("\n")

        # Open menu to set board size. If more option are added (number of ship, bot level, etc) It could open a sub menu instead
        elif main_menu_input == 2:
            settings.clear_screen()
            board_size = settings.set_board_size()
            settings.clear_screen()
            show_main_menu()
            print("\n")

        # Leave game
        elif main_menu_input == 3:
            settings.clear_screen()
            print(" Auf Wiedersehen!")
            exit()

        # Catch wrong input
        else:
            show_main_menu()
            settings.invalid_input()

    # Catch wron value input
    except ValueError:
        show_main_menu()
        settings.invalid_input()
        continue
