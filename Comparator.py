""" this is both V & C (View and Controller) of Comparator MVC, Model is @ Database """
from Configs.internationalizable_texts import Texts

from Configs.UserActions import userActions, possible_answers
from Singleton import Singleton
from multiOsHelpers.get_user_input import *


class Comparator(Singleton):
    """    Comparator serves a user with a process to order and/or rank a list of items
    User/front-end: I/O on rank per item compared
    User options: I/O item @ work + manage lists, items and axis + get / backup data and results
    Main process: compare item and find its place in rank order list (item@work + current_list)
        OR(/and): separate items according to different axis (grouping)
    Back end: serve lists, save results @ ordered list + one-on-one table DB, manage options
    Data: Lists, items and 1x1 DB (+ ordered [/axis] results)
    IDEAS / TODO: 5-star ***** output etc.
      5-star system ~= bell OR power OR sigmoid curve (depending on user?)
      5-star += hate {0} & super love OR new super (S2^3 // *6)
    OBS: think it needs to be a singleton, because of DB/data... or a Borg as seen here:
      https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

      TODO: log from gKeep: * make in between wall moving edit like form unnacepted review html...
                send and keep current state until accepted
        * edit item @ base (late item edit)
        * review equals [ @ top ranked only ? ]
    """

    intellij_ways = True
    exit_sign = False
    t = Texts()  # also: 'English' (default), 'pt-br'
    moving, against = None, None
    user_input = None

    def __init__(self, new_list=None, partial_ordered_list=None):
        """ first: prepare database. if not found: ask for first list
            second: if work ongoing found: offer to continue or create new list (main options)
            third, offer full options: continue, backup/import, manage and change lists, results or items and axis """
        Singleton.__init__(self)  # keep Singleton functionality intact
        #  TODO: check -- may be unneeded if Database already acts as should

        self.database = Singleton.database(new_list, partial_ordered_list)
        self.database.sanitize_parameters(method='init')  # unnecessary?
        # self.new_list_options()  # TODO: if user wants instead of step-ping in

    def new_list_options(self):
        """ offer to batch load txt files, present preview and confirmation...
        each item may be trashed or found as duplication on this stage already """
        pass

    def do_step(self):
        """ some behind the scene work , then present options and
        separate front-ends: tty/terminal/CLI or kivy TODO: kivy front end """
        if self.list_completed():
            self.__quit()  # TODO: maybe better to present options to new list, view results etc.

        # while True:  # this loop is for nailing down rank order in between moving walls TODO: belongs inside Database

        # self.database.sanitize_parameters()  # now at rank's end
        # if not self.database.has_no_walls_space():
        #     print('no? wall space reached!')
        #     return
        # else:
        self.user_input = userActions.ERROR  # always reset to avoid looping with first answer
        if self.database.still_has_work_todo():
            self.moving, self.against = self.database.get_current_items()
        else:
            self.__quit()  # or TODO: present options

        while self.user_input in (userActions.ERROR, userActions.GROUP):
            if self.user_input == userActions.GROUP:
                groups_available = None  # TODO: get list
                if groups_available is None:
                    new_group = self.request_user_input_long('Enter new group (or tag) for item ' + self.moving)
                    self.database.group(new_group, [self.moving])
                else:
                    self.database.group(self.group_select(), [self.moving])

            self.present_work_step()

        if self.user_input == userActions.QUIT:
            self.__quit()
        else:
            self.database.proceed(self.user_input, [self.moving, self.against])

        # print(self.t.put('COMMAND', self.user_input))

        self.database.sanitize_parameters(method='Full')

    def present_work_step(self):
        """ present options for user to
        compare or group in (new or already used) axis
        normal option: single moving x against single
        TODO: multiple x multiple (~= puzzle move) """
        if self.intellij_ways:
            # print(f"(-<) {self.moving} << {self.against} >> {self.moving} (>+) ", end='')  # must be comm if py 3.4-
            pass
        else:
            print("(-<) {0} << {1} >> {0} (>+)".format(self.moving, self.against))
        answer = self.database.user_choice_check(self.request_user_input())
        # if answer in (userActions.LEFT_TO, userActions.RIGHT_TO, userActions.EQUAL_TO):
        #     print(self.t.put('MOVE'))
        # elif answer in (userActions.DELETE, userActions.DUPLICATED):
        #     print(self.t.put('TRASH'))
        # elif answer == userActions.GROUP:
        #     print(self.t.put('GROUP'))
        # elif answer == userActions.QUIT:
        #     print(self.t.put('QUIT'))
        # else:
        #     if answer == userActions.ERROR:
        #         print(self.t.put('IERROR'))
        #         for k, v in possible_answers.items():
        #             print("{:>10}: {}".format(self.t.put('COMMAND', k).lower().capitalize(), v))
        #     else:
        #         print(self.t.put('WERROR') + str(answer) + "]")
        if answer == userActions.ERROR:
            print(self.t.put('IERROR'))
            for k, v in possible_answers.items():
                print("{:>10}: {}".format(self.t.put('COMMAND', k).lower().capitalize(), v))
        self.user_input = answer

    def request_user_input(self):
        """ if intellij: direction keys &all treated @ multiOSHelpers/get_char() & * """
        if self.intellij_ways:
            answer = get_char()
        else:
            answer = get_char_normal_input()
        return answer

    def request_user_input_long(self, prompt=''):
        return input(prompt)

    def group_select(self):
        pass

    def list_completed(self):
        return False  # TODO: check if list is fully (or enough*) ranked. *maybe at another func?

    def exit_signed(self):
        return self.exit_sign

    def __quit(self):
        self.exit_sign = True
        self.database.show_results()
        # exit()  # TODO: clean up and tidy database etc.


if __name__ == '__main__':
    # print(Comparator() is Comparator())  # DEBUG, must equal because of Singleton
    comparator = Comparator(['8', '4', '7', '5', '2', '0'], ['1', '3', '6', '9'])
    while True:
        comparator.do_step()
        if comparator.exit_signed():
            break  # TODO: missing… <- /lock trash zone etc. -> + ver gKeep
