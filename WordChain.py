from chainAlgorithm import get_chain
from dictionaryParser import read_dictionary
import argparse
import sys


def main():
    args = parse_args(sys.argv[1:])
    if args.words is not None:
        start = args.words[0]
        end = args.words[1]
    else:
        start = input("Choose the first word in the chain:")
        end = input("Choose the last word in the chain:")

    if args.dictionary is not None:
        dictionary = read_dictionary(args.dictionary)
    else:
        dictionary = read_dictionary()

    chain = get_chain(start, end, dictionary, args.length)

    if args.quiet:
        print(chain)
    else:
        if len(chain) == 0:
            print(f"No chain is possible between {start} and {end}")
        else:
            print(f"A chain was found with {len(chain)} links:")
            print(" -> ".join(chain))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dictionary", help="specify path to a custom dictionary")
    parser.add_argument("-l", "--length", action="store_true", help="require chains of constant word length")
    parser.add_argument("-q", "--quiet", action="store_true", help="reduces output to a minimum")
    parser.add_argument("-w", "--words", nargs=2, metavar=("start", "end"),
                        help="provide the start and end word here to skip the prompt")

    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == '__main__':
    main()
