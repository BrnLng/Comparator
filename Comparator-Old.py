""" this is View of Comparator mVc """
from Configs.internationalizable_texts import Texts
from Configs.UserActions import userActions, possible_answers
from multiOsHelpers.get_user_input import *
from main.Controller import Controller


class ComparatorViewer:
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
    """

    def __init__(self, new_list=None, partial_ordered_list=None):
        self.controller = Controller(new_list, partial_ordered_list)
        self.texts = Texts()  # also: 'English' (default), 'pt-br'
        self.user_input = userActions.ERROR

    def present_work_step(self):
        """ present options for user to
        compare or group in (new or already used) axis
        normal option: single moving x against single
        TODO: multiple x multiple (~= puzzle move) """
        print("(-<) {0} << {1} >> {0} (>+)".format(
            self.comparing.item_moving(), self.comparing.item_against()), end='')
        answer = self.user_choice_check(self.request_user_input())
        # if answer in (userActions.LEFT_TO, userActions.RIGHT_TO, userActions.EQUAL_TO):
        #     print(self.texts.put('MOVE'))
        # elif answer in (userActions.DELETE, userActions.DUPLICATED):
        #     print(self.texts.put('TRASH'))
        # elif answer == userActions.GROUP:
        #     print(self.texts.put('GROUP'))
        # elif answer == userActions.QUIT:
        #     print(self.texts.put('QUIT'))
        # else:
        #     if answer == userActions.ERROR:
        #         print(self.texts.put('IERROR'))
        #         for k, v in possible_answers.items():
        #             print("{:>10}: {}".format(self.texts.put('COMMAND', k).lower().capitalize(), v))
        #     else:
        #         print(self.texts.put('WERROR') + str(answer) + "]")
        if answer == userActions.ERROR:
            print(self.texts.put('IERROR'))
            for k, v in possible_answers.items():
                print("{:>10}: {}".format(self.texts.put('COMMAND', k).lower().capitalize(), v))
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

    def user_choice_check(self, answer=None):
        """ check and return based on enum @ UserActions.py """
        # if answer in possible_answers.values(): return userActions[key]  # TODO: try something expansible like this
        if answer is None:
            answer = self.user_input
        if answer in possible_answers[userActions.LEFT_TO]:
            print('<-')
            return userActions.LEFT_TO
        elif answer in possible_answers[userActions.RIGHT_TO]:
            print('+>')
            return userActions.RIGHT_TO
        elif answer in possible_answers[userActions.EQUAL_TO]:
            print('<=> (auto group @ level ...ask?)')  # TODO: ask level identifier (~=axis) or auto group possible?
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

    def new_list_options(self):
        """ offer to batch load txt files, present preview and confirmation...
        each item may be trashed or found as duplication on this stage already """
        pass

    def get_1x1_db(self):
        return self.comparing.get_1x1_db()

    def exit_signed(self):
        return self.exit_sign


if __name__ == '__main__':
    # print(Comparator() is Comparator())  # DEBUG, must equal because of Singleton
    to_do_list = ['8', '4', '7', '5', '2', '0']
    done_list = ['1', '3', '6', '9']
    comparator = ComparatorViewer(to_do_list, done_list)
    print("Ranked: ", done_list)
    print(comparator.get_1x1_db())  # TODO: missing… <- /lock trash zone etc. -> + ver gKeep
