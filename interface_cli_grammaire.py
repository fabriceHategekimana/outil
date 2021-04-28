from cmd import Cmd
from module_compile import *
import re

class CliGrammaire(Cmd):
    prompt = 'grammar>'
    use_raw_input= False

    def do_exit(self, inp):
        return True

    def default(self, inp):
        parser.parse(inp,debug=True)
        f = open("res.txt", "r")
        for line in f:
            print(line)

