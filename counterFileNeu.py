import threading
import time
import os

global my_input
global flag


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
    if len(my_input > 0):
        flag = True
    else:
        False

    # exit(exit_message)
    return my_input


def exit(msg):
    """
    Exit function, prints something and then exits using OS
    Please note you cannot use sys.exit when threading..
    You need to use os._exit instead
    """
    print(msg)
    # os._exit(1)


def close_if_time_pass(seconds):
    """
    Threading function, after N seconds print something and exit program
    """
    time.sleep(seconds)


bol = flag
if bol == False:
    pass

"""
Threading function, after N seconds print something and exit program

    time.sleep(seconds)
    exit("\nDeine Zeit ist abgelaufen. Es wurde ein zufälliges Feld beschossen")"""


def main():
    # define close_if_time_pass as a threading function, 15 as an argument
    t = threading.Thread(target=close_if_time_pass, args=(15,))
    # start threading
    t.start()
    # ask for input
    ask()


def ret_value():
    return my_input

# if __name__ == "__main__":
# main()
