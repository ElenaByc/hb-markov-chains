"""Generate Markov text from text files."""

from random import choice
import sys

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file = open(file_path)
    contents = file.read()
    file.close()

    return contents



def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains('hi there mary hi there juanita')

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key1, key2 = words[i], words[i + 1]
        if (key1, key2) in chains:
            chains[(key1, key2)].append(words[i + 2])
        else:
            chains[(key1, key2)] = [words[i + 2]]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    capital = False
    while capital == False:
        key = choice(list(chains.keys()))
        if key[0][0].isupper():
            capital = True
    print("First random key:", key)
    words.append(key[0])


    while key in chains:
        words.append(key[1])
        next_words_list = chains[key]
        # Make a new key out of the second word in the first key 
        # and the random word you pulled out from the list of words that followed it.
        key = (key[1], choice(next_words_list))
        
    words.append(key[1])
    return ' '.join(words)


def make_ngrams_chains(text_string, ngrams_size):
    chains = {}

    words = text_string.split()
    keys_list = []

    for i in range(len(words) - ngrams_size):
        for j in range(ngrams_size):
            keys_list.append(words[i + j])
        key = tuple(keys_list)
        # key = tuple(words[i:i + n])
        keys_list = []
        if key in chains:
            chains[key].append(words[i + ngrams_size])
        else:
            chains[key] = [words[i + ngrams_size]]

    return chains

def make_ngrams_text(chains):
    """Return text from chains."""

    words = []

    capital = False
    while capital == False:
        key = choice(list(chains.keys()))
        if key[0][0].isupper():
            capital = True
    print("First random key:", key)
    # words.append(key[0])
    words.extend(list(key[:-1]))
    # print("words: ", words)


    while key in chains:
        words.append(key[-1])
        # print("words: ", words)
        next_words_list = chains[key]
        # Make a new key out of the last (n-1) words in the first key 
        # and the random word you pulled out from the list of words that followed it.
        key = list(key[1:])
        key.append(choice(next_words_list))
        key = tuple(key)
        print("new_key = ", key)
        
    words.append(key[-1])
    return ' '.join(words)

# input_path = 'green-eggs.txt'
# input_path = 'gettysburg.txt'
input_path = sys.argv[1]
# print(sys.argv)

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)
print(input_text)

# Get a Markov chain
# chains = make_chains(input_text)
chains = make_ngrams_chains(input_text, 3)
for key, value in chains.items():
    print(key, value)

# Produce random text
# random_text = make_text(chains)
random_text = make_ngrams_text(chains)

print(random_text)
