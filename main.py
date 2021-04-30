import pve_game
import pvp_game
import settings
import game_functions

# Settings up defaults values
board_size = 10
player_1 = {"name": "Player 1", "score": 0}
player_2 = {"name": "Player 2", "score": 0}
# could import statistic from existing file

def show_main_menu():
    settings.clear_screen()
    print("  Wilkommen bei SCHIFFEVERSENKEN-2021 \n")
    print("  Was wollen Sie tun:\n\n   1: Spiel starten \n   2: Spielfeldgröße ändern \n   3: Spiel verlassen")


# Start menu
settings.clear_screen()
show_main_menu()
print("\n")
while True:
    try:
        main_menu_input = int(input("  Ihre Wahl: "))

        if main_menu_input == 1:
            settings.clear_screen()
            number_of_human_players = settings.game_typ()
            if number_of_human_players == 1:
                pve_game.launch(player_1, player_2, board_size)
                show_main_menu()
                print("\n")
                continue

            elif number_of_human_players == 2:
                pvp_game.launch(player_1, player_2, board_size)
                show_main_menu()
                print("\n")
                continue

            elif number_of_human_players == 3:
                settings.clear_screen()
                show_main_menu()
                print("\n")
                continue


        elif main_menu_input == 2:
            settings.clear_screen()
            board_size = settings.set_board_size()
            settings.clear_screen()
            show_main_menu()
            print("\n")


        elif main_menu_input == 3:
            settings.clear_screen()
            print(" Auf Wiedersehen!")
            exit()
        else:
            show_main_menu()
            settings.invalid_input()
    except ValueError:
        show_main_menu()
        settings.invalid_input()
        continue

