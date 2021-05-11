def clear_screen():
    """function for clearing the screen"""
    for j in range(50):
        print("")


def invalid_input():
    """function to display "invalid input" error message"""
    print("\n  Die Eingabe ist keine gültige Option.")


def show_main_menu():
    """Shows the options from the main settings_menu"""
    clear_screen()
    print("  Wilkommen bei SCHIFFEVERSENKEN-2021 \n")
    print("  Was wollen Sie tun:\n\n   1: Spiel starten \n   2: Einstellungen \n   3: Spiel verlassen")


def show_settings_menu():
    """Shows the options from the main settings_menu"""
    clear_screen()
    print("  Einstellungen \n")
    print("  Was wollen Sie tun:\n\n   1: Spielfeldgröße ändern \n   2: Schiffanzahl ändern \n   3: Zurück")


def settings_menu(settings_values):
    show_settings_menu()
    print("\n")

    while True:
        try:
            settings_menu_input = int(input("  Ihre Wahl: "))

            # # Open settings_menu to set board size
            if settings_menu_input == 1:
                clear_screen()
                settings_values["board_size"] = set_board_size()
                clear_screen()
                show_settings_menu()
                print("\n")

            # Set the amount of ships
            elif settings_menu_input == 2:
                clear_screen()
                settings_values["number_of_ships"] = set_number_of_ships()
                clear_screen()
                show_settings_menu()
                print("\n")

            # Go back to main settings_menu
            elif settings_menu_input == 3:
                clear_screen()
                show_main_menu()
                print("\n")
                break;

            # Catch wrong input
            else:
                show_settings_menu()
                invalid_input()


        # Catch wrong value input
        except ValueError:
            show_settings_menu()
            invalid_input()
            continue

    return settings_values


def set_board_size():
    """Choose the Size of the board"""
    board_size_option = [7, 8, 9, 10, 11, 12]

    # Locked in this loop until valid option is select and "break;" is reached
    while True:
        try:
            print("  Wählen Sie eine möglich Spielfeldgröße aus [Standard = 10]: \n")

            # Print possible board sizes and ask player to choose
            for i in range(len(board_size_option)):
                print(f"   {i + 1}: {board_size_option[i]}x{board_size_option[i]}")

            size = int(input("\n\n  Ihre Wahl: "))

            # If player input is in the possible range board size is set and we leave the loop to go back to main settings_menu
            if size >= 0 and size <= len(board_size_option):
                clear_screen()
                print(
                    f"  Spielfeldgröße wurde auf {board_size_option[size - 1]}x{board_size_option[size - 1]} festgelegt")
                return board_size_option[size - 1]
                break;

            # Bad input ask for player input again
            else:
                clear_screen()
                invalid_input()

        # Bad input ask for player input again
        except ValueError:
            clear_screen()
            invalid_input()
            continue


def game_typ():
    """Choose between pvp and pve or go back"""
    while True:
        try:
            # Display choice between PvP, PvE, and go back
            number_of_human_players = int(
                input(
                    "  Wählen Sie die gewünschte Spielart:\n\n   1: Player vs Bot \n   2: Player vs Player \n   3: Zurück \n\n  Ihre Wahl: "))
            if number_of_human_players == 1:
                break;
            elif number_of_human_players == 2:
                break;
            elif number_of_human_players == 3:
                break;
            else:
                clear_screen()
                invalid_input()
        except ValueError:
            clear_screen()
            invalid_input()
            continue
    return number_of_human_players


# Fragt nach wie viele Schiffe man setzen will
def set_number_of_ships():
    while True:
        try:
            ships_num = int(input("  Wie viele Schiffe wollen Sie platzieren [Standard = 5] : "))
            if ships_num >= 3 and ships_num < 11:
                break;
            else:
                clear_screen()
                print("  Sie müssen mindestens 3 und maximal 10 Schiffe platzieren: ")

        except ValueError:
            clear_screen()
            invalid_input()
            continue

    return ships_num
