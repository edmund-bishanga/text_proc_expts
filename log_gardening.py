#!usr/bin/python

# log gardening module

# primary APIs
# + read_chunks
# + read_lines
# + readlog_tail
# + readlog_head
# + search_printlines
# + search_countlines
# + logsize_numlines
# + logsize_numbytes
# + logdate_created
# + logdate_lastmodified

import sys
import pytest
from pprint import pprint

args = sys.argv[1:]
if not args:
    args = ['./sample_service_log.txt']
assert len(args) >= 1,'Please provide at least one arg: "filepath"'

logfile_path = args[0] if args else "./sample_service_log.txt"

def readlog_chunks(logfile_path, chunksize=1024):
    with open(logfile_path, 'r') as f:
        while True:
            # read in memory-efficient chunks
            chunk = f.read(chunksize)
            if not chunk:
                break
            yield chunk

def printlog_lines(logfile_path):
    assert type(logfile_path) == str
    file_generator = (line.strip() for line in open(logfile_path, 'r'))
    for line in file_generator:
        if line and line[0].isalnum():
            print("{}".format(line))

def readlog_tail(logfile_path, numbytes=100):
    assert type(numbytes) == int, "numbytes: expects: +ve number"
    with open(logfile_path, 'rb') as f:
        tail = f.read(f.seek(-numbytes, 2))
    return tail

def  readlog_head(logfile_path, numbytes=100):
    assert type(numbytes) == int and numbytes > 0, "numbytes: expects: +ve int"
    with open(logfile_path, 'rb') as f:
        head = f.read(numbytes)
    return head

def readlog_offsetchunk(logfile_path, offset=0, numbytes=100):
    assert type(offset) == int and type(numbytes) == int
    assert numbytes > 0, "numbytes: expects: +ve int"
    with open(logfile_path, 'rb') as f:
        f.seek(offset)
        chunk = f.read(f.seek(numbytes, 1))
    return chunk

valid_logfilepath = logfile_path
invalid_numbytes = [-100, 100000000000, 0, -1]
def test_readlog_head_invalid_input(valid_logfilepath, invalid_numbytes):
    # input validation
    print('started: inputs: {} {}'.format(valid_logfilepath, invalid_numbytes))
    # main 
    with pytest.raises(AssertionError) as exec_info:
        output = readlog_head(valid_logfilepath, invalid_numbytes)
        print('output:\n{}'.format(output))
    pprint(exec_info)
    assert 'numbytes' in exec_info.value

    # output verification
    print('done')