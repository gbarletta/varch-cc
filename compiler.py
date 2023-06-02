import lexer

class Compiler:
  def __init__(self, file_path):
    self.file_path = file_path
    try:
      with open(file_path, "r") as f:
        self.text = f.read()
    except:
      print(f"ERROR: couldn't open file {file_path}")

  def compile(self):
    lx = lexer.Lexer(self.file_path, self.text)
    lx.lex()

    for token in lx.tokens:
      print(str(token))