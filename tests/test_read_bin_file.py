import random
import pathlib
import time
# from pathlib import Path
from functools import partial

# https://stackoverflow.com/questions/1035340/reading-binary-file-and-looping-over-each-byte

BUFF_SIZE = 4096
LINE_SIZE = 16
BIN_FILE_NAME = 'mebibyte.bin'
BIN_FILE_SIZE = 2**20

def dummy_byte_op(b):
    x = b

def test_byte_by_byte():
    with open(BIN_FILE_NAME, "rb") as f:
        while (b := f.read(1)):
            dummy_byte_op(b)

def test_line_by_line():
    with open(BIN_FILE_NAME, "rb") as f:
        while (bs := f.read(LINE_SIZE)):
            for b in bs:
                dummy_byte_op(b)

def test_by_buff():
    with open(BIN_FILE_NAME, "rb") as f:
        while (bs := f.read(BUFF_SIZE)):
            for b in bs:
                dummy_byte_op(b)

def test_by_whole():
    with open(BIN_FILE_NAME, "rb") as f:
        bs = f.read()
        for b in bs:
            dummy_byte_op(b)

def file_byte_iterator(path):
    ''' Return an iterator over the path/file that lazily loads the file.'''
    with open(BIN_FILE_NAME, "rb") as f:
        reader = partial(f.read1, BUFF_SIZE)
        file_iterator = iter(reader, bytes())
        for chunk in file_iterator:
            yield from chunk

def test_by_read1_list():
    # Load into list.
    l = list(file_byte_iterator(BIN_FILE_NAME))
    for b in l:
        dummy_byte_op(b)

def test_by_read1_iterator():
    # Direct iterator access.
    for b in file_byte_iterator(BIN_FILE_NAME):
        dummy_byte_op(b)

from mmap import ACCESS_READ, mmap
def test_by_mmap():
    with open(BIN_FILE_NAME, "rb") as f, mmap(f.fileno(), 0, access=ACCESS_READ) as s:
        for b in s: # length is equal to the current file size
            dummy_byte_op(b)

def create_test_file():
    path = BIN_FILE_NAME
    pathobj = pathlib.Path(path)
    pathobj.write_bytes(bytes(random.randint(0, 255) for _ in range(BIN_FILE_SIZE)))

def do_test(func, func_name):
    start_time = time.perf_counter_ns()
    func()
    print(f'{func_name}: {(time.perf_counter_ns() - start_time) / 1000000}')

def do_tests():
    do_test(test_by_buff, 'test_by_buff')
    do_test(test_by_read1_iterator, 'test_by_read1_iterator')
    do_test(test_by_read1_list, 'test_by_read1_list')
    do_test(test_by_whole, 'test_by_whole')
    do_test(test_by_mmap, 'test_by_mmap')
    do_test(test_byte_by_byte, 'test_byte_by_byte')
    do_test(test_line_by_line, 'test_line_by_line')

    # test_by_buff: 22.7209
    # test_by_read1_iterator: 32.4184
    # test_by_read1_list: 53.5
    # test_by_whole: 23.4898
    # test_by_mmap: 28.689
    # test_byte_by_byte: 43.8904
    # test_line_by_line: 31.3826

do_tests()
