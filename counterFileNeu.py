import sys
import threading
import time
import os

flag = False
user_input = "EMPTY"
stopp_sign = False
start_sign = False


def ask():
    """
    Simple function where you ask for input, if he answers
    you print message and exit
    """

    global flag
    global stopp_sign

    my_input = input().upper()

    exit_message = "Du hast auf das Feld %s geschossen" % my_input
    flag = True

    exit(exit_message)

    if my_input != "EMPTY":
        stopp_sign = True

    return my_input


def exit(msg):
    ### lies unteren Kommentar
    """
    Exit function, prints something and then exits using OS
    Please note you cannot use sys.exit when threading..
    You need to use os._exit instead
    """

    print(msg)

    """Mit der Funktion os._exit wird das gesamte Programm beendet und nicht nur der eine Prozess
    Ich lasse es erst mal auskommentiert, bis wir eine gute Lösung dafür haben"""
    # os._exit(1)


def close_if_time_pass(seconds):
    """
    Threading function, after N seconds print something and exit program
    """

    time.sleep(seconds)
    global flag, stopp_sign
    stopp_sign = True

    exit(
        "\nDeine Zeit ist abgelaufen. Es wurde ein zufälliges Felb beschossen\nDrück die Enter-Taste um fortzufahren")


# counterfunktion die noch eingabaut werden muss
# ab t.start() in der main Funktion oben, muss der counter loslaufen
import time

flag = False


def countdown():
    global start_sign
    when_to_stop = 15
    stopp_sign = False
    print(when_to_stop)
    while when_to_stop > 0 and start_sign == True:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print("\rDeine Zeit: " + time_left + " ||| Deine Eingabe: ", end="")

        time.sleep(1)
        when_to_stop -= 1

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
    '''t.join()
    t2.join()'''

    # ask for input
    global user_input
    user_input = ask().upper()

    if len(user_input) < 1:
        user_input = game_functions.random_ship_attac(max)
    # t.join(0.1)
    # t2.join(0.1)
    print(t.is_alive())
    print(t2.is_alive())
    # t._stop()
    # t2._stop()
    start_sign = False

    return user_input

# main()
