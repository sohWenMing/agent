# tests.py

import unittest
import os
from functions.get_files_info import get_files_info, get_file_content, write_file_content
# this file is within the main directory, so cwd is the root 


class TestGetFiles(unittest.TestCase):

    def test_get_file_content_error(self):

        inputs = [
            ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
            ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
            ["calculator", "/tmp/temp/txt", "this should not be allowed "],
        ]

        for input in inputs:
            result = write_file_content(input[0],input[1],input[2])
            print(result)


if __name__ == "__main__":
    unittest.main()