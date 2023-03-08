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
            'A': b'0',
            'B': b'111',
            'R': b'110',
            'K': b'100',
            'D': b'101'
        })

    def test_encode_string(self):
        string = 'ABRAKADABRA'
        encoder = HuffmanEncoder(string, 1, None)
        encoder.analyze_string()
        encoder.build_tree()
        encoder.build_codes()
        encoder.encode_string()
        self.assertEqual(encoder.encoded_string, b'01111100100010101111100')

    def test_encode(self):
        pass
