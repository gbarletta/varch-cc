import json
from enum import IntEnum

class TokenType(IntEnum):
  TOKEN_NAME = 0,
  TOKEN_NUMBER = 1,
  TOKEN_OPAREN = 2,
  TOKEN_CPAREN = 3,
  TOKEN_OBRACK = 4,
  TOKEN_CBRACK = 5,
  TOKEN_OCURLY = 6,
  TOKEN_CCURLY = 7,
  TOKEN_HASH = 8,
  TOKEN_PLUS = 9,
  TOKEN_DASH = 10,
  TOKEN_SQUOTE = 11,
  TOKEN_DQUOTE = 12,
  TOKEN_GTS = 13,
  TOKEN_LTS = 14,
  TOKEN_EQUAL = 15,
  TOKEN_DOT = 16,
  TOKEN_COMMA = 17,
  TOKEN_STAR = 18,
  TOKEN_SEMICOL = 19,
  TOKEN_STRLIT = 20,
  TOKEN_CHARLIT = 21,
  TOKEN_RETURN = 22,
  TOKEN_TYPEINT = 23,
  TOKEN_TYPECHAR = 24,
  TOKEN_IF = 25,
  TOKEN_WHILE = 26,
  TOKEN_FOR = 27,
  TOKEN_QUEST = 28,
  TOKEN_CONST = 29,
  TOKEN_SLASH = 30,
  TOKEN_TYPEVOID = 31,
  TOKEN_VERBAR = 32,
  TOKEN_AMPERS = 33,
  TOKEN_OR = 34,
  TOKEN_AND = 35,
  TOKEN_NOT_EQUAL = 36,
  TOKEN_GTE = 37,
  TOKEN_LTE = 38,
  TOKEN_EXCL = 39,
  TOKEN_TRUE = 40,
  TOKEN_FALSE = 41,
  TOKEN_ELSE = 42,
  TOKEN_EQUAL_EQUAL = 43,

token_names = [
  "Name",
  "Number",
  "Open Parentheses",
  "Close Parentheses",
  "Open Bracket",
  "Close Bracket",
  "Open Curly",
  "Close Curly",
  "Hash",
  "Plus",
  "Dash",
  "Single Quote",
  "Double Quote",
  "Greater-than",
  "Less-than",
  "Equal",
  "Dot",
  "Comma",
  "Star",
  "Semicolon",
  "String Literal",
  "Character Literal",
  "Return",
  "Int Type",
  "Char Type",
  "If",
  "While",
  "For",
  "Question Mark",
  "Constant",
  "Slash",
  "Void Type",
  "Vertical Bar",
  "Ampersand",
  "Or",
  "And",
  "Not Equal",
  "Greater-than Or Equal",
  "Less-than Or Equal",
  "Exclamative Point",
  "True",
  "False",
  "Else",
  "Equal Equal",
]

class AstNodeType(IntEnum):
  PROGRAM = 0,
  BLOCK = 1,
  STATEMENT = 2,
  EXPRESSION = 3,
  SUM = 4,
  SUBTRACT = 5,
  MULTIPLY = 6,
  DIVIDE = 7,
  IDENTIFIER = 8,
  FUNCTION_CALL = 9,
  FUNCTION_CALL_ARGS = 10,
  FUNCTION_CALL_CALLEE = 11,
  VARIABLE_DECLARATION = 12,
  FUNCTION_DECLARATION = 13,
  PARAMETERS_FUNCTION_DECLARATION = 14,
  FUNCTION_DECLARATION_BODY = 15,
  RETURN = 16,
  NUMBER_LITERAL = 17,
  STRING_LITERAL = 18,
  TRUE_LITERAL = 19,
  FALSE_LITERAL = 20,
  NEGATE = 21,
  MINUS = 22,
  GREATER_THAN = 23,
  LESS_THAN = 24,
  GREATER_EQUAL_THAN = 25,
  LESS_EQUAL_THAN = 26,
  EQUAL = 27,
  NOT_EQUAL = 28,
  POINTER = 29,
  ASSIGNMENT = 30,
  IF = 31,
  CONDITION = 32,
  IF_BODY = 33,
  ELSE_BODY = 34,
  WHILE = 35,
  WHILE_BODY = 36,
  FOR = 37,
  FOR_INITIALIZATION = 38,
  FOR_STEP = 39,
  FOR_BODY = 40,
  AND = 41,
  OR = 42,
  ARRAY_ACCESS = 43,
  VARIABLE_DECLARATION_EXPR = 44,
  GLOBAL_VARIABLE_DECLARATION = 45,
  CHAR_LITERAL = 46,
  POINTER_ASSIGNMENT = 47,
  POINTER_ASSIGNMENT_ADDR = 48,
  POINTER_ASSIGNMENT_EXPR = 49,
  POINTER_ADDRESS = 50,

ast_names = [
  "Program", 
  "Block",
  "Statement",
  "Expression",
  "Sum",
  "Subtract",
  "Multiply",
  "Divide",
  "Identifier",
  "Function Call",
  "Arguments for Function Call",
  "Function Call Callee",
  "Variable Declaration",
  "Function Declaration",
  "Parameters for Function Declaration",
  "Function Declaration Body",
  "Return",
  "Number Literal",
  "String Literal",
  "True Literal",
  "False Literal",
  "Negate",
  "Minus",
  "Greater Than",
  "Less Than",
  "Greater Or Equal Than",
  "Less Or Equal Than",
  "Equal",
  "Not Equal",
  "Pointer",
  "Assignment",
  "If",
  "Condition",
  "If Body",
  "Else Body",
  "While",
  "While Body",
  "For",
  "For Initialization",
  "For Step",
  "For Body",
  "And",
  "Or",
  "Array Access",
  "Variable Declaration Expression",
  "Global Variable Declaration",
  "Char Literal",
  "Pointer Assignment",
  "Pointer Assignment Address",
  "Pointer Assignment Expression",
  "Pointer Address",
]

class IdentifierType(IntEnum):
  INVALID = -1,
  VOID = 0,
  VOID_PTR = 1,
  INT = 2,
  INT_PTR = 3,
  CHAR = 4,
  CHAR_PTR = 5,
  INT_ARR = 6,
  CHAR_ARR = 7,
  VOID_PTR_ARR = 8,
  INT_PTR_ARR = 9,
  CHAR_PTR_ARR = 10,

identifier_type_names = [
  "Void",
  "Pointer To Void",
  "Integer",
  "Pointer To Integer",
  "Character",
  "Pointer To Character",
  "Array Of Integers",
  "Array Of Characters",
  "Array Of Void Pointers",
  "Array Of Integer Pointers",
  "Array Of Character Pointers",
]

class TypeInfo:
  def __init__(self, identifier_type, size):
    self.type = identifier_type
    self.size = size

  def __str__(self):
    return f"{identifier_type_names[self.type]}, Size: {self.size}"
    
class Location:
  def __init__(self, file_path, row, col):
    self.file_path = file_path
    self.row = row + 1
    self.col = col + 1

  def __str__(self):
    return f"{self.file_path}:{self.row}:{self.col}"
  
class Token:
  def __init__(self, token_type, text, location):
    if token_type == TokenType.TOKEN_NAME:
      match text:
        case "return":
          self.type = TokenType.TOKEN_RETURN
        case "int":
          self.type = TokenType.TOKEN_TYPEINT
        case "char":
          self.type = TokenType.TOKEN_TYPECHAR
        case "void":
          self.type = TokenType.TOKEN_TYPEVOID
        case "if":
          self.type = TokenType.TOKEN_IF
        case "while":
          self.type = TokenType.TOKEN_WHILE
        case "for":
          self.type = TokenType.TOKEN_FOR
        case "const":
          self.type = TokenType.TOKEN_CONST
        case "true":
          self.type = TokenType.TOKEN_TRUE
        case "false":
          self.type = TokenType.TOKEN_FALSE
        case "else":
          self.type = TokenType.TOKEN_ELSE
        case _:
          self.type = TokenType.TOKEN_NAME
    else:
      self.type = token_type
    self.text = text
    self.location = location

  def is_type(self):
    match self.type:
      case TokenType.TOKEN_TYPEINT | TokenType.TOKEN_TYPECHAR | TokenType.TOKEN_TYPEVOID:
        return True
      case _:
        return False
  
  def __str__(self):
    return f"{self.location}: {token_names[self.type]} \"{self.text}\""

class AstNode:
  def __init__(self, node_type, location=None, metadata=None):
    self.type = node_type
    self.location = location
    self.metadata = metadata
    self.children = []

  def append(self, ast_node):
    self.children.append(ast_node)

  def extend(self, ast_nodes):
    self.children.extend(ast_nodes)

  def print(self, prefix=""):
    print(f"{prefix}└── {self}")
    prefix = prefix + "    "
    for child in self.children:
      child.print(prefix)

  def print_post(self):
    for child in self.children:
      child.print_post()
    print(self)

  def __str__(self):
    out = f"{self.location}: {ast_names[self.type]}"
    if self.metadata != None:
      for meta in self.metadata.keys():
        out += f", [{meta}: {self.metadata[meta]}]"
    return out
  
  def generate(self, codegen):
    for child in self.children:
      child.generate(codegen)
    codegen.process(self)

class CompilerError(Exception):
  def __init__(self, astgen, message, offset=0):
    self.location = astgen.get_current_location(offset=offset)
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f"{self.message} at {self.location}"