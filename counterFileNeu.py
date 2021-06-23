import threading
import time
import menu

# bool variable to signal the start.
start_sign = False

# int variable that shows the current time for the timer.
global when_to_stop

# str variable that stores user input from ask() function. It is global so that it can be compared in other functions.
my_input = ""

# bool var to signal the end of process.
check = False


def ask():
    """
    Simple function where you ask for input, if he answers
    you print message and exit
    """

    global my_input

    my_input = input().upper()

    if len(my_input) > 0:
        exit_message = "Du hast auf das Feld %s geschossen" % my_input
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
    global when_to_stop, my_input, check

    # Conditions are true if time is up and there was no user input
    if when_to_stop <= 1 and len(my_input) < 1 and check == False:
        menu.clear_screen()
        exit(
            "\n  Deine Zeit ist abgelaufen. Es wurde ein zufälliges Feld beschossen\n  Drück die Enter-Taste um fortzufahren")


def countdown():
    global start_sign, when_to_stop

    # countdown start at 15 sec and goes down (-2) ever 2 sec
    when_to_stop = 15

    # countdown starts if time greater than 0 and start sign is true
    while when_to_stop >= 0 and start_sign == True:
        m, s = divmod(when_to_stop, 60)
        time_left = str(m).zfill(2) + ":" + str(s).zfill(2)
        print("\r  Deine Zeit: " + time_left + " ||| Deine Eingabe: ", end="")

        # if current time is greater than 1, time goes down (-2) every 2 sec
        if when_to_stop > 1:
            if when_to_stop % 2:
                time.sleep(2)
                when_to_stop -= 2

        # if current time is equal to 1, time goes down (-1) and ends the loop
        elif when_to_stop == 1:
            time.sleep(1)
            when_to_stop -= 1
            break


def main(max):
    # print("\n\n\n\n")
    import game_functions
    global start_sign, check

    # bool variables that are needed to start
    start_sign = True
    check = False

    # define close_if_time_pass as a threading function, 15 as an argument
    t = threading.Thread(target=close_if_time_pass, args=(15,))
    t2 = threading.Thread(target=countdown)

    # start threading
    t2.start()
    t.start()

    # ask for input
    user_input = ask()

    # if there was no user input, the player will attack a random field automatically
    if len(user_input) < 1:
        user_input = game_functions.random_ship_attac(max)

    # bool variables that are needed to stop
    check = True
    start_sign = False

    return user_input
