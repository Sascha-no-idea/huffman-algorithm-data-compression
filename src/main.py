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
import collections


class HuffmanTree:
    """
    This class represents a binary tree that is used to encode
    and decode messages using the Huffman algorithm. The tree
    is constructed using a priority queue that is populated with
    the characters in the message and their frequencies. The
    tree is constructed by combining the two nodes with the
    highest priority (lowest frequency) until only one node
    is left. The Huffman tree is a binary tree where the
    nodes are HuffmanNodes.
    """
    def __init__(self, heap):
        self.heap = heap

    def build_tree(self):
        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            new = HuffmanNode(None, left.freq + right.freq)
            # None instead of char because this is not a leaf node
            new.left = left
            new.right = right
            heapq.heappush(self.heap, new)
        return self.heap[0]  # return the root node, which is the only node left in the heap


class HuffmanNode:
    """
    This class represents a node in the Huffman tree. It has
    a character, a frequency, and a pointer to the left and
    and right child nodes.
    """
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

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
    returned as a binary string.
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
        tree = HuffmanTree(self.heap)
        self.tree = tree.build_tree()

    def build_codes(self):
        """
        This function builds the codes for each character
        in the string.
        """
        pass

    def encode_string(self):
        """
        This function encodes the string using the Huffman
        tree.
        """
        pass

    def encode(self):
        """
        This function analyzes the string, builds the tree,
        builds the codes, and encodes the string.
        """
        self.analyze_string()
        self.build_tree()


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
        self.current_node = self.tree

    def decode_tree(self):
        """
        This function decodes the Huffman tree from the
        encoded string.
        """
        pass

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
        pass
