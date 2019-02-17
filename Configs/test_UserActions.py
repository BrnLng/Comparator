from unittest import TestCase
from Configs.UserActions import possible_answers


class TestUserActions(TestCase):

    def test_answers_collision(self):

        all_answers = []
        answers_block = possible_answers.values()

        for block in answers_block:
            for answer in block:
                all_answers.append(answer)

        answers_set = list(set(all_answers))

        all_answers.sort()
        answers_set.sort()

        # self.assertRaises(Exception,s.demo,2,1,2)
        self.assertEquals(all_answers, answers_set)
