# tests.py

import unittest
import os
from functions.functions import get_files_info, get_file_content, write_file_content, run_python_file
# this file is within the main directory, so cwd is the root 


class TestGetFiles(unittest.TestCase):

    def test_run_python_file(self):

        inputs = [
            ["calculator", "main.py"],
            ["calculator", "tests.py"],
            ["calculator", "../main.py"],
            ["calculator", "nonexistent.py"],
        ]

        for input in inputs:
            result = run_python_file(input[0], input[1])
            print(result)


if __name__ == "__main__":
    unittest.main()