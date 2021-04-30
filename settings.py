def clear_screen():
    """function for clearing the screen"""
    for j in range(50):
        print("")


def invalid_input():
    """function to display "invalid input" error message"""
    clear_screen()
    print("Die Eingabe ist keine gültige Option.")


def set_board_size():
    """Choose the Size of the board"""
    board_size_option = [7, 8, 9, 10, 11, 12]

    while True:
        try:
            print("Wählen Sie eine möglich Spielfeldgröße aus:\n")
            for i in range(len(board_size_option)):
                print(f"{i + 1}: {board_size_option[i]}x{board_size_option[i]}")

            size = int(
                input("\n\nIhre Wahl: "))
            if size >= 0 and size <= len(board_size_option):
                clear_screen()
                print(
                    f"Spielfeldgröße wurde auf {board_size_option[size - 1]}x{board_size_option[size - 1]} festgelegt")
                return board_size_option[size - 1]
                break;
            else:
                invalid_input()
        except ValueError:
            invalid_input()
            continue


def game_typ():
    """Choose between pvp and pve or go back"""
    while True:
        try:
            number_of_human_players = int(
                input(
                    "Wählen Sie die gewünschte Spielart:\n\n  1: Player vs Bot \n  2: Player vs Player \n  3: Zurück \n\nIhre Wahl: "))
            if number_of_human_players == 1:
                break;
            elif number_of_human_players == 2:
                break;
            elif number_of_human_players == 3:
                break;
            else:
                invalid_input()
        except ValueError:
            invalid_input()
            continue
    return number_of_human_players
