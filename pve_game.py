import random
import menu
import game_functions


def launch(player_1, player_2, settings_values, language):
    menu.clear_screen()
    print("Mensch gegen Maschine!\n")
    player_1["name"] = str(input("Wie wollen Sie heiße: "))
    bot_name = ["Silly", "Bad", "Idiot", "Donkey", "Shitty"]
    player_2["name"] = random.choice(bot_name) + " Bot"
    menu.clear_screen()
    print(
        f"Willkommen, {player_1.get('name')} ! Du spielst heute gegen ein {player_2.get('name')}")
    print("Möge die Schlacht beginnen!\n")
