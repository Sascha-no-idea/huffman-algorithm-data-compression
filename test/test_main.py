from unittest import TestCase
import heapq

from src.main import HuffmanTree, HuffmanNode, HuffmanEncoder, HuffmanDecoder


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
        pass

    def test_build_codes(self):
        pass

    def test_encode_string(self):
        pass

    def test_encode(self):
        pass
