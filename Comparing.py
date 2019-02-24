from multiOsHelpers.get_user_input import *
from Configs.UserActions import userActions


class Comparing:
    """ will be used @ Database to decouple this ranking part algorithm  TODO: will enable unittests """

    def __init__(self, list_working=None, list_organized=None):
        self._quit_signal = False
        self._hint_displayed = False
        self._is_at_same_step = False
        self._pooled = False  # if walls reached
        # self._print_hints = True  # DONE: check if is still needed
        self._position_bias = 0.36
        self._cursor_cache = 0
        self._answer = userActions.ERROR
        self.wall_left, self.wall_right = 0, 0

        self.db_1x1 = {}
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
        bool_response = False if (self.wall_right - self.wall_left) <= 1 else True
        bool_response = False if self._answer == userActions.LEFT_TO and self.cursor() < self.wall_left + 1 \
            else bool_response
        bool_response = False if self._answer == userActions.RIGHT_TO and self.cursor() >= self.wall_right \
            else bool_response
        return bool_response

    def cursor(self, position_override=-1):
        if self._is_at_same_step:
            return self._cursor_cache
        else:
            if position_override < 0:
                position_override = 1 - self._position_bias if self._answer == userActions.RIGHT_TO \
                    else self._position_bias
            new_cursor_position = int((self.wall_right - self.wall_left) * position_override)
            new_cursor_position = 1 if new_cursor_position < 1 else new_cursor_position
            if self._answer == userActions.RIGHT_TO:
                if new_cursor_position <= self._cursor_cache:
                    new_cursor_position += max(1, self._cursor_cache)
                    if new_cursor_position > self.wall_right:
                        new_cursor_position = self.wall_right
            else:
                new_cursor_position -= max(1, self._cursor_cache)
                if new_cursor_position < self.wall_left:
                    new_cursor_position = self.wall_left
            self._cursor_cache = new_cursor_position
            self._is_at_same_step = True
            return new_cursor_position

    def item_moving(self, pos=0, pop=False):
        if pop:
            if len(self.list_unordered) == 1:
                # if self._print_hints:
                #     print("Everything ranked! Quitting…")
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
        item_moving, item_against = self.item_moving(), self.item_against()
        try:
            right_to_if_ranked_already = self.db_1x1[frozenset([item_moving, item_against])]
            self._answer = userActions.RIGHT_TO if right_to_if_ranked_already == item_moving else userActions.LEFT_TO
            # print("(answer already taken) ", self._answer, right_to_if_ranked_already)
        except KeyError:
            print("(-<) {0} << {1} >> {0} (>+)".format(item_moving, item_against))
            self._answer = userActions.LEFT_TO if get_char_normal_input() == 'a' else userActions.RIGHT_TO

    def rank_item(self, position_modifier=0):
        # if self._print_hints:
        #     print(">>item saved<<")
        item_to_save = self.item_moving(pop=True)
        self.list_ordered.insert(self.cursor() + position_modifier, item_to_save)

    def rank(self):
        """pseudoCodeVersion userChoice(bool isAOverB, itemA, itemB, fixedListWhereItemBIs)"""
        # saving only self._answer won't work because a set does not save order
        self.db_1x1[frozenset([self.item_moving(), self.list_ordered[self.cursor()]])] = \
            self.list_ordered[self.cursor()] if self._answer == userActions.LEFT_TO else self.item_moving()
        if self.has_wall_space():
            if self._answer == userActions.LEFT_TO:
                self.wall_right = self.cursor()
            elif self._answer == userActions.RIGHT_TO:
                self.wall_left = self.cursor()
        else:
            self.rank_item(1 if self._answer == userActions.RIGHT_TO else 0)
            self._pooled = True  # ball in the machine
            self.walls_reset()

    def get_1x1_db(self):
        return self.db_1x1

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
    while not comparator.exit_signed():
        # print(" Still to rank: ", to_do_list, "…\nAlready ranked: ", done_list)
        to_do_list, done_list = comparator.do_step()
    print("Ranked: ", done_list)
    print(comparator.get_1x1_db())
