def ask_input_from(player, possible_input, board_size):
    """Ask for player input and checks against list of possible inputs and already tried"""
    drawing_utils.draw_boards(player)
    print("\n")
    when_to_stop = 15

    while when_to_stop > 0:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print(time_left + "\r", end="")
        time.sleep(1)
        when_to_stop -= 1

        try:
            player_input = str(input("  Was ist Ihr nächster Zug: ")).upper()
            if player_input == "EXIT":
                break
            if player_input not in possible_input:
                drawing_utils.draw_boards(player)
                print("\n  Das ist keine gültige Eingabe")
                continue
            else:
                if player_input in player["already_tried"]:
                    drawing_utils.draw_boards(player)
                    print("\n  Sie haben schon auf dieses Feld geschossen.")
                    continue
                else:
                    player["already_tried"].append(player_input)
                    break

        except ValueError:
            drawing_utils.draw_boards(player)
            print("\n  Das ist keine gültige Eingabe")
            continue
            return player_input
    else:
        return zufallsGenerator.random_ship_attac(board_size)