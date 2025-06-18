'''
File: writer_bot_ht.py
Author: Michael Masenheimer
Course: CSC 120, Fall 2024
Purpose: This program takes in a file of source
text and through the markov chain algorithm, generates a random
text (according to the random seed). It uses a hash table class to 
add prefixes and suffixes into as opposed to using
a built-in python dictionary.
'''

import sys
import random

SEED = 8
random.seed(SEED)

NONWORD = '@'

class Hashtable:
    '''
    This class represents a hash table to store prefix-suffix pairs.

    The class initializes the table to a list of None times
    a specified size of the table. The class defines methods for 
    hashing to an index through a key, adding a new item in the
    table, getting a specific item from the table, and special methods
    to check if an item is in the table and str representation
    of the table.
    '''
    def __init__(self, size):
        '''
        The init method initializes the size of the
        table to an inputted argument, and sets the self._pairs
        (the actual table) to a list of nones times the size.

        Parameters: size is an integer representing the size of the hash table.
        '''
        self._size = size
        self._pairs = [None] * size

    def _hash(self, key):
        '''
        This method takes in a tuple as a key, and hashes to get the 
        index of said key. This was taken from assignment 11 specs, but
        modified to search tuples instead of individual characters.
        
        Parameters: key is a tuple which is or will be a key in the table.
        
        Returns: an integer representation of the index of the key in the 
        table.
        '''
        num = 0
        for item in key:
            for character in item:
                num = 31 * num + ord(character)
        return num % self._size

    def put(self, key, value):
        '''
        This function adds a new prefix-suffix pair into the hash
        table. It uses linear probing with a decrement of 1 to resolve
        collisions.

        Parameters: key is a key to be added, and value is a value to be
        added into the table.
        '''
        index = self._hash(key)

        while self._pairs[index] != None:
            if self._pairs[index][0] == key:
                self._pairs[index][1] = value
                return
            index = (index - 1) % self._size
            # Probing by 1
           
        self._pairs[index] = [key, value]
        # Adding the items into the table
    
    def get(self, key):
        '''
        This method uses linear probing to find a key in the
        table, and returns the value associated with the key.

        Parameters: key is a key to be looked up

        Returns: the value associated with that key
        '''
        index = self._hash(key)
        # Hashing to find the index
     
        while self._pairs[index] is not None:
            if self._pairs[index][0] == key:
                return self._pairs[index][1]
                # Return the value (which is at index 1)
            index = (index - 1) % self._size
            # Probing by 1
        return None
    
    def __contains__(self, key):
        '''
        This method checks the table to see if a key is in it and returns
        true or false according to the result of the search.

        Parameters: key is a key to be looked up

        Returns: True or False depending on if the key exists in the table or
        not
        '''
        index = self._hash(key)
        # Hashing to find the index

        while self._pairs[index] is not None:
            if self._pairs[index][0] == key:
                return True
            index = (index - 1) % self._size
            # Probing by 1
        return False
    
    def __str__(self):
        return str(self._pairs)

def build_table(words, hash_size, prefix_size):
    '''
    This function creates a Markov chain table from a list of words
    (from the file of words), it creates prefixes of a length "length",
    and associates them with a list of possible suffixes from the text.

    Parameters: words is a list of words from the input text, and prefix_size
    is the size of the prefix to be used in the Markov table, hash_size is the
    size of the hash table

    Returns: A hash table where each key is a prefix from the text
    and the value is a list of words that follow the prefix.
    '''
        
    words = [NONWORD] * prefix_size + words
    table = Hashtable(hash_size)

    for index in range(len(words) - prefix_size):

        prefix = tuple(words[index:index + prefix_size])
        # Creating a tuple for immutibility

        suffix = words[index + prefix_size]
        # Identifying the suffix

        if prefix not in table:
            table.put(prefix, [])
            
            # If the prefix is not in the table, create a value for it
            
        current = table.get(prefix)
        current.append(suffix)
        # Otherwise add the possible suffixes for the current prefix

    return table


def make_text(dictionary, words, length, num_words):
    '''
    This function generates random text based on the Marov chain model.

    Parameters: Table is a hasmap with keys as prefixes and the values
    are lists of possible words following the prefix. Words is a list of words
    from the text, length is the length of the prefix used to generate each 
    suffix, and num_words is the total number of words to generate, specified 
    by user input.

    Returns: A list of generated words.
    '''
    
    tlist = list(words[:length])
    # Initializes the list of words for output
    current_prefix = tuple(tlist)

    for _ in range(num_words - length):

        if current_prefix in dictionary:
            # Check if the current prefix is in the dictionary
            suffixes = dictionary.get(current_prefix)


            if len(suffixes) > 1:
                next_word = suffixes[random.randint(0, len(suffixes) - 1)]
                # Choosing a random suffix (specified by the seed)

            else:
                next_word = suffixes[0]

            tlist.append(next_word)
            current_prefix = tuple(tlist[-length:])
            # Update the prefix
    return tlist

def format_lines(text):
    '''
    This function formats the text generated from the generate_text
    function, limiting the text of each line to 10 words.

    Perameters: text is a list of words which are to be printed out

    Returns: Prints the text 10 words per line
    '''

    for index in range(0, len(text), 10):
        # Limiting the words to 10 per line

        print(' '.join(text[index: index + 10]))


def plugin_inputs():
    '''
    This function handles all of the inputs in the program. It
    takes in a file, the prefix size and the number or words to
    be outputted and plugs them all into the other functions
    to create the tables and output text.
    '''
    infile = input()
    hash_table_size = int(input())
    prefix_size = int(input())
    num_words = int(input())
    if prefix_size < 1:
        print("ERROR: specified prefix size is less than one")
        sys.exit(0)

    if num_words < 1:
        print("ERROR: specified size of the generated text is less than one")
        sys.exit(0)
    # Gathering all of the inputs

    file = open(infile, "r")
    words = file.read().split()
    # Opening and reading the file

    table = build_table(words, hash_table_size, prefix_size)

    generated_text = make_text(table, words, prefix_size, num_words)

    format_lines(generated_text)
    
    file.close()

def main():
    plugin_inputs()
main()