from unittest import TestCase
import heapq

from huffman.core import HuffmanNode, HuffmanEncoder, HuffmanDecoder


class TestHuffmanEncoder(TestCase):
    def test_analyze_string(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1)
        encoder.analyze_string()
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('K', 1))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('D', 1))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('R', 2))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('B', 2))
        self.assertEqual(heapq.heappop(encoder.heap), HuffmanNode('A', 5))

    def test_analyze_string_non_ascii(self):
        string = 'ABRAKADABRA–'  # the last character is a non-ascii character
        encoder = HuffmanEncoder(string, 1)
        # check if ValueError is raised
        with self.assertRaisesRegex(ValueError, 'non-ASCII'):
            encoder.analyze_string()

    def test_build_tree(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1)
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
        encoder = HuffmanEncoder(string, 1)
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
        encoder = HuffmanEncoder(string, 1)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        encoder.encode_array()
        self.assertEqual(
            encoder.encoded_array,
            '00001011110000100000110001001011101010001001100101001011101000010'
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
        encoder = HuffmanEncoder(string, 1)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        encoder.encode_string()
        self.assertEqual(encoder.encoded_string, '01111100100010101111100')


class TestHuffmanDecoder(TestCase):
    def test_read_until(self):
        string = '111111001010100'
        decoder = HuffmanDecoder(string)
        result, i = decoder.read_until(0)
        self.assertEqual(result, '111111')
        self.assertEqual(i, 6)
        result, i = decoder.read_until(0, delete=True)
        self.assertEqual(result, '111111')
        self.assertEqual(i, 6)
        self.assertEqual(decoder.encoded_string, '001010100')
        result, i = decoder.read_until(1)
        self.assertEqual(result, '00')

    def test_read_next(self):
        string = '111111001010100'
        decoder = HuffmanDecoder(string)
        result = decoder.read_next(3)
        self.assertEqual(result, '111')
        result = decoder.read_next(3, delete=True)
        self.assertEqual(result, '111')
        self.assertEqual(decoder.encoded_string, '111001010100')

    def test_decode_array(self):
        decoder = HuffmanDecoder(
            '101000010111100001000001100010010111010100010011001010010111010000100111110010001010111110000000',
        )
        decoder.decode_array()
        self.assertEqual(
            decoder.codes,
            {
                '000': 'A',
                '111': 'B',
                '110': 'R',
                '100': 'K',
                '101': 'D',
            }
        )

    def test_decode_tree(self):
        decoder = HuffmanDecoder(
            '101000010111100001000001100010010111010100010011001010010111010000100111110010001010111110000000',
        )
        decoder.decode_array()
        decoder.decode_tree()
        self.assertEqual(
            decoder.tree,
            HuffmanNode(
                None,
                None,
                HuffmanNode(
                    None,
                    None,
                    HuffmanNode(
                        None,
                        None,
                        HuffmanNode('A', None, None, None,),
                        None,
                    ),
                    None,
                ),
                HuffmanNode(
                    None,
                    None,
                    HuffmanNode(
                        None,
                        None,
                        HuffmanNode('K', None, None, None),
                        HuffmanNode('D', None, None, None),
                    ),
                    HuffmanNode(
                        None,
                        None,
                        HuffmanNode('R', None, None, None),
                        HuffmanNode('B', None, None, None),
                    ),
                ),
            )
        )

    def test_optimize_tree(self):
        decoder = HuffmanDecoder(
            '101000010111100001000001100010010111010100010011001010010111010000100111110010001010111110000000',
        )
        decoder.decode_array()
        decoder.decode_tree()
        decoder.optimize_tree()
        self.assertEqual(
            decoder.tree,
            HuffmanNode(
                None,
                None,
                HuffmanNode('A', None, None, None,),
                HuffmanNode(
                    None,
                    None,
                    HuffmanNode(
                        None,
                        None,
                        HuffmanNode('K', None, None, None),
                        HuffmanNode('D', None, None, None),
                    ),
                    HuffmanNode(
                        None,
                        None,
                        HuffmanNode('R', None, None, None),
                        HuffmanNode('B', None, None, None),
                    ),
                ),
            )
        )

    def test_decode_data(self):
        decoder = HuffmanDecoder(
            '101000010111100001000001100010010111010100010011001010010111010000100111110010001010111110000000',
        )
        decoder.decode_array()
        decoder.decode_tree()
        decoder.optimize_tree()
        decoder.decode_data()
        self.assertEqual(decoder.decoded_string, 'ABRAKADABRA')
