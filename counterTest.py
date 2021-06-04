import threading
import time
import os


def ask():
    """
    Simple function where you ask for input, if he answers
    you print message and exit
    """
    name = input("Gib ein Feld an, auf das geschossen werden soll: ")
    exit_message = "Du hast auf das Feld %s geschossen" % name
    exit(exit_message)


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
    exit("\nDeine Zeit ist abgelaufen. Es wurde ein zufälliges Felb beschossen")


def main():
    # define close_if_time_pass as a threading function, 15 as an argument
    t = threading.Thread(target=close_if_time_pass, args=(15,))
    # start threading
    t.start()
    # ask for input
    ask()


if __name__ == "__main__":
    main()

