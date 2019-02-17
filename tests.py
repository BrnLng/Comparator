# from Configs.UserActions import possible_answers
#
#
# all_answers = []
# answers_block = possible_answers.values()
#
# for block in answers_block:
#     for answer in block:
#         all_answers.append(answer)
#
# answers_set = list(set(all_answers))
#
# all_answers.sort()
# answers_set.sort()
#
# print(all_answers)
# print(answers_set)

import kivy
from kivy.app import App
from kivy.uix.button import Button

kivy.require('1.0.7')


class TestsApp(App):

    def build(self):
        # return a Button() as a root widget
        return Button(text='hello world')


if __name__ == '__main__':
    TestsApp().run()

# # from pprint import pprint
# # pprint(possible_answers)
# from UserActions import possible_answers, userActions_list
# # print(possible_answers.items())
# # enumerate
# for k, v in possible_answers.items():
#     print(userActions_list[k], v)
#     # print(userActions_list[k] + ': ' + v)

# from multiOsHelpers.local_enum import enum
#
# my_enum = enum(TEST=1, OK=2)
# print(my_enum.TEST)

# from enum import Enum
#
#
# class MyEnum(Enum):
#     TEST = 1
#     TESTED = 2
#     WTF = 3
#
# if __name__ == '__main__':
#     myEnum = MyEnum()
#     for enumerated in myEnum:
#         print(repr(enumerated) + ' ' + enumerated)


# from msvcrt import getch
#
# print("char: "+chr(ord(getch())))

# def test():
#     return "working"
#
# read_options = {
#     'CURRENT_FILE': test,
#     'BAR': 'doBar',
# }
#
# command = read_options["CURRENT_FILE"]
# current_list_file = command()
#
# print(current_list_file)

print("\nin tests.py", end='')
