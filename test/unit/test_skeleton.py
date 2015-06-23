import unittest
import skeleton.server

class TestBasics(unittest.TestCase):
    def test_two_times_three(self):
        self.assertEqual(skeleton.server.testable_func(2, 3), 6)

    def test_minus_two_times_four(self):
        self.assertEqual(skeleton.server.testable_func(-2, 4), -8)

    def test_not_for_numbers(self):
        self.assertRaises(TypeError, skeleton.server.testable_func, 'a', 'b')
