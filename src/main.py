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

import sys
import os
import math
import heapq
import time
import argparse
import logging

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
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            node3 = HuffmanNode(None, node1.freq + node2.freq)
            node3.left = node1
            node3.right = node2
            heapq.heappush(self.heap, node3)
        return self.heap[0]


class HuffmanNode:
    """
    This class represents a node in the Huffman tree. It has
    a character, a frequency, and a pointer to the left and
    and right child nodes.
    """
    def __init__(self, char, freq):
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
        pass

    def build_tree(self):
        """
        This function builds the Huffman tree.
        """
        pass

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
        pass
    

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


def initialize_logger(verbose, debug):
    """
    This function initializes the logger and sets the
    debug level.
    """
    # TODO: might want to move this to a separate file
    # initalize
    log = logging.getLogger()
    if debug:
        log.setLevel(logging.DEBUG)
    elif verbose:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)
    # set formatter and file handler
    log_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    file_handler = logging.FileHandler('log.txt', mode='w')
    file_handler.setFormatter(log_formatter)
    log.addHandler(file_handler)
    # test logger
    log.info('Logger initialized')
    return log


def parse_args():
    """
    This function parses the command line arguments and
    returns the input file name, output file name, and
    the different compression and decompression options.
    Compression or decompression is chosen automatically
    by the file extension of the input file.
    """
    # TODO: might want to move this to a separate file
    parser = argparse.ArgumentParser(
        description='Compress and decompress files using the Huffman algorithm'
    )
    parser.add_argument(
        '-i',
        '--input_file',
        type=str,
        help='path the input file',
        required=True
    )
    parser.add_argument(
        '-o',
        '--overwrite',
        help='overwrite output file if it already exists',
        action='store_true'
    )
    parser.add_argument(
        '-l',
        '--level',
        type=int,
        help='compression level',
        required=False,
        default=1
    )
    parser.add_argument(
        '-v',
        '--verbose',
        help='verbose mode',
        action='store_true'
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='debug mode',
        action='store_true'
    )
    return vars(parser.parse_args())

if __name__ == '__main__':
    # parse the command line arguments
    args = parse_args()
    # initialize the logger
    log = initialize_logger(args['verbose'], args['debug'])
    # check if the input file exists
    if not os.path.exists(args['input_file']):
        log.error('Input file not found: %s', args['input_file'])
        raise FileNotFoundError('Input file not found')
    # check if the input file is a text file
    if not args['input_file'].endswith('.txt'):
        log.error('Input file is not a text file: %s', args['input_file'])
        raise ValueError('Input file is not a text file')
    # check if output file already exists
    args['output_file'] = args['input_file'].replace('.txt', '.bin')
    if os.path.exists(args['output_file']) and not args['overwrite']:
        log.error('Output file already exists: %s', args['output_file'])
        raise FileExistsError(
            'Output file already exists. Please delete it first or set the --overwrite flag.'
        )
    # check if the compression level is valid
    if args['level'] in [1, 2]:
        log.info('Compression level set to %s', args['level'])
    else:
        log.error('Invalid compression level: %s', args['level'])
        raise ValueError('Invalid compression level')
    # check which mode to use (compression or decompression)
    args['mode'] = 'compression' if args['input_file'].endswith('.txt') else 'decompression'
    # compress or decompress the file
    if args['mode'] == 'compression':
        # read the input file
        with open(args['input_file'], 'r') as f:
            string = f.read()
        # compress the string
        encoded_string = HuffmanEncoder(string, args['level'], log).encode()
        # write the encoded string to the output file
        with open(args['output_file'], 'wb') as f:
            f.write(encoded_string)
    elif args['mode'] == 'decompression':
        # read the input file
        with open(args['input_file'], 'rb') as f:
            encoded_string = f.read()
        # decompress the string
        string = HuffmanDecoder(encoded_string, log).decode()
        # write the decoded string to the output file
        with open(args['output_file'], 'w') as f:
            f.write(string)
    # print the compression ratio
    if args['mode'] == 'compression':
        uncompressed_size = os.path.getsize(args['input_file'])
        compressed_size = os.path.getsize(args['output_file'])
        compression_ratio = uncompressed_size / compressed_size * 100
        log.info('Compression ratio: %s %', compression_ratio)
