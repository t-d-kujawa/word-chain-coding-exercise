import random
import time
import chainAlgorithm
import dictionaryParser


def generate_test_cases(dictionary, test_count):
    test_cases = []
    dictionary_size = len(dictionary)
    for _ in range(0, test_count):
        start_word_index = random.randrange(0, dictionary_size)
        end_word_index = random.randrange(0, dictionary_size)
        test_cases.append((dictionary[start_word_index], dictionary[end_word_index]))
    return test_cases


def benchmark_function(function, dictionary, test_cases):
    run_times = []
    max_run_time = 0
    total_run_time = 0
    for test_case in test_cases:
        run_start = time.perf_counter()
        result = function(test_case[0], test_case[1], dictionary)
        run_stop = time.perf_counter()
        run_time = run_stop - run_start
        total_run_time += run_time
        if run_time > max_run_time:
            max_run_time = run_time

    avg_run_time = total_run_time / len(test_cases)
    return avg_run_time, max_run_time


def run_benchmarks():
    functions = [("Bidirectional BFS", chainAlgorithm.get_chain),
                 ("Alphabetical optimization", chainAlgorithm.get_chain_A)]
    dictionary = dictionaryParser.read_dictionary()
    test_count = 10
    test_cases = generate_test_cases(dictionary, test_count)
    for function in functions:
        print(f"Running {function[0]}...")
        benchmark_results = benchmark_function(function[1], dictionary, test_cases)
        print(f"{function[0]} had an average time of {benchmark_results[0]:0.6f}s "
              f"and a max time of {benchmark_results[1]:0.6f}s")


if __name__ == '__main__':
    run_benchmarks()
