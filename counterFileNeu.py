import sys
import threading
import time
import os

my_input = "EMPTY"
flag = False
user_input = "EMPTY"


def ask():
    """
    Simple function where you ask for input, if he answers
    you print message and exit
    """
    print("Deine Zeit: ")

    global my_input
    global flag

    my_input = input("Gib ein Feld an, auf das geschossen werden soll: ")

    exit_message = "Du hast auf das Feld %s geschossen" % my_input
    flag = True

    exit(exit_message)

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
    #os._exit(1)





def close_if_time_pass(seconds):
    """
    Threading function, after N seconds print something and exit program
    """

    time.sleep(seconds)
    global flag
    if flag == False:
        exit(
            "\nDeine Zeit ist abgelaufen. Es wurde ein zufälliges Felb beschossen\nDrück die Enter-Taste um fortzufahren")


def main():
    # define close_if_time_pass as a threading function, 15 as an argument
    t = threading.Thread(target=close_if_time_pass, args=(5,))
    # start threading
    t.start()
    # ask for input
    global user_input
    user_input = ask().upper()
    print(t.is_alive())

    return user_input




#main()

print("Hallo")

flag = False


# counterfunktion die noch eingabaut werden muss
# ab t.start() in der main Funktion oben, muss der counter loslaufen
'''import time
def countdown():
    when_to_stop = 15
    while when_to_stop > 0:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print("\rDeine Zeit: " + time_left, end="")

        time.sleep(1)
        when_to_stop -= 1

        if when_to_stop == 0:
            global flag
            flag = True'''