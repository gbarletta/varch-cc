import traceback
from defs import TokenType, Token, AstNodeType, IdentifierType, AstNode, Location, CompilerError, token_names, TypeInfo
from treelib import Node, Tree
from functools import wraps

def debug(num_tokens):
  def decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
      if False:
        print(func.__name__)
        print(self.peek())
      return func(self, *args, **kwargs)
    return wrapper
  return decorator

class AstGen:
  cursor = 0

  def __init__(self, file_path, tokens):
    self.file_path = file_path
    self.tokens = tokens
    self.program = None

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
  
  def expect_token(self, token_type, incr=True):
    token = self.peek()
    if token.type != token_type:
      raise CompilerError(self, f"expected \"{token_names[token_type]}\"")
    if incr:
      self.incr()
    return token
  
  @debug(0)
  def parse_identifier(self):
    t0 = self.peek()
    if t0.type != TokenType.TOKEN_NAME:
      raise CompilerError(self, "expected identifier")
    self.incr()
    return t0.text
  
  @debug(0)
  def parse_type(self):
    t0 = self.peek(0)
    t1 = self.peek(1)
    if t1.type == TokenType.TOKEN_STAR:
      self.incr(2)
      match t0.type:
        case TokenType.TOKEN_TYPEINT:
          return TypeInfo(IdentifierType.INT_PTR, 2)
        case TokenType.TOKEN_TYPECHAR:
          return TypeInfo(IdentifierType.CHAR_PTR, 2)
        case TokenType.TOKEN_TYPEVOID:
          return TypeInfo(IdentifierType.VOID_PTR, 2)
        case _:
          raise CompilerError(self, "expected type")
    else:
      self.incr()
      match t0.type:
        case TokenType.TOKEN_TYPEINT:
          return TypeInfo(IdentifierType.INT, 2)
        case TokenType.TOKEN_TYPECHAR:
          return TypeInfo(IdentifierType.CHAR, 1)
        case TokenType.TOKEN_TYPEVOID:
          return TypeInfo(IdentifierType.VOID, 1)
        case _:
          raise CompilerError(self, "expected type")

  @debug(0)     
  def parse_primary(self):
    location = self.peek().location
    match self.peek().type:
      case TokenType.TOKEN_NAME:
        identifier_node = AstNode(
          AstNodeType.IDENTIFIER,
          location,
          {"name": self.peek().text},
        )
        self.incr()
        return identifier_node
      case TokenType.TOKEN_NUMBER:
        number_node = AstNode(
          AstNodeType.NUMBER_LITERAL,
          location,
          {"value": self.peek().text},
        )
        self.incr()
        return number_node
      case TokenType.TOKEN_CHARLIT:
        charlit_node = AstNode(
          AstNodeType.CHAR_LITERAL,
          location,
          {"value": self.peek().text},
        )
        self.incr()
        return charlit_node
      case TokenType.TOKEN_STRLIT:
        strlit_node = AstNode(
          AstNodeType.STRING_LITERAL,
          location,
          {"value": self.peek().text},
        )
        self.incr()
        return strlit_node
      case TokenType.TOKEN_TRUE:
        true_node = AstNode(
          AstNodeType.TRUE_LITERAL,
          location,
        )
        self.incr()
        return true_node
      case TokenType.TOKEN_FALSE:
        false_node = AstNode(
          AstNodeType.FALSE_LITERAL,
          location,
        )
        self.incr()
        return false_node
      case TokenType.TOKEN_OPAREN:
        self.incr()
        expression_node = self.parse_expression()
        if self.peek().type == TokenType.TOKEN_CPAREN:
          self.incr()
          return expression_node
        else:
          raise CompilerError(self, "\")\" expected")
      case _:
        raise CompilerError(self, "invalid token for primary expression")
      
  """
  @debug(0)      
  def parse_call(self):
    location = self.peek().location
    cursor = self.cursor
    primary_node = self.parse_primary()
    if self.peek().type == TokenType.TOKEN_OPAREN:
      self.incr()
      function_call_node = AstNode(
        AstNodeType.FUNCTION_CALL,
        location,
      )
      function_call_callee_node = AstNode(
        AstNodeType.FUNCTION_CALL_CALLEE,
        location,
      )
      function_call_arguments_node = AstNode(
        AstNodeType.FUNCTION_CALL_ARGS,
        location,
      )
      while not self.eof() and self.peek().type != TokenType.TOKEN_CPAREN:
        function_call_arguments_node.append(self.parse_expression())
        match self.peek().type:
          case TokenType.TOKEN_COMMA:
            self.incr()
          case TokenType.TOKEN_CPAREN:
            self.incr()
            break
          case _:
            raise CompilerError(self, "expected \",\" or \")\"")
      function_call_callee_node.append(primary_node)
      function_call_node.append(function_call_callee_node)
      function_call_node.append(function_call_arguments_node)
      return function_call_node
    else:
      self.cursor = cursor
      return self.parse_primary()
  """

  @debug(0)      
  def parse_call(self):
    location = self.peek().location
    node = self.parse_primary()
    if not self.eof() and self.peek().type == TokenType.TOKEN_OPAREN:
      self.incr()
      function_call_node = AstNode(
        AstNodeType.FUNCTION_CALL,
        location,
      )
      function_call_callee_node = AstNode(
        AstNodeType.FUNCTION_CALL_CALLEE,
        location,
      )
      function_call_arguments_node = AstNode(
        AstNodeType.FUNCTION_CALL_ARGS,
        location,
      )
      while not self.eof() and self.peek().type != TokenType.TOKEN_CPAREN:
        function_call_arguments_node.append(self.parse_expression())
        match self.peek().type:
          case TokenType.TOKEN_COMMA:
            self.incr()
          case TokenType.TOKEN_CPAREN:
            break
          case _:
            raise CompilerError(self, "expected \",\" or \")\"")
      self.incr()
      function_call_callee_node.append(node)
      function_call_node.append(function_call_callee_node)
      function_call_node.append(function_call_arguments_node)
      return function_call_node
    else:
      return node

  @debug(0)      
  def parse_unary(self):
    location = self.peek().location
    match self.peek().type:
      case TokenType.TOKEN_EXCL:
        self.incr()
        unary_type = AstNodeType.NEGATE
      case TokenType.TOKEN_DASH:
        self.incr()
        unary_type = AstNodeType.MINUS
      case TokenType.TOKEN_STAR:
        self.incr()
        unary_type = AstNodeType.POINTER
      case _:
        return self.parse_call()
    unary_node = AstNode(
      unary_type,
      location,
    )
    unary_node.append(self.parse_unary())
    return unary_node

  @debug(0)      
  def parse_factor(self):
    location = self.peek().location
    factor_node = None
    unary_node = self.parse_unary()
    while not self.eof() and self.peek().type in [TokenType.TOKEN_STAR, TokenType.TOKEN_SLASH]:
      factor_node = AstNode(
        AstNodeType.MULTIPLY if self.peek().type == TokenType.TOKEN_STAR else AstNodeType.DIVIDE,
        location,
      )
      self.incr()
      factor_node.append(unary_node)
      factor_node.append(self.parse_unary())
      unary_node = factor_node
    return unary_node

  @debug(0)      
  def parse_term(self):
    location = self.peek().location
    term_node = None
    factor_node = self.parse_factor()
    while not self.eof() and self.peek().type in [TokenType.TOKEN_PLUS, TokenType.TOKEN_DASH]:
      term_node = AstNode(
        AstNodeType.SUM if self.peek().type == TokenType.TOKEN_PLUS else AstNodeType.SUBTRACT,
        location,
      )
      self.incr()
      term_node.append(factor_node)
      term_node.append(self.parse_factor())
      factor_node = term_node
    return factor_node

  @debug(0)    
  def parse_comparison(self):
    location = self.peek().location
    comparison_node = None
    term_node = self.parse_term()
    while not self.eof():
      match self.peek().type:
        case TokenType.TOKEN_GTS:
          comparison_type = AstNodeType.GREATER_THAN
        case TokenType.TOKEN_LTS:
          comparison_type = AstNodeType.LESS_THAN
        case TokenType.TOKEN_GTE:
          comparison_type = AstNodeType.GREATER_EQUAL_THAN
        case TokenType.TOKEN_LTE:
          comparison_type = AstNodeType.LESS_EQUAL_THAN
        case _:
          return term_node
      comparison_node = AstNode(
        comparison_type,
        location,
      )
      self.incr()
      comparison_node.append(term_node)
      comparison_node.append(self.parse_term())
      term_node = comparison_node
    return term_node
  
  @debug(0)      
  def parse_equality(self):
    location = self.peek().location
    equality_node = None
    comparison_node = self.parse_comparison()
    while not self.eof() and self.peek().type in [TokenType.TOKEN_EQUAL_EQUAL, TokenType.TOKEN_NOT_EQUAL]:
      equality_node = AstNode(
        AstNodeType.EQUAL if self.peek().type == TokenType.TOKEN_EQUAL_EQUAL else AstNodeType.NOT_EQUAL,
        location,
      )
      self.incr()
      equality_node.append(comparison_node)
      equality_node.append(self.parse_comparison())
      comparison_node = equality_node
    return comparison_node

  @debug(0)     
  def parse_and(self):
    location = self.peek().location
    equality_node = self.parse_equality()
    if self.peek().type == TokenType.TOKEN_AND:
      and_node = AstNode(
        AstNodeType.OR,
        location,
      )
      and_node.append(equality_node)
      while not self.eof() and self.peek().type == TokenType.TOKEN_AND:
        self.incr()
        and_node.append(self.parse_equality())
      return and_node
    return equality_node

  @debug(0)      
  def parse_or(self):
    location = self.peek().location
    and_node = self.parse_and()
    if self.peek().type == TokenType.TOKEN_OR:
      or_node = AstNode(
        AstNodeType.OR,
        location,
      )
      or_node.append(and_node)
      while not self.eof() and self.peek().type == TokenType.TOKEN_OR:
        self.incr()
        or_node.append(self.parse_and())
      return or_node
    return and_node

  """
  @debug(0)   
  def parse_assignment(self):
    location = self.peek().location
    t0 = self.peek(0)
    t1 = self.peek(1)
    if t0.type == TokenType.TOKEN_NAME and t1.type == TokenType.TOKEN_EQUAL:
      self.incr(2)
      assignment = AstNode(
        AstNodeType.ASSIGNMENT,
        location,
        {"name": t0.text},
      )
      assignment.append(self.parse_assignment())
      return assignment
    else:
      return self.parse_or()
  """

  
  @debug(0)   
  def parse_assignment(self):
    location = self.peek().location
    cursor = self.cursor
    lvalue = self.parse_or()
    if self.peek().type == TokenType.TOKEN_EQUAL:
      self.incr()
      assignment = AstNode(
        AstNodeType.ASSIGNMENT,
        location,
      )
      assignment.append(lvalue)
      assignment.append(self.parse_expression())
      return assignment
    else:
      self.cursor = cursor
      return self.parse_or()

  @debug(0)    
  def parse_expression(self):
    return self.parse_assignment()

  @debug(0)  
  def parse_parameters(self):
    parameters = []
    self.expect_token(TokenType.TOKEN_OPAREN)
    while not self.eof():
      if self.peek().type == TokenType.TOKEN_CPAREN:
        break
      identifier_type = self.parse_type()
      if identifier_type.type in [IdentifierType.CHAR_ARR, IdentifierType.INT_ARR]:
        raise CompilerError(self, "use pointers to pass arrays into function")
      if identifier_type.type == IdentifierType.VOID:
        raise CompilerError(self, "can't use a \"void\" parameter in function")
      identifier_name = self.parse_identifier()
      parameters.append({"name": identifier_name, "type": identifier_type})
      match self.peek().type:
        case TokenType.TOKEN_COMMA:
          self.incr()
    self.incr()
    return parameters
  
  @debug(0)
  def parse_arguments(self):
    location = self.peek().location
    arguments = AstNode(
      AstNodeType.ARGUMENTS_FUNCTION_CALL,
      location,
    )
    self.expect_token(TokenType.TOKEN_OPAREN)
    while not self.eof():
      if self.peek().type == TokenType.TOKEN_CPAREN:
        break
      expression = self.parse_expression()
      arguments.append(expression)
      match self.peek().type:
        case TokenType.TOKEN_COMMA:
          self.incr()
    self.incr()
    return arguments
  
  @debug(0)
  def parse_exprstmt(self):
    expression_node = self.parse_expression()
    self.expect_token(TokenType.TOKEN_SEMICOL)
    return expression_node
  
  @debug(0)
  def parse_block(self):
    location = self.peek().location
    statements = []
    self.expect_token(TokenType.TOKEN_OCURLY)
    while not self.eof() and self.peek().type != TokenType.TOKEN_CCURLY:
      statements.append(self.parse_declaration())
    self.expect_token(TokenType.TOKEN_CCURLY)
    block_node = AstNode(
      AstNodeType.BLOCK,
      location,
    )
    block_node.extend(statements)
    return block_node
  
  @debug(0)
  def parse_if(self):
    location = self.peek().location
    self.expect_token(TokenType.TOKEN_IF)
    self.expect_token(TokenType.TOKEN_OPAREN)
    if_node = AstNode(
      AstNodeType.IF,
      location
    )
    if_condition_node = AstNode(
      AstNodeType.CONDITION,
      self.peek().location,
    )
    if_condition_node.append(self.parse_expression())
    self.expect_token(TokenType.TOKEN_CPAREN)
    if_body_node = AstNode(
      AstNodeType.IF_BODY,
      self.peek().location,
    )
    if_body_node.append(self.parse_statement())
    if_node.append(if_condition_node)
    if_node.append(if_body_node)
    if self.peek().type == TokenType.TOKEN_ELSE:
      self.incr()
      else_body_node = AstNode(
        AstNodeType.ELSE_BODY,
        self.peek().location,
      )
      else_body_node.append(self.parse_statement())
      if_node.append(else_body_node)
    return if_node
  
  @debug(0)
  def parse_while(self):
    location = self.peek().location
    self.expect_token(TokenType.TOKEN_WHILE)
    self.expect_token(TokenType.TOKEN_OPAREN)
    while_node = AstNode(
      AstNodeType.WHILE,
      location,
    )
    while_condition_node = AstNode(
      AstNodeType.CONDITION,
      self.peek().location,
    )
    while_condition_node.append(self.parse_expression())
    self.expect_token(TokenType.TOKEN_CPAREN)
    while_body_node = AstNode(
      AstNodeType.WHILE_BODY,
      self.peek().location,
    )
    while_body_node.append(self.parse_statement())
    while_node.append(while_condition_node)
    while_node.append(while_body_node)
    return while_node
  
  @debug(0)
  def parse_for(self):
    location = self.peek().location
    self.expect_token(TokenType.TOKEN_FOR)
    self.expect_token(TokenType.TOKEN_OPAREN)
    for_node = AstNode(
      AstNodeType.FOR,
      location,
    )
    for_init_node = AstNode(
      AstNodeType.FOR_INITIALIZATION,
      self.peek().location,
    )
    if self.peek().type != TokenType.TOKEN_SEMICOL:
      for_init_node.append(self.parse_expression())
      self.expect_token(TokenType.TOKEN_SEMICOL)
    else:
      self.incr()
    for_condition_node = AstNode(
      AstNodeType.CONDITION,
      self.peek().location,
    )
    if self.peek().type != TokenType.TOKEN_SEMICOL:
      for_condition_node.append(self.parse_expression())
      self.expect_token(TokenType.TOKEN_SEMICOL)
    else:
      self.incr()
    for_step_node = AstNode(
      AstNodeType.FOR_STEP,
      self.peek().location,
    )
    if self.peek().type != TokenType.TOKEN_CPAREN:
      for_step_node.append(self.parse_expression())
      self.expect_token(TokenType.TOKEN_CPAREN)
    else:
      self.incr()
    for_body_node = AstNode(
      AstNodeType.FOR_BODY,
      self.peek().location,
    )
    for_body_node.append(self.parse_statement())
    for_node.append(for_init_node)
    for_node.append(for_condition_node)
    for_node.append(for_step_node)
    for_node.append(for_body_node)
    return for_node

  @debug(0)
  def parse_return(self):
    location = self.peek().location
    self.expect_token(TokenType.TOKEN_RETURN)
    return_node = AstNode(
      AstNodeType.RETURN,
      location,
    )
    if self.peek().type != TokenType.TOKEN_SEMICOL:
      return_node.append(self.parse_expression())
      if self.peek().type != TokenType.TOKEN_SEMICOL:
        raise CompilerError("expected \";\" after return statement")
    self.incr()
    return return_node
    
  @debug(0)
  def parse_statement(self):
    match self.peek().type:
      case TokenType.TOKEN_OCURLY:
        return self.parse_block()
      case TokenType.TOKEN_IF:
        return self.parse_if()
      case TokenType.TOKEN_WHILE:
        return self.parse_while()
      case TokenType.TOKEN_FOR:
        return self.parse_for()
      case TokenType.TOKEN_RETURN:
        return self.parse_return()
      case _:
        return self.parse_exprstmt()
  
  @debug(0)
  def parse_declaration(self):
    location = self.peek().location
    if self.peek().is_type():
      identifier_type = self.parse_type()
      identifier_name = self.parse_identifier()
      match self.peek().type:
        case TokenType.TOKEN_OBRACK:
          self.incr()
          arr_size = self.expect_token(TokenType.TOKEN_NUMBER)
          self.expect_token(TokenType.TOKEN_CBRACK)
          self.expect_token(TokenType.TOKEN_SEMICOL)
          match identifier_type.type:
            case IdentifierType.INT:
              identifier_type = TypeInfo(IdentifierType.INT_ARR, int(arr_size.text) * 2)
            case IdentifierType.CHAR:
              identifier_type = TypeInfo(IdentifierType.CHAR_ARR, int(arr_size.text))
            case IdentifierType.VOID_PTR:
              identifier_type = TypeInfo(IdentifierType.VOID_PTR_ARR, int(arr_size.text) * 2)
            case IdentifierType.INT_PTR:
              identifier_type = TypeInfo(IdentifierType.INT_PTR_ARR, int(arr_size.text) * 2)
            case IdentifierType.CHAR_PTR:
              identifier_type = TypeInfo(IdentifierType.CHAR_PTR_ARR, int(arr_size.text) * 2)
            case IdentifierType.VOID:
              raise CompilerError(self, "can't declare array of \"void\"")
            case _:
              raise CompilerError(self, "expected type")
          return AstNode(
            AstNodeType.VARIABLE_DECLARATION,
            location,
            {"name": identifier_name, "type": identifier_type},
          )    
        case TokenType.TOKEN_EQUAL:
          self.incr()
          if identifier_type.type in [IdentifierType.CHAR_ARR, IdentifierType.INT_ARR]:
            raise CompilerError(self, "can't declare and assign to array variables (please assign values later with memory accesses)")
          if identifier_type.type == IdentifierType.VOID:
            raise CompilerError(self, "can't declare \"void\" variable")
          variable_declaration = AstNode(
            AstNodeType.VARIABLE_DECLARATION,
            location,
            {"name": identifier_name, "type": identifier_type},
          )
          variable_declaration.append(self.parse_expression())
          self.expect_token(TokenType.TOKEN_SEMICOL)
          return variable_declaration
        case TokenType.TOKEN_SEMICOL:
          self.incr()
          if identifier_type.type == IdentifierType.VOID:
            raise CompilerError(self, "can't declare \"void\" variable")
          return AstNode(
            AstNodeType.VARIABLE_DECLARATION,
            location,
            {"name": identifier_name, "type": identifier_type},
          )
        case TokenType.TOKEN_OPAREN:
          if identifier_type.type in [IdentifierType.CHAR_ARR, IdentifierType.INT_ARR]:
            raise CompilerError(self, "can't use array type as return value in function declaration (please use a pointer as return value)")
          parameters = self.parse_parameters()
          function_decl_body = self.parse_statement()
          function_decl = AstNode(
            AstNodeType.FUNCTION_DECLARATION,
            location,
            {"name": identifier_name, "type": identifier_type, "parameters": parameters},
          )
          function_decl.append(function_decl_body)
          return function_decl
        case _:
          raise CompilerError(self, "uhm weird")
    else:
      return self.parse_statement()
    
  def parse(self):
    try:
      self.program = AstNode(
        AstNodeType.PROGRAM,
        Location(self.file_path, 0, 0),
      )
      while not self.eof():
        self.program.append(self.parse_declaration())
    except CompilerError as compiler_error:
      traceback.print_exc()
      print(str(compiler_error))