import traceback
from defs import TokenType, Token, AstNodeType, IdentifierType, AstNode, Location, CompilerError, token_names, TypeInfo
from treelib import Node, Tree
from functools import wraps

class CodeGen:
  def __init__(self, file_path):
    self.code = f"# {file_path}\n"
  
  def process(self, ast_node):
    print(ast_node)

  def __str__(self):
    return self.code