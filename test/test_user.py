from unittest import TestCase

from amsta.User import User


class TestUser(TestCase):
    def test_get_userid(self):
        user = User(1, "Jaap", "stam")
        self.assertEqual(1, user.get_userid())

    def test_get_first_name(self):
        user = User(1, "Jaap", "stam")
        self.assertEqual("Jaap", user.get_first_name())

    # testing if you get 10 users back in the list
    def test_get_highest_ranking_users(self):
        expected = 10
        self.assertEqual(expected, len(User.get_highest_ranking_users(10)))

    # testing if you get the right amount of points back
    def test_get_points(self):
        user = User(593488253213, "Jaap", "stam")
        expected = 40
        self.assertEqual(expected, User.get_points(user))
