import msvcrt


def get_char():
    """ return _Getch()  # not working because object is passed instead of function -- wtf?
     anyway, directly to end function as it is only temporary. Endpoint: Kivy front
     base, sub idea from: https://www.daniweb.com/programming/
       software-development/threads/228595/getting-an-input-from-arrow-keys
     """
    base = chr(ord(msvcrt.getch()))
    if base == '\xe0':
        sub = chr(ord(msvcrt.getch()))

        if sub == 'M':
            base = '>'
        elif sub == 'K':
            base = '<'
        # elif sub == 'H':
        #     key = 'UP_KEY'
        # elif sub == 'P':
        #     key = 'DOWN_KEY'

    return base  # chr(ord(msvcrt.getwch()))


def get_char_normal_input():
    """ alternative input because of old intellij, until updated """
    input_total = input()
    return input_total[:1]
