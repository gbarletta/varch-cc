import os
import sys
import compiler

cwd = os.getcwd()
file_path = sys.argv[1]

cc = compiler.Compiler(cwd + '/' + file_path)
cc.compile()
