from unittest import TestCase
import heapq

from src.main import HuffmanNode, HuffmanEncoder, HuffmanDecoder


class TestHuffmanEncoder(TestCase):
    def test_analyze_string(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        print(encoder.heap)
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('K', 1))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('D', 1))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('R', 2))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('B', 2))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('A', 5))

    def test_build_tree(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        encoder.build_tree()
        self.assertEqual(
            encoder.tree,
            HuffmanNode(
                None,
                11,
                HuffmanNode('A', 5, None, None,),
                HuffmanNode(
                    None,
                    6,
                    HuffmanNode(
                        None,
                        2,
                        HuffmanNode('K', 1, None, None),
                        HuffmanNode('D', 1, None, None),
                    ),
                    HuffmanNode(
                        None,
                        4,
                        HuffmanNode('R', 2, None, None),
                        HuffmanNode('B', 2, None, None),
                    ),
                ),
            )
        )

    def test_build_codes(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        self.assertEqual(encoder.codes, {
            'A': '0',
            'B': '111',
            'R': '110',
            'K': '100',
            'D': '101'
        })

    def test_encode_array(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        encoder.encode_array()
        self.assertEqual(
            encoder.encoded_array,
            '111000001010000100000110001001011101010001001100101001011101000010'
        )
        # NOTE: array was manually built according to the following pattern:
        # non-repeating
        # identifier: 111  # has the length 3 as its the length of the first code
        #
        # repeating
        # code: 000  # this is the code for 'A' padded with 0s
        # unicode: 01000001  # this is the unicode for 'A' in binary (8 bits) 

    def test_encode_string(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        encoder.encode_string()
        self.assertEqual(encoder.encoded_string, '01111100100010101111100')

    def test_encode(self):
        pass
