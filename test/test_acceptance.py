# this script uses subprocess to call the main_cli.py script
# and test for a real use case. The test consists of the encoding
# and decoding of the three text files in the test directory. The
# following steps are performed:
# 1. load short.txt
# 2. Encode short.txt
# 3. delete short.txt
# 4. Decode short.bin
# 5. load decoded short.txt
# 6. delete short.bin
# 7. Compare the two files

import os
import subprocess
import difflib

# main test function for funtionality
def run_test(file):
    # check if file exists
    if not os.path.isfile('test/' + file):
        raise FileNotFoundError(f'Original file {file} not found!')
    # load
    with open('test/' + file, 'r') as f:
        original = f.read()
    # encode
    subprocess.call(['python3', 'huffman', 'test/' + file, '-o'])
    # check if file exists
    if not os.path.isfile('test/' + file.replace('.txt', '.huff')):
        raise FileNotFoundError(f'Encoded file {file.replace(".txt", ".huff")} not found!')
    # delete
    os.remove('test/' + file)
    # decode
    subprocess.call(['python3', 'huffman', 'test/' + file.replace('.txt', '.huff'), '-o'])
    # check if file exists
    if not os.path.isfile('test/' + file):
        raise FileNotFoundError(f'Decoded file {file} not found!')
    # load
    with open('test/' + file, 'r') as f:
        decoded = f.read()
    # delete
    os.remove('test/' + file.replace('.txt', '.huff'))
    # compare
    if original != decoded:
        # print diff
        diff = difflib.unified_diff(
            original.splitlines(keepends=True), decoded.splitlines(keepends=True)
        )
        print(''.join(diff))
        # raise error
        raise ValueError(f'Original and decoded files {file} are not the same!')


# run tests
run_test('short.txt')
run_test('medium.txt')
run_test('long.txt')
