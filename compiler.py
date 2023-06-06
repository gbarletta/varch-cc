import lexer
import astgen

class Compiler:
  def __init__(self, file_path):
    self.file_path = file_path
    try:
      with open(file_path, "r") as f:
        self.text = f.read()
    except:
      print(f"ERROR: couldn't open file {file_path}")

  def compile(self):
    lex = lexer.Lexer(self.file_path, self.text)
    lex.lex()

    parser = astgen.AstGen(lex.tokens)
    parser.generate()