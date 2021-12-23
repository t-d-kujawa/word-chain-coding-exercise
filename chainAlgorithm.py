def get_chain(start, end, dictionary):
    """Finds a minimum length chain of words with only one character different between each link

    start -- the first word in the chain
    end -- the last word in the chain
    dictionary -- a list of strings which count as words"""
    # Immediately
    if start == end:
        return [start]

    # bidirectional_bfs expects the words in current_nodes and target_nodes to not be in the dictionary
    if start in dictionary:
        dictionary.remove(start)
    if end in dictionary:
        dictionary.remove(end)

    chain = bidirectional_bfs([SearchNode(start)], [SearchNode(end)], dictionary)

    # Bidirectional nature means result may be in opposite order
    if len(chain) > 0 and chain[0] != start:
        chain.reverse()
    return chain


def bidirectional_bfs(current_nodes, target_nodes, dictionary):
    """A recursive implementation of Breadth-first search to find a chain"""
    # Check if this is the last step
    potential_chain = check_single_step(current_nodes, target_nodes)
    if len(potential_chain) > 0:
        return potential_chain

    # If a single step was not sufficient, find all adjacent words from the dictionary
    remaining_dictionary = dictionary.copy()
    next_words = []
    for current_word in current_nodes:
        adjacent_words = get_adjacent_words(current_word, remaining_dictionary)
        for found_word in adjacent_words:
            remaining_dictionary.remove(found_word)
        next_words.extend(map(lambda word: SearchNode(word, current_word), adjacent_words))

    # if no adjacent words were found, then there is no path
    if len(next_words) == 0:
        return []

    return bidirectional_bfs(target_nodes, next_words, remaining_dictionary)


def check_single_step(current_nodes, target_nodes):
    """Returns a chain if any target node is one step from any current node, empty otherwise"""
    for current_node in current_nodes:
        for target_node in target_nodes:
            if check_one_char_difference(current_node.word, target_node.word):
                left_list = current_node.get_list()
                right_list = target_node.get_list()
                right_list.reverse()
                left_list.extend(right_list)
                return left_list
    return []


def get_adjacent_words(current_node, dictionary):
    """Gets a list of words from the dictionary adjacent to"""
    adjacent_words = []
    for word in dictionary:
        if check_one_char_difference(current_node.word, word):
            adjacent_words.append(word)
    return adjacent_words


def check_one_char_difference(str1, str2):
    """Returns true if the two strings are 1 character different"""
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
