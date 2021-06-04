import menu


def field_filling(value):
    """Sets how the Board position will be displayed and translates board info into graphics"""
    # empty field
    if value == "0":
        return "   "
    # ship Carrier, Battleship, Cruiser, Submarine or Destroyer
    elif value in ["Pa1", "Pa2", "Pa3", "Pa4", "Su1", "Su2", "Des", "Ba1", "Ba2", "Car"]:
        return "███"
    # hit ship
    elif value in ["Pa1_Hit", "Pa2_Hit", "Pa3_Hit", "Pa4_Hit", "Su1_Hit", "Su2_Hit", "Des_Hit", "Ba1_Hit", "Ba2_Hit",
                   "Car_Hit"]:
        return "▒X▒"
    # sunk ship
    elif value == "SS":
        return "░X░"
    # wrong guess
    elif value == "WG":
        return " O "
    # correct guess
    elif value == "CG":
        return " X "


def boards_to_blueprint(player, board_spacing):
    # Defines how big the Blueprint is going to be and fills it with empty spaces
    blueprint_height = len(player['board']) * 2 + 3
    blueprint_width = 1 + (len(player['board'][0]) * 2 + 3) * 2 + board_spacing
    blueprint = [["   " for i in range(blueprint_width)] for j in range(blueprint_height)]

    # Fill in the players board with space in between for the walls
    for y in range(len(player['board'])):
        for x in range(len(player['board'][0])):
            blueprint[y * 2 + 3][x * 2 + 4] = player['board'][y][x]

    # Fill in the players guess board with space in between for the walls
    for y in range(len(player['guesses'])):
        for x in range(len(player['guesses'][0])):
            blueprint[y * 2 + 3][x * 2 + 4 + len(player['board']) * 2 + 3 + board_spacing] = player['guesses'][y][x]

    # Column numbering on both boards
    for x in range(len(player['board'][0])):
        if x + 1 < 10:
            blueprint[0][x * 2 + 4] = " " + str(x + 1) + " "
            blueprint[0][x * 2 + 4 + len(player['board']) * 2 + 3 + board_spacing] = " " + str(x + 1) + " "
        else:
            blueprint[0][x * 2 + 4] = " " + str(x + 1)
            blueprint[0][x * 2 + 4 + len(player['board']) * 2 + 3 + board_spacing] = " " + str(x + 1)

    # Row Letter on both boards
    for y in range(len(player['board'])):
        blueprint[y * 2 + 3][1] = " " + chr(65 + y) + " "
        blueprint[y * 2 + 3][x * 2 + 6 + board_spacing] = " " + chr(65 + y) + " "

    # Filling in the walls for both boards
    # First board has 2 < x < length of the original board *2 + 4 because of the walls, empty left border and lettering
    # Second board start at x = length of the original board *2 + 4 + the spacing between the boards
    # and ends at x = the width of the full blueprint

    for y in range(blueprint_height):
        for x in range(blueprint_width):
            # Filling in the vertical walls for both boards. They all have odd x coordinate
            if x % 2 == 1 and ((2 < x < (len(player['board']) * 2 + 4)) or (
                    (len(player['board']) * 2 + 4 + board_spacing) < x < blueprint_width)):
                blueprint[y][x] = "│"

            # Filling in the horizontal walls. They all have even y coordinate
            if y > 1 and y % 2 == 0 and (0 < x < (len(player['board']) * 2 + 4) or (
                    len(player['board']) * 2 + 3 + board_spacing < x < blueprint_width - 1)):
                blueprint[y][x] = "───"

            # Filling in the cross section of the walls
            if y > 1 and y % 2 == 0 and x % 2 == 1 and ((2 < x < (len(player['board']) * 2 + 3)) or (
                    (len(player['board']) * 2 + 5 + board_spacing) < x < blueprint_width)):
                blueprint[y][x] = "┼"

            # Cleaning up the right most wall on both boards
            if y > 1 and y % 2 == 0 and (x == (len(player['board']) * 2 + 3) or x == blueprint_width - 1):
                blueprint[y][x] = "┤"

            # Cleaning up the lowest wall on both boards
            if y == blueprint_height - 1 and x % 2 == 1 and ((2 < x < (len(player['board']) * 2 + 3)) or (
                    (len(player['board']) * 2 + 5 + board_spacing) < x < blueprint_width)):
                blueprint[y][x] = "┴"

            # Putting the corner on both boards
            if y == blueprint_height - 1 and (x == (len(player['board']) * 2 + 3) or x == blueprint_width - 1):
                blueprint[y][x] = "┘"

    # Joins two ship pieces if they belong to the same ship
    for y in range(blueprint_height):
        for x in range(blueprint_width):
            if y % 2 == 0 and (2 < y < blueprint_height - 2) and x % 2 == 0 and (
                    (2 < x < (len(player['board']) * 2 + 3)) or (
                    (len(player['board']) * 2 + 5 + board_spacing) < x < blueprint_width)):

                if blueprint[y - 1][x][0:3] == blueprint[y + 1][x][0:3] and blueprint[y - 1][x] != "0" and \
                        blueprint[y - 1][x] != "WG" and blueprint[y - 1][x] != "CG":

                    if "H" in blueprint[y - 1][x] and "H" in blueprint[y + 1][x]:
                        blueprint[y][x] = "▒▒▒"
                    else:
                        blueprint[y][x] = "███"

            if y % 2 == 1 and (2 < y < blueprint_height - 1) and x % 2 == 1 and (
                    (2 < x < (len(player['board']) * 2 + 3)) or (
                    (len(player['board']) * 2 + 5 + board_spacing) < x < blueprint_width - 1 and y > 1)):

                if (blueprint[y][x - 1][0:3] == blueprint[y][x + 1][0:3]
                        and blueprint[y][x - 1] != "0"
                        and blueprint[y][x - 1] != "WG"
                        and blueprint[y][x - 1] != "CG"):

                    if "H" in blueprint[y][x + 1] and "H" in blueprint[y][x - 1]:
                        blueprint[y][x] = "▒"
                    else:
                        blueprint[y][x] = "█"

    # Replaces the ships names with the symbolic form to be printed
    for y in range(len(player['board'])):
        for x in range(len(player['board'][0])):
            blueprint[y * 2 + 3][x * 2 + 4] = field_filling(player['board'][y][x])

    # Replaces the guesses names with the symbolic form to be printed
    for y in range(len(player['guesses'])):
        for x in range(len(player['guesses'][0])):
            blueprint[y * 2 + 3][x * 2 + 4 + len(player['board']) * 2 + 3 + board_spacing] = field_filling(
                player['guesses'][y][x])

    return blueprint


def draw_boards(player, language):
    # Titles of the boards
    header_1 = language['your_board']
    header_2 = language['your_enemys_board']
    sub_header = language['how_many_ships_left']

    # Spacing between the two boards depended on title length
    board_spacing = 5  # Has to be an odd number
    final_spacing = " " * int(board_spacing + ((board_spacing + 1) / 2) * 2)
    header_1_spacing = " " * (len(player['board'][0]) * 4 - len(header_1))
    sub_header_spacing = " " * (len(player['board'][0]) * 4 - len(sub_header) - 1)

    # Create a blueprint to be printed
    blueprint = boards_to_blueprint(player, board_spacing)

    # Print the titles and Sub-headers

    menu.clear_screen()
    print(f"   {player['name']} {language['is_playing']}:\n"
          f"        {header_1}{header_1_spacing}{final_spacing}       {header_2}\n"
          f"        {sub_header}{player['ships_left']}{sub_header_spacing}{final_spacing}       {sub_header}{player['enemy_ships_left']}\n\n")

    # Print the boards
    for y in blueprint:
        for x in y:
            print(f"{x}", end="")
        print("\n", end="")
