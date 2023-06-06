import traceback
from defs import TokenType, Token, AstNodeType, IdentifierType, AstNode, Location, CompilerError, token_names
from treelib import Node, Tree
from functools import wraps

def debug(num_tokens):
  def decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
      for i in range(num_tokens):
        print(self.peek(i))
      return func(self, *args, **kwargs)
    return wrapper
  return decorator

class AstGen:
  cursor = 0

  def __init__(self, tokens):
    self.tokens = tokens

  def eof(self):
    return self.cursor >= len(self.tokens)

  def incr(self, offset=1):
    self.cursor += offset

  def peek(self, offset=0):
    position = self.cursor + offset
    if position >= len(self.tokens):
      raise CompilerError(self, "eof")
    return self.tokens[position]
  
  def get_current_location(self, offset=0):
    position = self.cursor + offset
    if position >= len(self.tokens):
      raise CompilerError(self, "eof")
    return self.tokens[position].location
  
  def parse_identifier(self):
    t0 = self.peek()
    if t0.type != TokenType.TOKEN_NAME:
      raise CompilerError(self, "expected identifier")
    self.incr()
    return t0.text
  
  def parse_type(self):
    t0 = self.peek(0)
    t1 = self.peek(1)
    if t1.type != TokenType.TOKEN_STAR:
      self.incr()
      match t0.type:
        case TokenType.TOKEN_TYPEINT:
          return IdentifierType.INT
        case TokenType.TOKEN_TYPECHAR:
          return IdentifierType.CHAR
        case TokenType.TOKEN_TYPEVOID:
          return IdentifierType.VOID
        case _:
          raise CompilerError(self, "expected type")
    else:
      self.incr(2)
      match t0.type:
        case TokenType.TOKEN_TYPEINT:
          return IdentifierType.INT_PTR
        case TokenType.TOKEN_TYPECHAR:
          return IdentifierType.CHAR_PTR
        case TokenType.TOKEN_TYPEVOID:
          return IdentifierType.VOID_PTR
        case _:
          raise CompilerError(self, "expected type")
        
  def parse_parameters(self):
    if self.peek().type != TokenType.TOKEN_OPAREN:
      raise CompilerError(self, "expected \"(\"")
    parameters = []
    self.incr()
    while not self.eof():
      identifier_type = self.parse_type()
      identifier_name = self.parse_identifier()
      parameters.append({"name": identifier_name, "type": identifier_type})
      if self.peek().type == TokenType.TOKEN_COMMA:
        self.incr()
        continue
      elif self.peek().type != TokenType.TOKEN_CPAREN:
        raise CompilerError(self, "expected \")\" for function declaration")
      else:
        break
    self.incr()
    return parameters
  
  def parse_decl(self):
    location = self.peek().location
    identifier_type = self.parse_type()
    identifier_name = self.parse_identifier()
    match self.peek().type:
      case TokenType.TOKEN_SEMICOL:
        self.incr()
        return AstNode(
          AstNodeType.VARIABLE_DECLARATION,
          location,
          {"name": identifier_name, "type": identifier_type},
        )
      case TokenType.TOKEN_OPAREN:
        parameters = self.parse_parameters()
        if self.peek().type != TokenType.TOKEN_SEMICOL:
          raise CompilerError(self, "expected ;")
        self.incr()
        return AstNode(
          AstNodeType.FUNCTION_DECLARATION,
          location,
          {"parameters": parameters},
        )
      case _:
        raise CompilerError(self, f"unexpected \"{self.peek().text}\" token")
    
  def generate(self):
    try:
      while not self.eof():
        print(self.parse_decl())
    except CompilerError as compiler_error:
      # traceback.print_exc()
      print(str(compiler_error))