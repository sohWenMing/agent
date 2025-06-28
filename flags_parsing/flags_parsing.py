import argparse

def init_parser():
    parser = argparse.ArgumentParser(
                        prog="python3 main.py",
                        description="This is a practice tool - to help you get your heard around how chatbots actually work",
                        epilog="")

    parser.add_argument("-v", 
                        "--verbose",
                        action="store_true",
                        help="add verbose information during the execution of the program")
    # action = store true is to ensure that the flag itself is used as a boolean, doesn't need other arguments
    return parser

class Parser:
    def __init__(self):
        self.parser = init_parser()
        self.args = None
    
    def parse_args(self):
        self.args = self.parser.parse_args()
    
    def is_verbose(self):
        self.parse_args()
        if self.args == None:
            return False
        return self.args.verbose