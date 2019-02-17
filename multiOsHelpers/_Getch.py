#seems to not be working properly

class _Getch:
    """Gets a single character from standard input. Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        # def readch(echo=True):
        "Get a single character on Windows."
        # while msvcrt.kbhit():  # clear out keyboard buffer
        #     ch = msvcrt.getch()
        #     if ch in '\x00\xe0':  # arrow or function key prefix?
        #         ch = msvcrt.getch()  # second call returns the actual key code
        ch = msvcrt.getch()
        if ch in '\x00\xe0':  # arrow or function key prefix?
            ch = msvcrt.getch()  # second call returns the actual key code
        # if echo:
        #     msvcrt.putch(ch)
        return 'x'  # ch

        # return msvcrt.getch()
