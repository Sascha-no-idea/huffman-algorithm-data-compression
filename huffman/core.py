import heapq
import numpy as np
import collections
import logging


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
        if other is None:
            return False
        if not isinstance(other, HuffmanNode):
            return False
        return self.freq == other.freq


class HuffmanEncoder:
    """
    This class handles the encoding of a string using the
    Huffman algorithm. It takes a string as input, analyzes
    the string, creates a Huffman tree, and encodes the
    string using the Huffman tree. The encoded string is
    returned.
    """
    def __init__(self, string, level, log=logging.getLogger()):
        self.string = string
        self.level = level
        self.log = log
        self.heap = []
        self.codes = {}

    def analyze_string(self):
        """
        This function analyzes the string and creates a
        priority queue (heap) that is used to construct
        the Huffman tree.
        """
        self.log.info('Analyzing string...')
        self.log.debug(f'Input string: {self.string}')
        self.log.debug('Checking if string is empty...')
        if not self.string:
            self.log.error('The string is empty.')
            raise ValueError('The string is empty.')
        self.log.debug('String is not empty.')
        self.log.debug('Checking if string only contains ASCII characters...')
        try:
            np.fromstring(self.string, dtype='S1').astype('U1')
        except UnicodeDecodeError:
            self.log.error('Non-ASCII characters found in string.')
            self.log.debug('Checking which character is non-ASCII...')
            for i, char in enumerate(self.string):
                # check if the character can be encoded using 8 bits
                if not len(char) == len(char.encode()):
                    self.log.debug(f'Character {i+1} in string is non-ASCII: "{char}".')
                    raise ValueError(
                        f'Character {i+1} in string is non-ASCII: "{char}".'
                    )
        self.log.debug('String only contains ASCII characters.')
        self.log.debug('Counting characters...')
        d = collections.Counter(self.string)  # count the characters --> dict
        # use heapq to create a priority queue
        self.log.debug('Creating Huffman nodes and priority queue...')
        for key, value in d.items():
            node = HuffmanNode(key, value)
            heapq.heappush(self.heap, node)
        self.log.debug('Priority queue created.')

    def build_tree(self):
        """
        This function builds the Huffman tree using the priority queue.
        """
        self.log.info('Building Huffman tree...')
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
        self.log.debug('Huffman tree built.')

    def build_codes(self):
        """
        This function builds the codes for each character
        in the string.
        """
        self.log.info('Building codes...')
        self.codes = {}  # TODO: improve performance
        # TODO: since dict is not ordered, a bug might occur
        # when the identifier is supposed to be determined
        # by the first character in the string (b'0') when
        # the order changes

        def traverse_tree(node, current_code=''):
            if node.char is not None:  # leaf node
                self.codes[node.char] = current_code
                return
            # traverse the left and right subtrees
            traverse_tree(node.left, current_code + '0')
            traverse_tree(node.right, current_code + '1')

        self.log.debug('Traversing Huffman tree...')
        traverse_tree(self.tree)
        self.log.debug('Codes built: %s', self.codes)

    def encode_array(self):
        """
        This function encodes the array that is used for translating
        the ASCII characters into the binary string.
        """
        self.log.info('Encoding array...')
        # define helper functions
        def pad_zeros(code: str, max_length: int):
            # invert string twice to pad zeros on the right
            return code[::-1].zfill(max_length)[::-1]

        def char_to_binary(char: str):
            # NOTE: this only works for single characters
            return format(char.encode('utf-8')[0], '08b')

        # convert the codes and chars to numpy arrays
        codes = np.array(list(self.codes.values()), dtype=object)
        chars = np.array(list(self.codes.keys()), dtype=object)
        # use vectorized helper functions
        bin_chars = np.vectorize(char_to_binary, otypes=[object])(chars)
        self.log.debug('Binary characters: %s', bin_chars)
        max_length = np.max(np.vectorize(len)(codes))
        self.log.debug('Number of codes: %s', len(codes))
        codes = np.vectorize(pad_zeros)(codes, max_length)
        self.log.debug('Padded codes: %s', codes)
        # concatenate the codes and the chars
        pairs = codes + bin_chars
        identifier = '1' * max_length
        self.log.debug('Identifier: %s', identifier)
        number = bin(len(self.codes))[2:].zfill(7)
        self.log.debug('Number of codes: 0b%s', number)
        # The first 3 bits are reserved for the length of the right
        # padding, that is added to round the length of the encoded
        # bits to a multiple of 8.
        # After the identifier follows the number of codes as an 7-bit
        # binary number (max. 128 codes = ASCII).
        # Number of following ones identifies the length of the codes.
        # Since the order of codes is preserved, the first code will be
        # '0', thus determining the end of the identifier.
        self.encoded_array = number + identifier + np.sum(pairs, axis=0)
        self.log.debug('Array encoding finished: %s', self.encoded_array)
        # TODO: automatically switch to dense array if its
        # size is smaller than the sparse array

    def encode_string(self):
        """
        This function encodes the string using the Huffman
        tree.
        """
        self.log.info('Encoding string...')
        self.encoded_string = ''
        for char in self.string:
            self.encoded_string += self.codes[char]
        self.log.debug('String encoding finished: %s', self.encoded_string)

    def finalize_encoding(self):
        self.log.info('Finalizing encoding...')
        self.finalized_string = self.encoded_array + self.encoded_string
        length = bin(8 - ((len(self.finalized_string) + 3) % 8))[2:].zfill(3)
        self.log.debug('Setting number of padding bits: 0b%s', length)
        self.finalized_string = length + self.finalized_string

    def encode(self):
        """
        This function analyzes the string, builds the tree,
        builds the codes, and encodes the string.
        """
        self.log.info('Encoding string...')
        self.analyze_string()
        self.build_tree()
        self.build_codes()
        self.encode_array()
        self.encode_string()
        self.finalize_encoding()
        self.log.info('Encoding finished.')
        return self.finalized_string


class HuffmanDecoder:
    """
    This class handles the decoding of a binary string using
    the Huffman algorithm. It takes a binary string as input,
    and decodes the string into the Huffman tree and the encoded
    data. The encoded data is then decoded using the Huffman
    tree. The decoded string is returned as a string.
    """
    def __init__(self, encoded_string, log=logging.getLogger()):
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
        self.log.info('Decoding array...')
        # read the length of the right padding and delete it
        right_padding = int(self.read_next(3, delete=True), 2)
        self.encoded_string = self.encoded_string[:-right_padding]
        self.log.debug('Number of padding bits: %s', right_padding)
        # read the number of codes
        number_of_codes = int(self.read_next(7, delete=True), 2)
        self.log.debug('Number of codes: %s', number_of_codes)
        # read until the first 0 is encountered
        _, depth = self.read_until(0, delete=True)
        # read the codes and the characters
        self.codes = {}
        self.log.debug('Start reading codes...')
        for _ in range(number_of_codes):
            code = self.read_next(depth, delete=True)
            char = self.read_next(8, delete=True)
            char = int(char, 2).to_bytes(1, 'big').decode('utf-8')
            self.codes[code] = char
            # TODO: improve performance by using numpy arrays
        self.log.debug('Reading codes finished: %s', self.codes)

    def decode_tree(self):
        """
        This function decodes the Huffman tree from the
        encoded string.
        """
        self.log.info('Decoding tree...')
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
        self.log.debug('Tree decoding finished.')

    def optimize_tree(self):
        """
        As the current tree has paths of standardized length,
        due to the encoding of the tree, the tree can be optimized
        in order to shorten paths that have no further branches.
        """
        self.log.info('Optimizing tree...')
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

        self.log.debug('Removing unecessary branches.')
        traverse_tree(self.tree)
        self.log.debug('Tree optimization finished.')

    def decode_data(self):
        """
        This function decodes the encoded data from the
        encoded string.
        """
        self.log.info('Decoding data...')
        self.decoded_string = ''
        self.current = self.tree
        for char in self.encoded_string:
            if char == '0':
                self.encoded_string = self.encoded_string[1:]
                self.current = self.current.left
            elif char == '1':
                self.encoded_string = self.encoded_string[1:]
                self.current = self.current.right
            if self.current.char is not None:
                self.decoded_string += self.current.char
                self.current = self.tree
        self.log.debug('String successfully decoded: %s', self.decoded_string)

    def decode(self):
        """
        This function decodes the encoded string.
        """
        self.log.info('Decoding string...')
        self.decode_array()
        self.decode_tree()
        self.optimize_tree()
        self.decode_data()
        self.log.info('Decoding finished.')
        return self.decoded_string
