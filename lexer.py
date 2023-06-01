from enum import IntEnum

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
]

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
        case _:
          self.type = TokenType.TOKEN_NAME
          pass
    else:
      self.type = token_type
    self.text = text
    self.location = location
  
  def __str__(self):
    return f"{self.location}: {token_names[self.type]} \"{self.text}\""

class Lexer:
  cursor = 0
  row = 0
  col = 0
  stomach = []
  tokens = []

  def __init__(self, file_path):
    self.file_path = file_path
    try:
      with open(file_path, "r") as f:
        self.text = f.read()
    except:
      print(f"ERROR: couldn't open file {file_path}")
  
  def eof(self):
    return self.cursor >= len(self.text)
  
  def incr(self):
    if self.curchar() == "\n":
      self.col = 0
      self.row += 1
    else:
      self.col += 1
    self.cursor += 1

  def eat(self):
    character = self.text[self.cursor]
    self.stomach.append(character)
    self.incr()
    return character
  
  def digest(self):
    token_string = "".join(self.stomach)
    self.stomach = []
    return token_string
  
  def curchar(self):
    return self.text[self.cursor]
  
  def append(self, token):
    self.tokens.append(token)

  def get_location(self, token_length=0):
    return Location(self.file_path, self.row, self.col - token_length)

  def lex(self):
    while not self.eof():
      print(f"Current char: {self.curchar()}")
      if self.curchar() == ";":
        self.append(Token(TokenType.TOKEN_SEMICOL, ";", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "*":
        self.append(Token(TokenType.TOKEN_STAR, "*", self.get_location()))
        self.incr()
        continue
      if self.curchar() == ",":
        self.append(Token(TokenType.TOKEN_COMMA, ",", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "(":
        self.append(Token(TokenType.TOKEN_OPAREN, "(", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "[":
        self.append(Token(TokenType.TOKEN_OBRACK, "[", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "]":
        self.append(Token(TokenType.TOKEN_CBRACK, "]", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "{":
        self.append(Token(TokenType.TOKEN_OCURLY, "{", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "}":
        self.append(Token(TokenType.TOKEN_CCURLY, "}", self.get_location()))
        self.incr()
        continue
      if self.curchar() == ")":
        self.append(Token(TokenType.TOKEN_CPAREN, ")", self.get_location()))
        self.incr()
        continue
      if self.curchar() == ".":
        self.append(Token(TokenType.TOKEN_DOT, ".", self.get_location()))
        self.incr()
        continue
      if self.curchar() == "<":
        self.append(Token(TokenType.TOKEN_LTS, "<", self.get_location()))
        self.incr()
        continue
      if self.curchar() == ">":
        self.append(Token(TokenType.TOKEN_GTS, ">", self.get_location()))
        self.incr()
        continue
      if self.curchar().isspace():
        self.incr()
        continue
      if self.curchar() == "#":
        self.append(Token(TokenType.TOKEN_HASH, "#", self.get_location()))
        self.incr()
        continue
      if self.curchar().isalpha():
        self.eat()
        while not self.eof() and self.curchar().isalnum():
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NAME, digest, self.get_location(token_length=len(digest))))
        continue
      if self.curchar() == "\"":
        self.incr()
        while not self.eof() and self.curchar() != "\"":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_STRLIT, digest, self.get_location(token_length=len(digest))))
        self.incr()
        continue
      if self.curchar() == "'":
        self.incr()
        while not self.eof() and self.curchar() != "'":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_CHARLIT, digest, self.get_location(token_length=len(digest))))
        self.incr()
        continue
      if self.curchar().isnumeric():
        self.eat()
        while not self.eof() and (self.curchar().isnumeric() or self.curchar() == "."):
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NUMBER, digest, self.get_location(token_length=len(digest))))
        continue
    
  def print(self):
    print(self.text)
      