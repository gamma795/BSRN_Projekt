# Diese Funktion greift ein zufälliges Schiff an
def random_ship_attac(max):
    from random import randint
    # max ist das äußere Ende des Spielfeldes z.B 10 * 10
    # Zufällige int Werte
    y = randint(1, max)
    x = randint(1, max)

    # Umwandeln von int zu einem Buchstaben für 'Y'
    y = chr(y + 64)

    # Output bestehend aus Buchstabe und Zahla
    output = y + str(x)
    print(output)
    return output
