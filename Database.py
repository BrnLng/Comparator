import os
from Configs.UserActions import userActions, possible_answers
from Configs.config import file_ending
from Comparing import *  # TODO: implement coupling


class Database:
    """ will try and use instead of Singleton later TODO: test singleton-ability
    (i.e. cancel singleton and check multi thread)x(i.e.python module are already singletons. read it somewhere.)

    open text format 4 data + hash checkable
    mainly lists:
    one line per item (pseudo newLines allowed with ' ++ ')
    each list consists of -raw and -ord pair for unordered (+= new items) and ordered ~= linked list from 1st to last
    each file is saved with a hash beside it ex. list-raw-hash, if contents won't relate, show option to re-hash
      (accept outside changes) or reload backup
    total: some 6 files per list (not counting axis and 1x1 table)

    important: sometimes the time it takes to precisely pidgen-hole each item is not available, so it also needs
    to make available option to put many items together at a 'basket group of sorts' (i.e. ***-)
    or simply to equally like stuff at ***** lvl for example.
    """

    wall_left, wall_right = 0, 1
    cursor = 0  # tracking where it is at
    moving_direction = userActions.ERROR
    step_multiplier = 0.27

    current_list_file = "DB/testListA"  # TODO: make less hacky self.current_list_file

    def __init__(self, new_list=None, partial_ordered_list=None):
        # self.current_list_file = self._load_file_option() if new_list is None else new_list
        self.current_unordered_list = self.set_current_list() if new_list is None else new_list
        self.current_ordered_list = [] if partial_ordered_list is None else partial_ordered_list
        self.ordered_equals_list = {}  # TODO: partial_load also?

    def get_current_list(self):
        return self.current_unordered_list

    def set_current_list(self):
        items = []
        try:
            with open(self.current_list_file + file_ending.RAW, 'r', encoding='utf-8') as f:
                for item in f.readlines():
                    items.append(item.rstrip('\n'))
                f.close()
            #                         {''} == set([''])
            items = list(set(items) - {''})  # normalizing list by first cleaning new lines with set functionality

            # check if initial backup exists, then create one if not and leave it untouched ever after
            if not os.access(self.current_list_file + file_ending.RAWB, os.R_OK):
                try:
                    with open(self.current_list_file + file_ending.RAWB, 'w', encoding='utf-8') as fbkp:
                        output = "\n".join(items)
                        fbkp.write(output)
                except IOError as e:
                    print(e)

            return items

        except IOError as e:
            print(e)  # TODO: totally new run: create list or batch read, move file etc.

    def _is_new_list(self):
        if self.current_ordered_list.__len__() > 0:
            return False
        try:
            with open(self.current_list_file + file_ending.ORD, 'r', encoding='utf-8') as f:
                if f.seek(4):
                    return True
                f.close()
            return False
        except (IOError, EOFError) as e:
            # print(e)  # list will be created elsewhere
            return True

    def sanitize_parameters(self, method='default'):
        """ this deals with moving walls and mostly to check if everything is ok,
        or if it's the first choices of a new list (initial setup) etc.
        also used for restoring state at reloading etc. """
        if self._is_new_list():
            return  # TODO: maybe call restore state in here ?
        else:
            # print('in "', method, end='" sanitize. ')
            if method.lower() == 'default':  # TODO: CURRENTLY DOING IT TO MAKE IT WORK, no other place uses CURSOR

                if self.moving_direction == userActions.LEFT_TO:
                    self.wall_left, self.wall_right = self.wall_left, self.cursor
                    # self.cursor *= self.step_multiplier
                elif self.moving_direction == userActions.RIGHT_TO:
                    self.wall_left, self.wall_right = self.cursor, self.wall_right
                    # self.cursor *= (1 + self.step_multiplier)
                else:
                    pass
                # self.cursor = int(self.cursor)
                self._get_item_at_position()

            elif method.lower() in ['full', 'init']:
                self.wall_left, self.wall_right = 0, self.current_ordered_list.__len__()
            else:
                print("New entry type or Error on sanitize_parameters() call")
                # self.wall_left, self.wall_right = -1, 0  # TODO: no use? Error? wtf?
                self.wall_left, self.wall_right = 0, self.current_ordered_list.__len__()
                # raise Exception
        print('sanitizing or not: ', self.wall_left, self.cursor, self.wall_right)

    def has_no_walls_space(self):
        # print('has_walls_space? = ', self.wall_right - self.wall_left)
        if (self.wall_right - self.wall_left) <= 1:
            return True
        return False

    def _get_item_at_position(self, position=step_multiplier):
        walled_space = self.wall_right - self.wall_left
        walled_aiming = walled_space * position
        walled_aiming += self.wall_left
        get_pos = int(walled_aiming)
        # get_pos = int(position * self.current_ordered_list.__len__())
        item = self.current_ordered_list[get_pos]
        # self.cursor = pos
        return item

    def get_current_items(self):
        """ items = moving, against """
        if self._is_new_list():
            base_item = self.current_unordered_list.pop()
            self.current_ordered_list.append(base_item)  # initial position
            return self.current_unordered_list.pop(), base_item
        else:
            print(self.current_unordered_list, ' <-ToDo ; N/item-> ', self._get_item_at_position(),
                  self.current_ordered_list)
            return self.current_unordered_list.pop(), self._get_item_at_position()

    def still_has_work_todo(self):
        return self.current_unordered_list.__len__() > 0

    def user_choice_check(self, answer):
        """ check and return based on enum @ UserActions.py """
        # if answer in possible_answers.values(): return userActions[key]  # TODO: try something expansible like this
        if answer in possible_answers[userActions.LEFT_TO]:
            # print('<-')
            return userActions.LEFT_TO
        elif answer in possible_answers[userActions.RIGHT_TO]:
            # print('+>')
            return userActions.RIGHT_TO
        elif answer in possible_answers[userActions.EQUAL_TO]:
            # print('<=> (auto group @ level ...ask?)')  # TODO: ask level identifier (~=axis) or auto group possible?
            return userActions.EQUAL_TO
        elif answer in possible_answers[userActions.DELETE]:
            # print('entry will be trashed (recoverable)')
            return userActions.DELETE
        elif answer in possible_answers[userActions.DUPLICATED]:
            # print('entry will be archived (as duplication and equal)')
            return userActions.DUPLICATED
        elif answer in possible_answers[userActions.GROUP]:
            # print('entry will be tagged and may or not be ranked now')
            return userActions.GROUP
        elif answer in possible_answers[userActions.QUIT]:
            return userActions.QUIT
        else:
            return userActions.ERROR

    def group(self, group, items):
        for item in items:
            print(item + ' now in ' + group)

    def rank_item(self, item, pos, action):
        """ continues shuffling or reach walls and commit saving
        ALSO: Save at 1x1 table etc. """
        # TODO: save @ 1x1 table
        # print("in rank_item: ", item, pos, '>' if action == userActions.RIGHT_TO else '<', end='')
        if self.has_no_walls_space():
            # print('. no wall space, saving...', end='')
            self.current_ordered_list.insert(pos + 1 if action == userActions.RIGHT_TO else 0,
                                             item)  # TODO: deal when having more than one item -- NOT HERE? always 1
            # TODO: save DBComparison 1x1 here
            # self.sanitize_parameters(method='between')
        # else:
        self.sanitize_parameters()  # move walls span (halve or something) method='walls' / cursor / move
        # print('.')

    def index_most(self, direction, items_to_search):
        print(items_to_search, 'searched, "inserting(?)" ', 'left' if direction == userActions.LEFT_TO else 'right')
        print('over "', self._get_item_at_position(), '" current ordered list: ', self.current_ordered_list)
        if direction == userActions.LEFT_TO:
            left_most = self.current_ordered_list.index(items_to_search[0])
            if left_most < self.wall_left:
                return self.wall_left
            else:
                return left_most
        elif direction == userActions.RIGHT_TO:
            right_most = self.current_ordered_list.index(items_to_search[0])
            if right_most >= self.wall_right:
                return self.wall_right
            else:
                return right_most
        # return self.current_ordered_list.index(items_to_search[0])  # TODO: when items++, search right/left-most

    def proceed(self, process, items):
        """ this should call the main shuffling algorithm depending on answer given.
         OBS: grouping/tagging and quitting made @ Comparator.main ...all else here
         the main algorithm for putting things in rank order place """
        self.moving_direction = 0
        if process in (userActions.LEFT_TO, userActions.RIGHT_TO):
            self.moving_direction = process
            self.cursor = self.index_most(process, items[1:])  # TODO: currently HERE!
            self.rank_item(items[0], self.cursor, process)
        elif process == userActions.EQUAL_TO:
            print(items, 'UNDONE: first is equal to the other (must be only one)')
        # TODO: later:
        elif process == userActions.DUPLICATED:
            print(items, 'UNDONE: is to be equal to an other (must be only one) but also archived - invisible')
        elif process == userActions.DELETE:
            print(items, 'UNDONE: is to be trashed')  # do a trash file
        else:  # TODO: maybe unneeded
            print("Error @ Database.proceed func")

    def show_results(self):
        print("Results = waiting")  # TODO: show
