import sys
import threading
import time
import os

flag = False
user_input = "EMPTY"
stop_sign = False
start_sign = False


def ask():
    """
    Simple function where you ask for input, if he answers
    you print message and exit
    """

    global flag
    global stop_sign

    my_input = input().upper()

    exit_message = "Du hast auf das Feld %s geschossen" % my_input
    flag = True
    stop_sign = True

    exit(exit_message)

    return my_input


def exit(msg):
    """
    Exit function, prints something and then exits using OS
    Please note you cannot use sys.exit when threading..
    You need to use os._exit instead
    """

    print(msg)


def close_if_time_pass(seconds):
    """
    Threading function, after N seconds print something and exit program
    """

    time.sleep(seconds)
    global flag, stop_sign
    stop_sign = True

    exit(
        "\n  Deine Zeit ist abgelaufen. Es wurde ein zufälliges Feld beschossen\n  Drück die Enter-Taste um fortzufahren")


# counterfunktion die noch eingabaut werden muss
# ab t.start() in der main Funktion oben, muss der counter loslaufen
import time

flag = False


def countdown():
    global start_sign
    when_to_stop = 15
    stopp_sign = False

    while when_to_stop > 0 and start_sign == True:  # and stopp_sign != True:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print("\r  Deine Zeit: " + time_left + " ||| Deine Eingabe: ", end="")

        if when_to_stop % 2:
            time.sleep(2)
            when_to_stop -= 2

        if when_to_stop == -1:
            global flag
            flag = True
            break

        if stopp_sign == True:
            exit("Zeit abgelaufen")
            break


def main(max):
    print("\n\n\n\n")
    import game_functions
    global start_sign

    # define close_if_time_pass as a threading function, 15 as an argument
    t = threading.Thread(target=close_if_time_pass, args=(15,))
    t2 = threading.Thread(target=countdown)
    # start threading

    start_sign = True

    t2.start()
    t.start()

    # ask for input
    global user_input
    user_input = ask()

    if len(user_input) < 1:
        user_input = game_functions.random_ship_attac(max)

    start_sign = False

    return user_input



