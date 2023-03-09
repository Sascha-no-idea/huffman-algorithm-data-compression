# write a program that compresses ASCII text files using the
# huffman algorithm and writes the compressed file to disk
# as a binary file. The program should also be able to decompress
# the binary file and write the decompressed file to disk as a
# text file.

# This is implemented in four classes:
# 1. HuffmanTree
# 2. HuffmanNode
# 3. HuffmanEncoder
# 4. HuffmanDecoder

import heapq
import numpy as np
import collections


class HuffmanNode:
    """
    This class represents a node in the Huffman tree. It has
    a character, a frequency, and a pointer to the left and
    and right child nodes.
    """
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, HuffmanNode):
            return False
        return self.freq == other.freq

    def __ne__(self, other):
        return not self.__eq__(other)


class HuffmanEncoder:
    """
    This class handles the encoding of a string using the
    Huffman algorithm. It takes a string as input, analyzes
    the string, creates a Huffman tree, and encodes the
    string using the Huffman tree. The encoded string is
    returned.
    """
    def __init__(self, string, level, log):
        self.string = string
        self.level = level
        self.log = log
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def analyze_string(self):
        """
        This function analyzes the string and creates a
        priority queue (heap) that is used to construct
        the Huffman tree.
        """
        d = collections.Counter(self.string)  # count the characters --> dict
        # use heapq to create a priority queue
        for key, value in d.items():
            node = HuffmanNode(key, value)
            heapq.heappush(self.heap, node)

    def build_tree(self):
        """
        This function builds the Huffman tree using the priority queue.
        """
        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            new = HuffmanNode(None, left.freq + right.freq)
            # None instead of char because this is not a leaf node
            new.left = left
            new.right = right
            heapq.heappush(self.heap, new)

        # return the root node, which is the only node left in the heap
        self.tree = self.heap[0]

    def build_codes(self):
        """
        This function builds the codes for each character
        in the string.
        """
        self.codes = {}  # TODO: improve performance
        # TODO: since dict is not ordered, a bug might occur
        # when the identifier is supposed to be determined
        # by the first character in the string (b'0') when
        # the order changes

        def traverse_tree(node, current_code=''):
            if node is None:  # is this necessary?
                return

            if node.char is not None:  # leaf node
                self.codes[node.char] = current_code
                return
            # traverse the left and right subtrees
            traverse_tree(node.left, current_code + '0')
            traverse_tree(node.right, current_code + '1')

        traverse_tree(self.tree)

    def encode_array(self):
        """
        This function encodes the array that is used for translating
        the ASCII characters into the binary string.
        """
        # define helper functions
        def pad_zeros(code: str, max_length: int):
            return code.zfill(max_length)

        def char_to_binary(char: str):
            # NOTE: this only works for single characters
            return format(char.encode('utf-8')[0], '08b')

        # convert the codes and chars to numpy arrays
        codes = np.array(list(self.codes.values()), dtype=object)
        chars = np.array(list(self.codes.keys()), dtype=object)
        # use vectorized helper functions
        bin_chars = np.vectorize(char_to_binary, otypes=[object])(chars)
        max_length = np.max(np.vectorize(len)(codes))
        codes = np.vectorize(pad_zeros)(codes, max_length)
        # concatenate the codes and the chars
        pairs = codes + bin_chars
        identifier = '1' * max_length
        number = bin(len(self.codes))[2:].zfill(8)
        # NOTE: Number of ones identifies the length of the codes.
        # After the identifier follows the number of codes as an 8-bit
        # binary number. For 128 ASCII characters, the number starts
        # with 0 --> separator between identifier and number is 0.
        self.encoded_array = identifier + number + np.sum(pairs, axis=0)
        # TODO: automatically switch to dense array if its
        # size is smaller than the sparse array

    def encode_string(self):
        """
        This function encodes the string using the Huffman
        tree.
        """
        self.encoded_string = ''
        for char in self.string:
            self.encoded_string += self.codes[char]

    def encode(self):
        """
        This function analyzes the string, builds the tree,
        builds the codes, and encodes the string.
        """
        self.analyze_string()
        self.build_tree()
        self.build_codes()
        self.encode_array()
        self.encode_string()
        return self.encoded_array + self.encoded_string


class HuffmanDecoder:
    """
    This class handles the decoding of a binary string using
    the Huffman algorithm. It takes a binary string as input,
    and decodes the string into the Huffman tree and the encoded
    data. The encoded data is then decoded using the Huffman
    tree. The decoded string is returned as a string.
    """
    def __init__(self, encoded_string, log):
        self.encoded_string = encoded_string
        self.log = log

    def read_until(self, char: int, delete: bool = False):
        """
        This function reads the encoded string until the
        specified character is encountered.
        """
        if char not in [0, 1]:
            raise ValueError('char must be 0 or 1')
        char = str(char)
        i = 0
        while self.encoded_string[i] != char:
            i += 1
            if i >= len(self.encoded_string):
                raise ValueError('char not found')
        result = self.encoded_string[:i]
        if delete:
            self.encoded_string = self.encoded_string[i:]
        return result, i

    def read_next(self, number: int, delete: bool = False):
        """
        This function reads the next n characters from
        the encoded string.
        """
        if number < 0:
            raise ValueError('number must be non-negative')
        result = self.encoded_string[:number]
        if delete:
            self.encoded_string = self.encoded_string[number:]
        return result

    def decode_array(self):
        # read until the first 0 is encountered
        _, depth = self.read_until(0, delete=True)
        # read the number of codes
        number_of_codes = int(self.read_next(8, delete=True), 2)
        # read the codes and the characters
        self.codes = {}
        for _ in range(number_of_codes):
            code = self.read_next(depth, delete=True)
            char = self.read_next(8, delete=True)
            char = int(char, 2).to_bytes(1, 'big').decode('utf-8')
            self.codes[code] = char
            # TODO: improve performance by using numpy arrays

    def decode_tree(self):
        """
        This function decodes the Huffman tree from the
        encoded string.
        """
        self.tree = HuffmanNode()
        for code, leaf in self.codes.items():
            current_node = self.tree
            for direction in code:
                if direction == '0':
                    if current_node.left is None:
                        current_node.left = HuffmanNode()
                    current_node = current_node.left
                elif direction == '1':
                    if current_node.right is None:
                        current_node.right = HuffmanNode()
                    current_node = current_node.right
            current_node.char = leaf

    def optimize_tree(self):
        """
        As the current tree has paths of standardized length,
        due to the encoding of the tree, the tree can be optimized
        in order to shorten paths that have no further branches.
        """
        def traverse_tree(node, current_code=''):
            # traverse to the deepest node
            if node.left is None and node.right is None:
                # must be a leaf node with a character
                return node.char

            if node.left is not None:
                # traverse the left subtree
                left_char = traverse_tree(node.left, current_code + '0')
                if node.right is None:
                    # if there is no right subtree, the left subtree
                    # must be a leaf node with a character
                    node.left = None
                    node.char = left_char
                    return left_char

            if node.right is not None:
                # traverse the right subtree
                traverse_tree(node.right, current_code + '1')

        traverse_tree(self.tree)

    def decode_data(self):
        """
        This function decodes the encoded data from the
        encoded string.
        """
        pass

    def decode(self):
        """
        This function decodes the encoded string.
        """
        self.decode_array()
        self.decode_tree()
        self.optimize_tree()


# for debugging
if __name__ == '__main__':
    #encoder = HuffmanEncoder('ABRAKADABRA', 1, None)
    #encoder.encode()

    decoder = HuffmanDecoder(
        '111000001010000100000110001001011101010001001100101001011101000010',
        None,
    )
    decoder.decode()
