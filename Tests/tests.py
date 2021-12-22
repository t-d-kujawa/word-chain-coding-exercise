import os
import shutil
import unittest
import dictionaryParser
import chainAlgorithm


class DictionaryParserTests(unittest.TestCase):
    test_directory = "testfiles"

    def setUp(self):
        os.mkdir(self.test_directory)
        os.chdir(self.test_directory)

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree(self.test_directory)

    def test_basic_function(self):
        with open("testfile.txt", mode='x') as testfile:
            testfile.write("line1\nline2\nline3")
        output = dictionaryParser.read_dictionary("testfile.txt")
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "line1")
        self.assertEqual(output[1], "line2")
        self.assertEqual(output[2], "line3")
        os.remove("testfile.txt")

    def test_skips_empty_lines(self):
        with open("testfile.txt", mode='x') as testfile:
            testfile.write("line1\n\nline2\n\nline3")
        output = dictionaryParser.read_dictionary("testfile.txt")
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "line1")
        self.assertEqual(output[1], "line2")
        self.assertEqual(output[2], "line3")
        os.remove("testfile.txt")

    def test_ignores_trailing_newline(self):
        with open("testfile.txt", mode='x') as testfile:
            testfile.write("line1\nline2\nline3\n")
        output = dictionaryParser.read_dictionary("testfile.txt")
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "line1")
        self.assertEqual(output[1], "line2")
        self.assertEqual(output[2], "line3")
        os.remove("testfile.txt")

    def test_uses_default_location(self):
        with open("dictionary.txt", mode='x') as testfile:
            testfile.write("line1\nline2\nline3")
        output = dictionaryParser.read_dictionary()
        self.assertEqual(len(output), 3)
        self.assertEqual(output[0], "line1")
        self.assertEqual(output[1], "line2")
        self.assertEqual(output[2], "line3")
        os.remove("dictionary.txt")


class OneCharDifferentTests(unittest.TestCase):
    def test_zero_char_different(self):
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hope"))

    def test_one_char_different(self):
        self.assertTrue(chainAlgorithm.check_one_char_difference("hope", "hose"))

    def test_two_char_different(self):
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hold"))


class WordHistoryTests(unittest.TestCase):
    def test_history_construction(self):
        first_word = chainAlgorithm.SearchNode("first")
        second_word = chainAlgorithm.SearchNode("second", first_word)
        third_word = chainAlgorithm.SearchNode("third", second_word)
        history = third_word.get_list()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0], "first")
        self.assertEqual(history[1], "second")
        self.assertEqual(history[2], "third")

    def test_single_word_history(self):
        word = chainAlgorithm.SearchNode("only")
        history = word.get_list()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0], "only")


class AdjacentWordsTests(unittest.TestCase):
    def test_adjacent_words_found(self):
        current_word = chainAlgorithm.SearchNode("hope")
        other_words = ["hope", "nope", "hype", "hole", "hops", "hold", "cape", "gold", "type", "rate"]
        adjacent_words = chainAlgorithm.get_adjacent_words(current_word, other_words)
        self.assertEqual(len(adjacent_words), 4)
        self.assertIn("nope", adjacent_words)
        self.assertIn("hype", adjacent_words)
        self.assertIn("hole", adjacent_words)
        self.assertIn("hops", adjacent_words)


class FullAlgorithmTests(unittest.TestCase):
    def test_chain_found(self):
        result = chainAlgorithm.get_chain("hope", "host", ["hope", "hose", "host", "distraction"])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "hope")
        self.assertEqual(result[1], "hose")
        self.assertEqual(result[2], "host")


if __name__ == '__main__':
    unittest.main()
