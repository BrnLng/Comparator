class Comparator:

    def __init__(self, *args):
        if args:
            print(args)
            if isinstance(args[0], list):
                print("is list")
            else:
                pass  # TODO: check if it is a list found partially done etc. useful for above part too

        if self.is_list_empty():
            self._new()
        else:
            self._continue()

    def is_list_empty(self):
        print("checking")
        return False

    def _new(self):
        print("new")

    def _continue(self):
        print("continue")


if __name__ == '__main__':
    comparator = Comparator(1, 2, "asas")
