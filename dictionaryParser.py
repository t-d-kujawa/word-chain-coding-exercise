def read_dictionary(file_location="dictionary.txt"):
    """Interprets a file as a list of words separated by newlines.

    file_location -- The path to the file (default "dictionary.txt")
    """
    words = []
    with open(file_location) as file:
        for line in file:
            word = line.strip()
            if len(word) > 0:
                words.append(word)

    return words
