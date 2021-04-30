import game_functions

board_size = 10

player_1 = {"name": "John"}
player_1["board"] = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["S", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["S", "0", "S", "S", "0", "S", "S", "S", "0", "0"],
                     ["S", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "S", "S", "S", "S", "S", "S", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "0", "WG", "0", "0", "0", "0", "0"],
                     ["0", "0", "0", "S", "HS", "S", "S", "0", "0", "0"]
                     ]
player_1["guesses"] = [["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "CG", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "CG", "WG", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "0", "WG", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "WG", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "WG", "0", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                       ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
                       ]

possible_input = []
for y in range(board_size):
    for x in range(board_size):
        possible_input.append(chr(65 + y) + str(x + 1))
print(possible_input)
game_functions.ask_input_from(player_1, possible_input)
