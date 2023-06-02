from defs import TokenType, Token, Location

class Lexer:
  cursor = 0; row = 0; col = 0
  stomach = []; tokens = []

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

  def get_location(self):
    return Location(self.file_path, self.row, self.col)

  def lex(self):
    sym_tokens = {
      ";": TokenType.TOKEN_SEMICOL, "*": TokenType.TOKEN_STAR, ",": TokenType.TOKEN_COMMA,
      "(": TokenType.TOKEN_OPAREN, ")": TokenType.TOKEN_CPAREN, "[": TokenType.TOKEN_OBRACK,
      "]": TokenType.TOKEN_CBRACK, "{": TokenType.TOKEN_OCURLY, "}": TokenType.TOKEN_CCURLY,
      ".": TokenType.TOKEN_DOT, "<": TokenType.TOKEN_LTS, ">": TokenType.TOKEN_GTS,
      "#": TokenType.TOKEN_HASH, "?": TokenType.TOKEN_QUEST,
    }
    while not self.eof():
      for sym in sym_tokens.keys():
        if self.curchar() == sym:
          self.append(Token(sym_tokens[sym], sym, self.get_location()))
          self.incr()
          if self.eof():
            return
      if self.curchar().isspace():
        self.incr()
        continue
      if self.curchar().isalpha():
        loc = self.get_location()
        self.eat()
        while not self.eof() and self.curchar().isalnum():
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NAME, digest, loc))
        continue
      if self.curchar() == "\"":
        loc = self.get_location()
        self.incr()
        while not self.eof() and self.curchar() != "\"":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_STRLIT, digest, loc))
        self.incr()
        continue
      if self.curchar() == "'":
        loc = self.get_location()
        self.incr()
        while not self.eof() and self.curchar() != "'":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_CHARLIT, digest, loc))
        self.incr()
        continue
      if self.curchar().isnumeric():
        loc = self.get_location()
        self.eat()
        while not self.eof() and (self.curchar().isnumeric() or self.curchar() in ["b", "x"]):
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NUMBER, digest, loc))
        continue
      