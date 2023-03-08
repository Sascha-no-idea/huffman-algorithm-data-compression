from unittest.mock import TestCase, patch

from src.main_cli import Interface
# from src.main import HuffmanEncoder, HuffmanDecoder

class TestInterface(TestCase):
    @patch('src.main.HuffmanEncoder')
    def test_init_call_args(self):
        interface = Interface()
        interface.args = {
            'input_file': 'test/short.txt',
            'overwrite': False,
            'level': 1,
            'verbose': False,
            'debug': False,
        }
        interface.initialize_logger()
        interface.check_input()
        interface.check_mode()
        # run the appropriate mode
        if interface.args['mode'] == 'compression':
            interface.compress()
            interface.compression_ratio()
        elif  interface.args['mode'] == 'decompression':
            interface.decompress()
        # check instance variables of HuffmanEncoder

