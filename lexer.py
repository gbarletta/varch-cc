from defs import TokenType, Token, Location

class Lexer:
  cursor = 0; row = 0; col = 0
  stomach = []; tokens = []

  def __init__(self, file_path, text):
    self.file_path = file_path
    self.text = text

  def eof(self):
    return self.cursor >= len(self.text)
  
  def incr(self, steps=1): # increment cursor while updating current row and col
    for _ in range(0, steps):
      if self.curchar() == "\n":
        self.col = 0
        self.row += 1
      else:
        self.col += 1
      self.cursor += 1

  def eat(self): # eat character and put in stomach
    character = self.text[self.cursor]
    self.stomach.append(character)
    self.incr()
    return character
  
  def digest(self): # digest current eaten characters
    token_string = "".join(self.stomach)
    self.stomach = []
    return token_string
  
  def curchar(self, offset=0):
    position = self.cursor + offset
    if position >= len(self.text):
      raise Exception("eof")
    return self.text[position]
  
  def append(self, token):
    self.tokens.append(token)

  def get_location(self):
    return Location(self.file_path, self.row, self.col)
  
  def lex(self):
    sym_tokens = { # map for cleaner code 
      ";": TokenType.TOKEN_SEMICOL, "*": TokenType.TOKEN_STAR, ",": TokenType.TOKEN_COMMA,
      "(": TokenType.TOKEN_OPAREN, ")": TokenType.TOKEN_CPAREN, "[": TokenType.TOKEN_OBRACK,
      "]": TokenType.TOKEN_CBRACK, "{": TokenType.TOKEN_OCURLY, "}": TokenType.TOKEN_CCURLY,
      ".": TokenType.TOKEN_DOT, "<": TokenType.TOKEN_LTS, ">": TokenType.TOKEN_GTS,
      "?": TokenType.TOKEN_QUEST, "+": TokenType.TOKEN_PLUS, "-": TokenType.TOKEN_DASH,
      "/": TokenType.TOKEN_SLASH, "|": TokenType.TOKEN_VERBAR, "&": TokenType.TOKEN_AMPERS,
      "!": TokenType.TOKEN_EXCL, "=": TokenType.TOKEN_EQUAL,
    }
    while not self.eof():
      # print(self.curchar())
      if self.curchar() == "|" and self.curchar(1) == "|":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_OR, "||", loc))
        continue
      if self.curchar() == "&" and self.curchar(1) == "&":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_AND, "&&", loc))
        continue
      if self.curchar() == "!" and self.curchar(1) == "=":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_NOT_EQUAL, "!=", loc))
        continue
      if self.curchar() == "=" and self.curchar(1) == "=":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_EQUAL_EQUAL, "==", loc))
        continue
      if self.curchar() == ">" and self.curchar(1) == "=":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_GTE, ">=", loc))
        continue
      if self.curchar() == "<" and self.curchar(1) == "=":
        loc = self.get_location()
        self.incr(2)
        self.append(Token(TokenType.TOKEN_LTE, "<=", loc))
        continue
      for sym in sym_tokens.keys():
        if self.curchar() == sym: # one character tokens (see sym_tokens)
          self.append(Token(sym_tokens[sym], sym, self.get_location()))
          self.incr()
          if self.eof():
            return
        continue
      if self.curchar().isspace():
        self.incr()
        continue
      if self.curchar().isalpha(): # names (identifiers)
        loc = self.get_location()
        self.eat()
        while not self.eof() and (self.curchar().isalnum() or self.curchar() == "_"):
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NAME, digest, loc))
        continue
      if self.curchar() == "#": # ignoring preprocessor 
        while not self.eof() and self.curchar() != "\n":
          self.incr()
        continue
      if self.curchar() == "/" and self.text[self.cursor + 1] == '/': # comments 
        while not self.eof() and self.curchar() != "\n":
          self.incr()
        continue
      if self.curchar() == "\"": # string literals
        loc = self.get_location()
        self.incr()
        while not self.eof() and self.curchar() != "\"":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_STRLIT, digest, loc))
        self.incr()
        continue
      if self.curchar() == "'": # character literals
        loc = self.get_location()
        self.incr()
        while not self.eof() and self.curchar() != "'":
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_CHARLIT, digest, loc))
        self.incr()
        continue
      if self.curchar().isnumeric(): # number literals (5, 0b101, 0x5)
        loc = self.get_location()
        self.eat()
        while not self.eof() and (self.curchar().isnumeric() or self.curchar() in ["b", "x", "a", "c", "d", "e", "f"]):
          self.eat()
        digest = self.digest()
        self.append(Token(TokenType.TOKEN_NUMBER, digest, loc))
        continue
      