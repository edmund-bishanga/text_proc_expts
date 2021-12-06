#!/usr/bin/python

"""
log gardening module:
Often SysTest Experiments generate logs
These need to be post-processed and analysed
This module aims to have re-usable methods for doing just that...
"""

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring

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
from pprint import pprint

import pytest

MEM_LIMIT = 10000
DEF_LOGFILE = "./logs/sample_service_log.txt"


args = sys.argv[1:]
# assert len(args) >= 1,'Please provide at least one arg: "log_filepath"'
logfile_path = args[0] if args else DEF_LOGFILE

def readlog_chunks(logfile_path, chunksize=1024):
    with open(logfile_path, 'r') as f:
        while True:
            # read in memory-efficient chunks
            chunk = f.read(chunksize)
            if not chunk:
                break
            yield chunk

def printlog_lines(logfile_path):
    assert isinstance(logfile_path, str)
    file_generator = (line.strip() for line in open(logfile_path, 'r'))
    for line in file_generator:
        if line and line[0].isalnum():
            print("{}".format(line))

def printlog_lines_head(logfile_path, num_lines=10):
    assert isinstance(logfile_path, str)
    file_generator = (line.strip() for line in open(logfile_path, 'r'))
    line_num = 0
    for line in file_generator:
        line_num = line_num + 1
        print('{}: {}'.format(line_num, line))
        if line_num == num_lines:
            break

def readlog_tail(logfile_path, numbytes=100):
    assert isinstance(numbytes, int) and numbytes > 0, "numbytes: expects: +ve integer"
    with open(logfile_path, 'rb') as f:
        tail = f.read(f.seek(-numbytes, 2))
    return tail

def  readlog_head(logfile_path, numbytes=100):
    assert isinstance(numbytes, int) and numbytes > 0, "numbytes: expects: +ve int"
    head = ''
    try:
        with open(logfile_path, 'rb') as f:
            # head = f.read(numbytes) if numbytes < MEM_LIMIT else None
            head = f.read(numbytes)
    except FileNotFoundError as io_err:
        print(io_err)
    except MemoryError as mem_err:
        pprint(mem_err)
        err_details = 'numbytes: {} >> mem_limit: {}'.format(numbytes, MEM_LIMIT)
        print('MemoryError: ', err_details)
    else:
        if head is None:
            print('Error: empty output, probably a MemoryError')
    return head

def readlog_offsetchunk(logfile_path, offset=0, numbytes=100):
    assert isinstance(offset, int) and isinstance(numbytes, int)
    assert numbytes > 0, "numbytes: expects: +ve int"
    with open(logfile_path, 'rb') as f:
        f.seek(offset)
        chunk = f.read(f.seek(numbytes, 1))
    return chunk

invalid_numbytes = [-100, 100000000000, 0, -1]
# @pytest.mark.skip(reason="not in appropriate syntactic format")
@pytest.mark.parametrize('invalid_bytnum', invalid_numbytes)
def test_readlog_head_invalid_input(invalid_bytnum):
    with pytest.raises(AssertionError) as exec_info:
        output = readlog_head(DEF_LOGFILE, invalid_bytnum)
        pprint(repr(exec_info))
        assert 'numbytes' in exec_info.value or output

invalid_options = ['123', 'abc', '~', './sample_service_log.txt']
@pytest.mark.parametrize("logfile_path", invalid_options)
def test_readlog_tail_invalid_path(logfile_path):
    print('Testing: {}'.format(logfile_path))
    with pytest.raises(FileNotFoundError):
        readlog_tail(logfile_path)
