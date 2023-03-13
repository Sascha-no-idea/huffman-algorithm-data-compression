import argparse
import logging
import os
from bitstring import BitArray

from main import HuffmanEncoder, HuffmanDecoder


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
        # set formatter and file handler
        log_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler('log.txt', mode='w')
        file_handler.setFormatter(log_formatter)
        self.log.addHandler(file_handler)
        # test logger
        self.log.info('Logger initialized')
        return

    def check_input(self):
        # check if the input file exists
        if not os.path.exists(self.args['input_file']):
            self.log.error('Input file not found: %s', self.args['input_file'])
            raise FileNotFoundError('Input file not found')
        # check if output file already exists
        if os.path.exists(self.args['output_file']) and not self.args['overwrite']:
            self.log.error('Output file already exists: %s', self.args['output_file'])
            raise FileExistsError(
                'Output file already exists. Please delete it first or set the --overwrite flag.'
            )
        # check if the compression level is valid
        if self.args['level'] in [1, 2]:
            self.log.info('Compression level set to %s', self.args['level'])
        else:
            self.log.error('Invalid compression level: %s', self.args['level'])
            raise ValueError('Invalid compression level')

    def check_mode(self):
        if self.args['input_file'].endswith('.txt'):
            self.args['mode'] = 'compression'
            self.args['output_file'] = self.args['input_file'].replace('.txt', '.bin')
        elif self.args['input_file'].endswith('.bin'):
            self.args['mode'] = 'decompression'
            self.args['output_file'] = self.args['input_file'].replace('.bin', '.txt')
        else:
            self.log.error('Invalid file extension: %s', self.args['input_file'])
            raise ValueError('Invalid file extension')

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
        with open(self.args['input_file'], 'r') as f:
            string = f.read()
        # compress the string
        encoder = HuffmanEncoder(string, self.args['level'], self.log)
        encoded_string = encoder.encode()
        byte_array = self.bits_to_bytes(encoded_string)
        # write the encoded string to the output file
        with open(self.args['output_file'], 'wb') as f:
            f.write(byte_array)

    def decompress(self):
        # read the input file
        with open(self.args['input_file'], 'rb') as f:
            encoded_bytes = f.read()
        # decompress the string
        encoded_string = self.bytes_to_bits(encoded_bytes)
        string = HuffmanDecoder(encoded_string, self.log).decode()
        # write the decoded string to the output file
        with open(self.args['output_file'], 'w') as f:
            f.write(string)

    def compression_ratio(self):
        uncompressed_size = os.path.getsize(self.args['input_file'])
        compressed_size = os.path.getsize(self.args['output_file'])
        compression_ratio = uncompressed_size / compressed_size * 100
        self.log.info('Compression ratio: %s %', compression_ratio)

    def run(self):
        # initialize
        self.parse_args()
        self.initialize_logger()
        self.check_mode()
        self.check_input()
        # run the appropriate mode
        if self.args['mode'] == 'compression':
            self.compress()
            self.compression_ratio()
        elif self.args['mode'] == 'decompression':
            self.decompress()


if __name__ == '__main__':
    Interface().run()
