import unittest
import skeleton.server

class TestTrivial(unittest.TestCase):
    def test_two_times_three(self):
        self.assertEqual(skeleton.server.testable_func(2, 3), 6)

    def test_minus_two_times_four(self):
        self.assertEqual(skeleton.server.testable_func(-2, 4), -8)

    def test_not_for_numbers(self):
        self.assertRaises(TypeError, skeleton.server.testable_func, 'a', 'b')

class TestBones(unittest.TestCase):
    def setUp(self):
        self.app = skeleton.server.app.test_client()

    def test_bones_exist(self):
        response = self.app.get('/')
        body = str(response.get_data())
        self.assertIn('bones', body)

    def test_flesh_does_not_exist(self):
        response = self.app.get('/')
        body = str(response.get_data())
        self.assertNotIn(u'flesh', body)