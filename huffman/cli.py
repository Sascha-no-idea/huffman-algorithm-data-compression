import argparse
import logging
import os
import sys
from bitstring import BitArray

from core import HuffmanEncoder, HuffmanDecoder


class Interface:
    def __init__(self):
        self.args = None
        self.log = None

    def parse_args(self):
        """
        This function parses the command line arguments and
        returns the input file name, output file name, and
        the different compression and decompression options.
        Compression or decompression is chosen automatically
        by the file extension of the input file.
        """
        parser = argparse.ArgumentParser(
            description='Compress and decompress files using the Huffman algorithm'
        )
        parser.add_argument(
            'input_file',
            nargs='?',
            type=str,
            help='path the input file',
        )
        parser.add_argument(
            '-o',
            '--output_file',
            type=str,
            help='path to the output file',
            required=False
        )
        parser.add_argument(
            '-f',
            '--force',
            help='force overwrite output file if it already exists',
            action='store_true'
        )
        parser.add_argument(
            '-l',
            '--level',
            type=int,
            help='compression level (1-2)',
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
        self.args = vars(parser.parse_args())
        return

    def initialize_logger(self):
        """
        This function initializes the logger and sets the
        debug level.
        """
        # initalize
        self.log = logging.getLogger()
        if self.args['debug']:
            self.log.setLevel(logging.DEBUG)
        elif self.args['verbose']:
            self.log.setLevel(logging.INFO)
        else:
            self.log.setLevel(logging.WARNING)
        # set file handler
        log_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler('log.txt', mode='w')
        file_handler.setFormatter(log_formatter)
        self.log.addHandler(file_handler)
        # set stream handler
        stream_log_formatter = logging.Formatter('%(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(stream_log_formatter)
        self.log.addHandler(stream_handler)
        # test logger
        self.log.info('Logger initialized')
        self.log.debug('Debug mode enabled')
        return

    def check_mode(self):
        if self.args['input_file'] is not None:
            if os.path.exists(self.args['input_file']):
                if self.args['input_file'].endswith('.txt'):
                    self.args['mode'] = 'compression'
                    self.log.info('compression mode selected')
                elif self.args['input_file'].endswith('.huff'):
                    self.args['mode'] = 'decompression'
                    self.log.info('decompression mode selected')
            else:
                self.log.error('Input file not found: %s', self.args['input_file'])
                raise FileNotFoundError('Input file not found')
        else:
            self.args['input_file'] = None
            self.args['input_string'] = sys.stdin.read()
            if self.args['input_string'].isascii():
                self.args['mode'] = 'compression'
                self.log.info('compression mode selected')
            else:
                self.args['mode'] = 'decompression'
                self.log.info('decompression mode selected')

    def check_output_path(self):
        if self.args['output_file'] is None:
            if self.args['input_file'] is not None:
                if self.args['mode'] == 'compression':
                    self.args['output_file'] = self.args['input_file'].replace('.txt', '.huff')
                elif self.args['mode'] == 'decompression':
                    self.args['output_file'] = self.args['input_file'].replace('.huff', '.txt')
            else:
                if self.args['mode'] == 'compression':
                    self.args['output_file'] = 'output.huff'
                elif self.args['mode'] == 'decompression':
                    self.args['output_file'] = 'output.txt'

    def check_output_file(self):
        if os.path.exists(self.args['output_file']):
            if not self.args['force']:
                self.log.error('Output file already exists and --force flag not set')
                raise FileExistsError('Output file already exists and --force flag not set')

    def check_level(self):
        if self.args['level'] in [1, 2]:
            self.log.info('Compression level set to %s', self.args['level'])
        else:
            self.log.error('Invalid compression level: %s', self.args['level'])
            raise ValueError('Invalid compression level')

    def bits_to_bytes(self, bits, size=8, pad='0'):
        """
        This function converts a binary string into a byte array.
        It was taken from https://stackoverflow.com/a/47311736.
        """
        chunks = [bits[n:n+size] for n in range(0, len(bits), size)]
        if pad:
            chunks[-1] = chunks[-1].ljust(size, pad)
        return bytearray([int(c, 2) for c in chunks])

    def bytes_to_bits(self, byte_array):
        return BitArray(byte_array).bin

    def compress(self):
        # read the input file
        if self.args['input_file'] is not None:
            self.log.info('Reading input file: %s', self.args['input_file'])
            with open(self.args['input_file'], 'r') as f:
                self.args['input_string'] = f.read()
        self.log.debug('Input string: %s', self.args['input_string'])
        # compress the string
        self.log.info('Starting HuffmanEncoder')
        encoder = HuffmanEncoder(self.args['input_string'], self.args['level'], self.log)
        encoded_string = encoder.encode()
        self.log.info('Compression successful')
        self.log.debug('Encoded string: %s', encoded_string)
        self.log.debug('Encoded string length: %s', len(encoded_string))
        self.log.debug('Converting bit sequence to byte array')
        byte_array = self.bits_to_bytes(encoded_string)
        self.log.debug('Byte array: %s', byte_array)
        # write the encoded string to the output file
        self.log.info('Writing output file: %s', self.args['output_file'])
        with open(self.args['output_file'], 'wb') as f:
            f.write(byte_array)

    def decompress(self):
        # read the input file
        if self.args['input_file'] is not None:
            self.log.info('Reading input file: %s', self.args['input_file'])
            with open(self.args['input_file'], 'rb') as f:
                self.args['input_string'] = f.read()
        self.log.debug('Encoded byte array: %s', self.args['input_string'])
        # decompress the string
        self.log.debug('Converting byte array to bit sequence')
        encoded_string = self.bytes_to_bits(self.args['input_string'])
        self.log.debug('Encoded string: %s', encoded_string)
        self.log.debug('Encoded string length: %s', len(encoded_string))
        self.log.info('Starting HuffmanDecoder')
        string = HuffmanDecoder(encoded_string, self.log).decode()
        # write the decoded string to the output file
        self.log.info('Writing output file: %s', self.args['output_file'])
        with open(self.args['output_file'], 'w') as f:
            f.write(string)

    def compression_ratio(self):
        self.log.debug('Calculating compression ratio')
        if self.args['input_file'] is not None:
            uncompressed_size = os.path.getsize(self.args['input_file'])
        else:
            uncompressed_size = len(self.args['input_string'])
        compressed_size = os.path.getsize(self.args['output_file'])
        compression_ratio = compressed_size / uncompressed_size * 100
        self.log.info(f'Compression ratio: {compression_ratio:.2f} %')

    def run(self):
        # initialize
        self.parse_args()
        self.initialize_logger()
        self.check_mode()
        self.check_output_path()
        self.check_output_file()
        # run the appropriate mode
        if self.args['mode'] == 'compression':
            self.compress()
            self.compression_ratio()
        elif self.args['mode'] == 'decompression':
            self.decompress()


def main():
    Interface().run()


if __name__ == '__main__':
    main()
