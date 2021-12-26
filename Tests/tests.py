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
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hope"), False)
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hope"), True)

    def test_one_char_different(self):
        self.assertTrue(chainAlgorithm.check_one_char_difference("hope", "hose"), False)
        self.assertTrue(chainAlgorithm.check_one_char_difference("hope", "hose"), True)

    def test_two_char_different(self):
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hold"), False)
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hold"), True)

    def test_different_length(self):
        self.assertTrue(chainAlgorithm.check_one_char_difference("hope", "hoped", False))
        self.assertFalse(chainAlgorithm.check_one_char_difference("hope", "hoped", True))


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
    def test_variable_length(self):
        current_word = chainAlgorithm.SearchNode("hope")
        other_words = ["hope", "nope", "hype", "hole", "hops", "hoped", "hop", "hold", "cape", "gold", "type", "rate"]
        adjacent_words = chainAlgorithm.get_adjacent_words(current_word, other_words)
        self.assertEqual(len(adjacent_words), 6)
        self.assertIn("nope", adjacent_words)
        self.assertIn("hype", adjacent_words)
        self.assertIn("hole", adjacent_words)
        self.assertIn("hops", adjacent_words)
        self.assertIn("hoped", adjacent_words)
        self.assertIn("hop", adjacent_words)

    def test_constant_length(self):
        current_word = chainAlgorithm.SearchNode("hope")
        other_words = ["hope", "nope", "hype", "hole", "hops", "hoped", "hop", "hold", "cape", "gold", "type",
                       "rate"]
        adjacent_words = chainAlgorithm.get_adjacent_words(current_word, other_words, True)
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

    def test_length_increase(self):
        result = chainAlgorithm.get_chain("pace", "paced", ["pace", "paced"])
        self.assertEqual(len(result), 2)

    def test_length_decrease(self):
        result = chainAlgorithm.get_chain("hope", "hop", ["hope", "hop"])
        self.assertEqual(len(result), 2)

    def test_route_through_other_length(self):
        result = chainAlgorithm.get_chain("abet", "bate", ["abet", "bet", "bat", "bate"])
        self.assertEqual(len(result), 4)

    def test_chain_impossible(self):
        result = chainAlgorithm.get_chain("hello", "goodbye", ["hello", "irrelevant", "random", "useless", "goodbye"])
        self.assertEqual(len(result), 0)

    def test_self_chain(self):
        result = chainAlgorithm.get_chain("hello", "hello", ["hello"])
        self.assertEqual(len(result), 1)

    def test_dictionary_preserved(self):
        dictionary = ["hope", "hose", "host", "distraction"]
        chainAlgorithm.get_chain("hope", "host", dictionary)
        self.assertEqual(len(dictionary), 4)

    # constant length tests
    def test_cl_chain_found(self):
        result = chainAlgorithm.get_chain("hope", "host", ["hope", "hose", "host", "distraction"], True)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "hope")
        self.assertEqual(result[1], "hose")
        self.assertEqual(result[2], "host")

    def test_cl_length_increase(self):
        result = chainAlgorithm.get_chain("pace", "paced", ["pace", "paced"], True)
        self.assertEqual(len(result), 0)

    def test_cl_length_decrease(self):
        result = chainAlgorithm.get_chain("hope", "hop", ["hope", "hop"], True)
        self.assertEqual(len(result), 0)

    def test_cl_route_through_other_length(self):
        result = chainAlgorithm.get_chain("abet", "bate", ["abet", "bet", "bat", "bate"], True)
        self.assertEqual(len(result), 0)



class LevenshteinDistanceTests(unittest.TestCase):
    def test_zero_distance(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hope")
        self.assertEqual(result, 0)

    def test_one_change(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hose")
        self.assertEqual(result, 1)

    def test_one_addition(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hoped")
        self.assertEqual(result, 1)

    def test_one_removal(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hop")
        self.assertEqual(result, 1)

    def test_change_and_add(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hyper")
        self.assertEqual(result, 2)

    def test_change_and_remove(self):
        result = chainAlgorithm.get_levenshtein_distance("hope", "hip")
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
