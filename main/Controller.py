""" This is Controller of mvC """

from main.Singleton import Singleton
from main.Comparing import Comparing
from Configs.UserActions import userActions


class Controller(Singleton):

    def __init__(self, new_list=None, partial_ordered_list=None):
        """ first: prepare database. if not found: ask for first list
                    second: if work ongoing found: offer to continue or create new list (main options)
                    third, offer full options: continue, backup/import, manage and change lists, results or items and axis
                    +++
                    some behind the scene work , then present options and
                separate front-ends: tty/terminal/CLI or Kivy TODO: kivy front end """
        Singleton.__init__(self)  # keep Singleton functionality intact
        #  TODO: check -- may be unneeded if Database already acts as should

        self.database = Singleton.database()
        self.comparing = Comparing(new_list, partial_ordered_list)

        self.intellij_ways = True
        self.exit_sign = False
        self.user_input = None

        # def do_step(self):  # no need to separate from __init__
        if self.is_list_completed():
            self.__quit()

        self.user_input = userActions.ERROR  # always reset to avoid looping with first answer

        while self.user_input in (userActions.ERROR, userActions.GROUP):
            if self.user_input == userActions.GROUP:
                groups_available = None  # TODO: get groups list (trash in here too)
                if groups_available is None:
                    new_group = self.request_user_input_long('Enter new group (or tag) for item ' + self.moving)
                    self.database.group(new_group, [self.moving])
                else:
                    self.database.group(self.group_select(), [self.moving])

            while not self.comparing.exit_signed():
                self.present_work_step()

        if self.user_input == userActions.QUIT:
            self.__quit()
        else:
            self.comparing.do_step(type_='manual', answer=self.user_input)  # TODO: DOING NOW

    def present_work_step(self):
        print("at new place that should not be here")
        quit()

    def group_select(self):
        pass

    def is_list_completed(self):
        return False  # TODO: check if list is fully (or enough*) ranked. *maybe at another func?

    def __quit(self):
        self.exit_sign = True
        self.database.show_results()
        # exit()  # TODO: clean up and tidy database etc.
