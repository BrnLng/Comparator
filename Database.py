from Configs.UserActions import userActions, possible_answers
from DB_Lists_text import FileDB


class Database:
    """ will try and use instead of Singleton later TODO: test singleton-ability
    (i.e. cancel singleton and check multi thread)x(i.e.python module are already singletons. read it somewhere.)

    open text format 4 data + hash checkable
    mainly lists:
    one line per item (pseudo newLines allowed with ' ++ ')
    each list consists of -raw and -ord pair for unordered (+= new items) and ordered ~= linked list from 1st to last
    each file is saved with a hash beside it ex. list-raw-hash, if contents won'texts relate, show option to re-hash
      (accept outside changes) or reload backup
    total: some 6 files per list (not counting axis and 1x1 table)

    important: sometimes the time it takes to precisely pidgen-hole each item is not available, so it also needs
    to make available option to put many items together at a 'basket group of sorts' (i.e. ***-)
    or simply to equally like stuff at ***** lvl for example.
    """

    # wall_left, wall_right = 0, 1
    # cursor = 0  # tracking where it is at
    # step_multiplier = 0.27

    def __init__(self, new_list=None, partial_ordered_list=None):
        # self.current_list_file = self._load_file_option() if new_list is None else new_list
        self.current_list_file = "DB/testListA"  # TODO: make less hacky self.current_list_file
        self.file_DB = FileDB()
        self.current_unordered_list = self.file_DB.set_current_list(self.current_list_file) \
            if new_list is None else new_list
        self.current_ordered_list = [] if partial_ordered_list is None else partial_ordered_list
        self.ordered_equals_list = {}  # TODO: partial_load also?
        self.user_action = userActions.ERROR

    def get_current_list(self):
        return self.current_unordered_list

    # def _is_new_list(self):
    #     if self.current_ordered_list.__len__() > 0:
    #         return False
    #     try:
    #         with open(self.current_list_file + file_ending.ORD, 'r', encoding='utf-8') as f:
    #             if f.seek(4):
    #                 return True
    #             f.close()
    #         return False
    #     except (IOError, EOFError) as e:
    #         # print(e)  # list will be created elsewhere
    #         return True

    # def has_no_walls_space(self):
    #     # print('has_walls_space? = ', self.wall_right - self.wall_left)
    #     if (self.wall_right - self.wall_left) <= 1:
    #         return True
    #     return False

    # def _get_item_at_position(self, position=step_multiplier):
    #     walled_space = self.wall_right - self.wall_left
    #     walled_aiming = walled_space * position
    #     walled_aiming += self.wall_left
    #     get_pos = int(walled_aiming)
    #     # get_pos = int(position * self.current_ordered_list.__len__())
    #     item = self.current_ordered_list[get_pos]
    #     # self.cursor = pos
    #     return item

    # def get_current_items(self):
    #     """ items = moving, against """
    #     if self._is_new_list():
    #         base_item = self.current_unordered_list.pop()
    #         self.current_ordered_list.append(base_item)  # initial position
    #         return self.current_unordered_list.pop(), base_item
    #     else:
    #         print(self.current_unordered_list, ' <-ToDo ; N/item-> ', self._get_item_at_position(),
    #               self.current_ordered_list)
    #         return self.current_unordered_list.pop(), self._get_item_at_position()

    def still_has_work_todo(self):
        return self.current_unordered_list.__len__() > 0

    def group(self, group, items):
        for item in items:
            print(item + ' now in ' + group)

    # def rank_item(self, item, pos, action):
    #     """ continues shuffling or reach walls and commit saving
    #     ALSO: Save at 1x1 table etc. """
    #     # TODO: save @ 1x1 table
    #     # print("in rank_item: ", item, pos, '>' if action == userActions.RIGHT_TO else '<', end='')
    #     if self.has_no_walls_space():
    #         # print('. no wall space, saving...', end='')
    #         self.current_ordered_list.insert(pos + 1 if action == userActions.RIGHT_TO else 0,
    #                                          item)  # TODO: deal when having more than one item -- NOT HERE? always 1
    #         # TODO: save DBComparison 1x1 here
    #         # self.sanitize_parameters(method='between')
    #     # else:
    #     self.sanitize_parameters()  # move walls span (halve or something) method='walls' / cursor / move
    #     # print('.')

    # def index_most(self, direction, items_to_search):
    #     print(items_to_search, 'searched, "inserting(?)" ', 'left' if direction == userActions.LEFT_TO else 'right')
    #     print('over "', self._get_item_at_position(), '" current ordered list: ', self.current_ordered_list)
    #     if direction == userActions.LEFT_TO:
    #         left_most = self.current_ordered_list.index(items_to_search[0])
    #         if left_most < self.wall_left:
    #             return self.wall_left
    #         else:
    #             return left_most
    #     elif direction == userActions.RIGHT_TO:
    #         right_most = self.current_ordered_list.index(items_to_search[0])
    #         if right_most >= self.wall_right:
    #             return self.wall_right
    #         else:
    #             return right_most
    #     # return self.current_ordered_list.index(items_to_search[0])  # TODO: when items++, search right/left-most

    def proceed(self, process, items):
        """ this should call the main shuffling algorithm depending on answer given.
         OBS: grouping/tagging and quitting made @ Comparator.main ...all else here
         the main algorithm for putting things in rank order place """
        self.user_action = 0
        if process in (userActions.LEFT_TO, userActions.RIGHT_TO):
            self.user_action = process
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
