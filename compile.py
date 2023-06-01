import lexer

lx = lexer.Lexer("hello.c")
lx.lex()

for token in lx.tokens:
  print(str(token))