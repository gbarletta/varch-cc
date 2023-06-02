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
]

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
        case "if":
          self.type = TokenType.TOKEN_IF
        case "while":
          self.type = TokenType.TOKEN_WHILE
        case "for":
          self.type = TokenType.TOKEN_FOR
        case _:
          self.type = TokenType.TOKEN_NAME
    else:
      self.type = token_type
    self.text = text
    self.location = location
  
  def __str__(self):
    return f"{self.location}: {token_names[self.type]} \"{self.text}\""