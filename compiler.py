import lexer
import astgen
import codegen

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

    parser = astgen.AstGen(self.file_path, lex.tokens)
    parser.parse()

    gen = codegen.CodeGen(self.file_path)
    parser.print()
    gen.process(parser.program)

    with open(f"{self.file_path.replace('.c', '.s')}", "w") as f:
      f.write(str(gen))
    
    # print(gen)