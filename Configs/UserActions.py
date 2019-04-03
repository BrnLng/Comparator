""" userActions are 'ERROR', 'LEFT_TO', 'RIGHT_TO', 'EQUAL_TO', 'DELETE', 'DUPLICATED', 'GROUP' and 'QUIT'
 as of 2019.03.23 """

from multiOsHelpers.local_enum import enum
# from enum import Enum
# https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python & https://pythonspot.com/python-enum/
# TODO: maybe add: mk as (un)important for 1x1 table, maybe as a special subGROUP to not add much overhead


userActions = enum(ERROR=0, LEFT_TO=1, RIGHT_TO=2, EQUAL_TO=3, DELETE=4, DUPLICATED=5, GROUP=6, QUIT=7)

userActions_list = ['ERROR', 'LEFT_TO', 'RIGHT_TO', 'EQUAL_TO', 'DELETE', 'DUPLICATED', 'GROUP', 'QUIT']

# TODO: customizable + test
possible_answers = {
    userActions.LEFT_TO: [',', '<', 'a'],
    userActions.RIGHT_TO: ['.', '>', 'z', 's'],  # s because it is at right of a with QWERTY
    userActions.EQUAL_TO: ['=', 'l', 'e'],  # l because it is above < & >
    userActions.DELETE: ['x'],  # x for deletion
    userActions.DUPLICATED: ['d'],  # d for duplicate found, many = new axis / grouping
    userActions.GROUP: ['g', "+", "#", "@", "$", "%", "&", "*"],
    userActions.QUIT: ['q', 'w']  # s WAS for Save (and quit), as it implies auto saving
    }

# class UserActions(Enum):
#     LEFT_TO = 1
#     RIGHT_TO = 2
#     EQUAL_TO = 3
#     DELETE = 4
#     DUPLICATE = 5
#     NEW_GROUP = 6
