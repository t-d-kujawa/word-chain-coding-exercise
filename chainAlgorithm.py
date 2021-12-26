def get_chain(start, end, dictionary, constant_length=False):
    """Finds a minimum length chain of words with only one character different between each link

    start -- the first word in the chain
    end -- the last word in the chain
    dictionary -- a list of strings which count as words"""
    # Short-circuit obvious results
    if start == end:
        return [start]
    if constant_length and len(start) != len(end):
        return []

    # Duplicate the dictionary so it can be modified safely
    remaining_dictionary = dictionary.copy()

    # bidirectional_bfs expects the words in current_nodes and target_nodes to not be in the dictionary
    if start in remaining_dictionary:
        remaining_dictionary.remove(start)
    if end in remaining_dictionary:
        remaining_dictionary.remove(end)

    # Run the main algorithm
    chain = bidirectional_bfs([SearchNode(start)], [SearchNode(end)], remaining_dictionary, constant_length)

    # Bidirectional nature means result may be in opposite order
    if len(chain) > 0 and chain[0] != start:
        chain.reverse()
    return chain


def bidirectional_bfs(current_nodes, target_nodes, dictionary, constant_length=False):
    """A recursive implementation of Breadth-first search to find a chain"""
    # Check if this is the last step
    potential_chain = check_single_step(current_nodes, target_nodes, constant_length)
    if len(potential_chain) > 0:
        return potential_chain

    # If a single step was not sufficient, find all adjacent words from the dictionary
    next_words = []
    for current_word in current_nodes:
        adjacent_words = get_adjacent_words(current_word, dictionary, constant_length)
        for found_word in adjacent_words:
            dictionary.remove(found_word)
        next_words.extend(map(lambda word: SearchNode(word, current_word), adjacent_words))

    # If no adjacent words were found, then there is no path
    if len(next_words) == 0:
        return []

    # Otherwise, move on to the next step
    return bidirectional_bfs(target_nodes, next_words, dictionary, constant_length)


def check_single_step(current_nodes, target_nodes, constant_length=False):
    """Returns a chain if any target node is one step from any current node, empty otherwise"""
    for current_node in current_nodes:
        for target_node in target_nodes:
            if check_one_char_difference(current_node.word, target_node.word, constant_length):
                left_list = current_node.get_list()
                right_list = target_node.get_list()
                right_list.reverse()
                left_list.extend(right_list)
                return left_list
    return []


def get_adjacent_words(current_node, dictionary, constant_length=False):
    """Gets a list of words from the dictionary adjacent to"""
    adjacent_words = []
    for word in dictionary:
        if check_one_char_difference(current_node.word, word, constant_length):
            adjacent_words.append(word)
    return adjacent_words


def check_one_char_difference(str1, str2, constant_length=False):
    """Returns true if the two strings are 1 character different"""
    if constant_length:
        if len(str1) != len(str2):
            return False
        differences = 0
        for i in range(0, len(str1)):
            if str1[i] != str2[i]:
                differences += 1
                if differences > 1:
                    return False
        return differences == 1
    else:
        return get_levenshtein_distance(str1, str2) == 1


def get_levenshtein_distance(str1, str2):
    """An implementation of the Levenshtein Distance algorithm"""
    # Prepare the original matrix
    matrix = []
    for s1 in range(0, len(str1)+1):
        matrix.append([s1])
    for s2 in range(1, len(str2)+1):
        matrix[0].append(s2)

    for s1 in range(1, len(str1)+1):
        for s2 in range(1, len(str2)+1):
            if str1[s1-1] == str2[s2-1]:
                matrix[s1].append(matrix[s1-1][s2-1])
            else:
                a = matrix[s1][s2-1]
                b = matrix[s1-1][s2]
                c = matrix[s1-1][s2-1]
                if a <= b and a <= c:
                    matrix[s1].append(a + 1)
                elif b <= a and b <= c:
                    matrix[s1].append(b + 1)
                else:
                    matrix[s1].append(c + 1)

    return matrix[len(str1)][len(str2)]


class SearchNode:
    """Retains the previous steps of a BFS node so a full chain can be constructed later"""

    def __init__(self, this_word, prev_node=None):
        """Represents a partial chain while the search isn't completed

        this_word -- The most recent word to be added to the chain
        prev_node -- The previous node in the chain
        """
        self.word = this_word
        self.previous = prev_node

    def get_list(self):
        """Generates a list of the words used to reach the current word"""
        history = self.previous.get_list() if self.previous is not None else []
        history.append(self.word)
        return history
