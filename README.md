# huffman-algorithm-data-compression
This is a Python implementation of the Huffman algorithm for data compression. This implementation allows for the compression of ASCII code from a text file as binary file with different levels of compression, and decompression of the binary file back to the original text file. It was implemented as part of a university assignment for the course "Intoduction into Optimization" at the Berlin University of Applied Sciences ([BHT](https://www.bht-berlin.de/)) of [Department II](https://www.bht-berlin.de/ii).

## Installation
```bash
pip install -r requirements.txt
```
## Usage
### Compress
```bash
python main.py -i <input_file_name>.txt
```
### Decompress
```bash
python main.py -i <input_file_name>.bin
```
### Options
- `-o, --overwrite` Overwrite the output file if it already exists
- `-l, --level` Set the compression level (default: 1)
    - 1: Huffman Coding with single character encoding
    - 2: Huffman Coding with multi character encoding
- `-v, --verbose` Print verbose output 
- `-d, --debug` Print debug output
- `-h, --help` Print help message
### Run Unit Tests
```bash
cd huffman-algorithm-data-compression
python -m unittest test.test_main
```