import languages


def clear_screen():
    """function for clearing the screen"""
    for j in range(50):
        print("")


def invalid_input(language):
    """function to display "invalid input" error message"""
    print(f"\n  {language['invalid_input']}.")


def show_main_menu(language):
    """Shows the options from the main settings_menu"""
    clear_screen()
    print(f"  {language['welcome_screen']} \n")
    print(
        f"  {language['what_to_do']}\n\n   1: {language['start_game']} \n   2: {language['settings']} \n   3: {language['quit']}")


def show_settings_menu(language):
    """Shows the options from the main settings_menu"""
    clear_screen()
    print(f"  {language['settings']} \n")
    print(
        f"  {language['what_to_do']}:\n\n   1: {language['change_board_size']} \n   2: {language['change_ship_amount']} \n   3: {language['change_language']} \n   4: {language['back']}")


def settings_menu(settings_values, language):
    show_settings_menu(language)
    print("\n")

    while True:
        try:
            settings_menu_input = int(input(f"  {language['your_choice']} "))

            # # Open settings_menu to set board size
            if settings_menu_input == 1:
                clear_screen()
                settings_values["board_size"] = set_board_size(language)
                clear_screen()
                show_settings_menu(language)
                print("\n")

            # Set the amount of ships
            elif settings_menu_input == 2:
                clear_screen()
                settings_values["number_of_ships"] = set_number_of_ships(language)
                clear_screen()
                show_settings_menu(language)
                print("\n")

            # Go back to main settings_menu
            elif settings_menu_input == 3:
                while True:
                    try:
                        clear_screen()
                        print(f"  {language['choose_language']}\n\n")
                        print(f"   1: Deutsch\n   2: English \n   3: {language['back']}\n\n")
                        player_input = int(input(f"  {language['your_choice']}: "))
                        if player_input == 1:
                            language = languages.deutsch
                            break
                        elif player_input == 2:
                            language = languages.english
                            break
                        elif player_input == 3:
                            break
                        else:
                            invalid_input(language)
                    except ValueError:
                        invalid_input(language)
                        continue
                show_settings_menu(language)
                print("\n")

            # Go back to main settings_menu
            elif settings_menu_input == 4:
                clear_screen()
                show_main_menu(language)
                print("\n")
                break

            # Catch wrong input
            else:
                show_settings_menu(language)
                invalid_input(language)

        # Catch wrong value input
        except ValueError:
            show_settings_menu(language)
            invalid_input(language)
            continue

    return settings_values, language


def set_board_size(language):
    """Choose the Size of the board"""
    board_size_option = [7, 8, 9, 10, 11, 12]

    # Locked in this loop until valid option is select and "break;" is reached
    while True:
        try:
            print(f"  {language['choose_board_size']} [Standard = 10]: \n")

            # Print possible board sizes and ask player to choose
            for i in range(len(board_size_option)):
                print(f"   {i + 1}: {board_size_option[i]}x{board_size_option[i]}")

            size = int(input(f"\n\n  {language['your_choice']}: "))

            # If player input is in the possible range board size is set and we leave the loop to go back to main settings_menu
            if 0 <= size <= len(board_size_option):
                clear_screen()
                print(
                    f"  Spielfeldgröße wurde auf {board_size_option[size - 1]}x{board_size_option[size - 1]} festgelegt")
                return board_size_option[size - 1]
                break

            # Bad input ask for player input again
            else:
                clear_screen()
                invalid_input(language)

        # Bad input ask for player input again
        except ValueError:
            clear_screen()
            invalid_input(language)
            continue


def game_typ(language):
    """Choose between pvp and pve or go back"""
    while True:
        try:
            # Display choice between PvP, PvE, and go back
            number_of_human_players = int(
                input(
                    f"  {language['type_of_game']}:\n\n   1: {language['pve']} \n   2: {language['pvp']} \n   3: {language['back']} \n\n  {language['your_choice']}: "))
            if number_of_human_players == 1:
                break
            elif number_of_human_players == 2:
                break
            elif number_of_human_players == 3:
                break
            else:
                clear_screen()
                invalid_input(language)
        except ValueError:
            clear_screen()
            invalid_input(language)
            continue
    return number_of_human_players


# Fragt nach wie viele Schiffe man setzen will
def set_number_of_ships(language):
    while True:
        try:
            ships_num = int(input(f"  {language['how_many_ships']} [Standard = 5] : "))
            if 3 <= ships_num < 11:
                break
            else:
                clear_screen()
                print(f"  {language['how_many_ships_error']}: ")

        except ValueError:
            clear_screen()
            invalid_input(language)
            continue

    return ships_num


def leave_game(language):
    clear_screen()
    while True:
        try:

            player_input = input(f"  {language['really_leave']} (y/n) : ")
            if player_input == "y":
                return True
            elif player_input == "n":
                return False
            else:
                clear_screen()
                print(f" {language['really_leave_error']}")

        except ValueError:
            clear_screen()
            print(f" {language['really_leave_error']}")
            continue
