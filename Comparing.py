from multiOsHelpers.get_user_input import *
from Configs.UserActions import userActions

# TODO: make a stand-alone module, than plug it into Database


class Comparing:
    """ will be used @ Database to decouple this ranking part algorithm  TODO: will enable unittests """

    def __init__(self, list_working=None, list_organized=None):
        self._quit_signal = False
        self._hint_displayed = False
        self._print_hints = True  # TODO: check if is still needed
        self._is_at_same_step = False
        self._pooled = False  # if walls reached
        self._position_bias = 0.36
        self._cursor = 0
        self._answer = userActions.ERROR
        self.wall_left, self.wall_right = 0, 0

        self.list_unordered = [] if list_working is None else list_working
        self.list_ordered = [] if list_organized is None else list_organized
        self.walls_reset()

    # def __repr__(self):
    #     return " Still to rank: " + str(self.list_unordered) + "…\nAlready ranked: " + \
    #            str(self.list_ordered)

    def walls_reset(self):
        self.wall_left, self.wall_right = 0, len(self.list_ordered) - 1

    def do_step(self):
        self._pooled = False
        if self.is_list_finished():
            self._quit_signal = True
        else:
            while not self._pooled:
                self.get_response()
                self.rank()
                self._is_at_same_step = False
            return self.list_unordered, self.list_ordered

    def has_wall_space(self):
        """ True if cursor has travel space or else False """
        bool_response = False if (self.wall_right - self.wall_left) <= 1 else True  # TODO: check +1 keep?
        bool_response = False if self._answer == userActions.LEFT_TO and self.cursor() <= self.wall_left + 1 \
            else bool_response
        bool_response = False if self._answer == userActions.RIGHT_TO and self.cursor() >= self.wall_right \
            else bool_response
        return bool_response

    def cursor(self, position_override=-1):
        if self._is_at_same_step:
            return self._cursor
        else:
            if position_override < 0:
                position_override = 1 if self._answer == userActions.RIGHT_TO else 0 - self._position_bias
            new_cursor_position = int((self.wall_right - self.wall_left) * position_override)
            new_cursor_position = 1 if new_cursor_position < 1 else new_cursor_position
            if self._answer == userActions.RIGHT_TO:
                if new_cursor_position <= self._cursor:
                    new_cursor_position += max(1, self._cursor)
            else:
                new_cursor_position -= max(1, self._cursor)
            self._cursor = new_cursor_position
            self._is_at_same_step = True
            return new_cursor_position

    def item_moving(self, pos=0, pop=False):
        if pop:
            if len(self.list_unordered) == 1:
                if self._print_hints:
                    print("Everything ranked! Quitting…")
                self._quit_signal = True
            return self.list_unordered.pop(pos)
        else:
            return self.list_unordered[pos]

    def item_against(self):
        try:
            return self.list_ordered[self.cursor()]
        except IndexError:
            return self.list_ordered[-1]

    def get_response(self):
        if not self._hint_displayed:
            print("SUPPORT VERSION: use ONLY a or * for answering <- or -> (* = anything else)")
            self._hint_displayed = True
        if self._print_hints:
            print(" (get_response) Wall left {:2}, cursor {:2},                              right wall {:2}".format(
                self.wall_left, self.cursor(), self.wall_right))
        print("(-<) {0} << {1} >> {0} (>+)".format(self.item_moving(), self.item_against()))
        self._answer = userActions.LEFT_TO if get_char_normal_input() == 'a' else userActions.RIGHT_TO

    def rank_item(self, position_modifier=0):
        self.list_ordered.insert(self.cursor() + position_modifier, self.item_moving(pop=True))
        if self._print_hints:
            print(">>item saved<<")

    def rank(self):
        """pseudoCodeVersion userChoice(bool isAOverB, itemA, itemB, fixedListWhereItemBIs)"""
        if self.has_wall_space():
            if self._answer == userActions.LEFT_TO:
                self.wall_right = self.cursor()
            elif self._answer == userActions.RIGHT_TO:
                self.wall_left = self.cursor()
        else:
            self.rank_item(1 if self._answer == userActions.RIGHT_TO else 0)
            self._pooled = True  # ball in the machine
            # saveDBComparison(etc)  # TODO: db comp 1x1 save and sanitize needed or decouple able?
            self.walls_reset()
        self.sanity_check()

    def sanity_check(self):
        if self._print_hints:
            print("(before sanity) Wall left {:2}, cursor {:2},                              right wall {:2}".format(
                self.wall_left, self.cursor(), self.wall_right))
        wall_space = self.wall_right - self.wall_left
        point_space = wall_space + self.wall_left
        if self._print_hints:
            print(" (after sanity) Wall left {:2}, cursor {:2}, pointSpace {:2}, wallSpace {:2}, "
                  "right wall {:2}".format(self.wall_left, self.cursor(), point_space, wall_space, self.wall_right))
        if point_space < self.wall_left or point_space > self.wall_right:
            print("(sanity error)")
            self._quit_signal = True

    def is_list_finished(self):
        if len(self.list_unordered) < 1:
            return True
        return False

    def exit_signed(self):
        return self._quit_signal

if __name__ == '__main__':
    to_do_list = ['8', '4', '7', '5', '2', '0']
    done_list = ['1', '3', '6', '9']
    comparator = Comparing(to_do_list, done_list)
    while True:  # TODO: make this loop totally internal to call
        if comparator.exit_signed():
            break
        print(" Still to rank: ", to_do_list, "…\nAlready ranked: ", done_list)
        to_do_list, done_list = comparator.do_step()
    print("Ranked: ", done_list)
