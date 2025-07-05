# tests.py

import unittest
import os
from functions.get_files_info import get_files_info
# this file is within the main directory, so cwd is the root 


class TestGetFiles(unittest.TestCase):
    def test_directory_not_in_working_directory(self):
        inputs = [
            "../",
            "booger"
        ]
        for input in inputs:
            result = get_files_info(os.getcwd(), input)
            self.assertEqual(result,
                f'Error: Cannot list "{input}" as it is outside the permitted working directory'
                )
    
    def test_is_not_a_directory(self):
        inputs = [
            "main.py",
            "tests.py"
        ]
        for input in inputs:
            result = get_files_info(os.getcwd(), input)
            self.assertEqual(result,
                f'Error: "{input}" is not a directory'
                )

    def test_directory_in_working_directory(self):
        inputs = [
            "functions", 
            "calculator",
        ]
        for input in inputs:
            result = get_files_info(os.getcwd(), input)
            self.assertEqual(result, "ok, this is a directory in the cwd")

if __name__ == "__main__":
    unittest.main()