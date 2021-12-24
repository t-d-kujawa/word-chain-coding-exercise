import benchmark
import unittest


class TestCaseTests(unittest.TestCase):
    def test_case_generates(self):
        dictionary = ["word"]
        test_cases = benchmark.generate_test_cases(dictionary, 1)
        self.assertEqual(len(test_cases), 1)
        self.assertEqual(test_cases[0][0], "word")
        self.assertEqual(test_cases[0][1], "word")

    def test_multiple_test_cases(self):
        dictionary = ["first", "second", "third", "fourth"]
        test_cases = benchmark.generate_test_cases(dictionary, 3)
        self.assertEqual(len(test_cases), 3)
        for test_case in test_cases:
            self.assertIn(test_case[0], dictionary)
            self.assertIn(test_case[1], dictionary)


if __name__ == '__main__':
    unittest.main()
