# huffman-algorithm-data-compression
This is a Python implementation of the Huffman algorithm for data compression. This implementation allows for the compression of ASCII code from a text file as binary file with different levels of compression, and decompression of the binary file back to the original text file. It was implemented as part of a university assignment for the course "Intoduction into Optimization" at the Berlin University of Applied Sciences ([BHT](https://www.bht-berlin.de/)) of [Department II](https://www.bht-berlin.de/ii).

## Installation
```bash
pip install -r requirements.txt
```
## Usage
### Compress
```bash
python huffman <input_file_name>.txt  # output to stdout
python huffman <input_file_name>.txt -o  # output to default file name
python huffman <input_file_name>.txt -o <output_file_name>.huff
cat <input_file_name>.txt | python huffman
cat <input_file_name>.txt | python huffman -o
cat <input_file_name>.txt | python huffman -o <output_file_name>.huff
echo <input_string> | python huffman
echo <input_string> | python huffman -o
echo <input_string> | python huffman -o <output_file_name>.huff
```
### Decompress
```bash
python huffman <input_file_name>.huff
python huffman <input_file_name>.huff -o
python huffman <input_file_name>.huff -o <output_file_name>.txt
python huffman <input_file_name>.huff > <output_file_name>.txt
```
### Options
- `-o, --output-file` Specify the output file name
- `-f, --force` Overwrite existing output file
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