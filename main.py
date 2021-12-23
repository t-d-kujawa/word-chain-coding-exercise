from chainAlgorithm import get_chain
from dictionaryParser import read_dictionary


def main():
    """A basic runner that prompts for necessary inputs and prints the result"""
    dictionary_path = input("Choose a dictionary location (leave blank for default dictionary):")
    first_word = input("Choose the first word in the chain:")
    final_word = input("Choose the last word in the chain:")

    if dictionary_path == "":
        dictionary = read_dictionary()
    else:
        dictionary = read_dictionary(dictionary_path)
    chain = get_chain(first_word, final_word, dictionary)

    if len(chain) == 0:
        print(f"No chain is possible between {first_word} and {final_word}")
    else:
        print(f"A chain was found with {len(chain)} links:")
        print(" -> ".join(chain))


if __name__ == '__main__':
    main()
