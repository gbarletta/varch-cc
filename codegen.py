import traceback
from defs import TokenType, Token, AstNodeType, IdentifierType, AstNode, Location, CompilerError, token_names, TypeInfo
from treelib import Node, Tree
from functools import wraps

class CodeGen:
  def __init__(self, file_path):
    self.code = f"# {file_path}\n"
    self.regs = [False] * 16
    self.in_func = False
    self.current_var_declarations = 0
    self.symbols = {}
    self.stack_symbols = []
    self.current_label = 0

  def alloc_reg(self):
    for idx, reg in enumerate(self.regs):
      if not reg:
        self.regs[idx] = True
        return idx
      
  def free_reg(self, reg):
    if reg >= len(self.regs):
      raise Exception(f"invalid reg {reg}")
    self.regs[reg] = False

  def get_label(self):
    cur = self.current_label
    self.current_label += 1
    return cur

  def append(self, line="", level=1):
    for _ in range(level):
      self.code += "\t"
    self.code += f"{line}\n"

  def replace(self, find, repl):
    self.code = self.code.replace(find, repl)
  
  def process(self, node):
    match node.type:
      case AstNodeType.PROGRAM:
        self.append()
        for prog_node in node.children:
          self.process(prog_node)
      case AstNodeType.FUNCTION_DECLARATION:
        self.append(f".{node.metadata['name']}:", level=0)
        self.in_func = True
        self.append(f"push\tsf")
        self.append(f"mov\tsf, sp")
        self.append(f"LOCAL_STACK_INIT_PLACEHOLDER")
        self.symbols[node.metadata["name"]] = {"type": "func"}
        for idx, param in enumerate(node.metadata["parameters"]):
          self.symbols[param["name"]] = {"type": "stack", "pos": 2 + ((idx + 1) * 2)}
          self.stack_symbols.append(param["name"])
        self.process(node.children[0])
        self.append(f"mov\tsp, sf")
        self.append(f"pop\tsf")
        self.append(f"ret")
        if self.current_var_declarations > 0:
          self.replace("LOCAL_STACK_INIT_PLACEHOLDER", f"sub\tsp, {str(self.current_var_declarations * 2)}")
        else:
          self.replace("LOCAL_STACK_INIT_PLACEHOLDER", "")
        self.current_var_declarations = 0
        self.symbols = {key: self.symbols[key] for key in self.symbols if key not in self.stack_symbols}
        self.in_func = False
      case AstNodeType.BLOCK:
        for block_node in node.children:
          self.process(block_node)
      case AstNodeType.VARIABLE_DECLARATION:
        stack_pos = None
        if len(node.children) == 1:
          reg = self.process(node.children[0])
        if self.in_func:
          print("Ay Yo porco", self.current_var_declarations)
          self.current_var_declarations += 1
          stack_pos = -2 - ((self.current_var_declarations - 1) * 2)
          self.symbols[node.metadata["name"]] = {"type": "stack", "pos": stack_pos}
          self.stack_symbols.append(node.metadata["name"])
          print(self.symbols)
        else:
          self.symbols[node.metadata["name"]] = {"type": "data"}
        if len(node.children) == 1:
          self.append(f"mov\tsf {stack_pos:+g}, r{reg}".replace("-", "- ").replace("+", "+ "))
          self.free_reg(reg)
      case AstNodeType.NUMBER_LITERAL:
        reg = self.alloc_reg()
        self.append(f"mov\tr{reg}, {node.metadata['value']}")
        return reg
      case AstNodeType.STRING_LITERAL:
        reg = self.alloc_reg()
        self.append(f"mov\tr{reg}, \"{node.metadata['value']}\"")
        return reg
      case AstNodeType.IDENTIFIER:
        reg = self.alloc_reg()
        name = node.metadata["name"]
        if name in self.symbols:
          if self.symbols[name]["type"] == "stack":
            self.append(f"mov\tr{reg}, sf {self.symbols[name]['pos']:+g}".replace("-", "- ").replace("+", "+ "))
          else:
            self.append(f"mov\tr{reg}, {node.metadata['name']}")
        else:
          raise Exception("double kek")
        return reg
      case AstNodeType.VALUE:
        addr = self.process(node.children[0])
        reg = self.alloc_reg()
        self.append(f"mov\tr{reg}, [r{addr}]")
        self.free_reg(addr)
        return reg
      case AstNodeType.FUNCTION_CALL:
        func_reg = self.process(node.children[0]) # Callee expression
        num_args = self.process(node.children[1]) # Arguments for function call
        self.append(f"call\tr{func_reg}")
        if num_args > 0:
          self.append(f"add\tsf, {num_args * 2}")
        self.free_reg(func_reg)
        ret_reg = self.alloc_reg()
        self.append(f"mov\tr{ret_reg}, rv")
        return ret_reg
      case AstNodeType.FUNCTION_CALL_CALLEE:
        return self.process(node.children[0])
      case AstNodeType.FUNCTION_CALL_ARGS:
        for arg_node in node.children:
          r = self.process(arg_node)
          self.append(f"push\tr{r}")
          self.free_reg(r)
        return len(node.children)
      case AstNodeType.SUM:
        ra = self.process(node.children[0])
        rb = self.process(node.children[1])
        self.append(f"add\tr{ra}, r{rb}")
        self.free_reg(rb)
        return ra
      case AstNodeType.SUBTRACT:
        ra = self.process(node.children[0])
        rb = self.process(node.children[1])
        self.append(f"sub\tr{ra}, r{rb}")
        self.free_reg(rb)
        return ra
      case AstNodeType.MULTIPLY:
        ra = self.process(node.children[0])
        rb = self.process(node.children[1])
        self.append(f"mul\tr{ra}, r{rb}")
        self.free_reg(rb)
        return ra
      case AstNodeType.ASSIGNMENT:
        match node.children[0].type:
          case AstNodeType.IDENTIFIER:
            ra = self.process(node.children[0])
          case AstNodeType.POINTER:
            ra = self.process(node.children[0].children[0])
          case _:
            raise Exception("invalid assignment")
        rb = self.process(node.children[1])
        self.append(f"mov\t[r{ra}], r{rb}")
        self.free_reg(ra)
        self.free_reg(rb)
      case AstNodeType.IF:
        cond_reg = self.process(node.children[0])
        ok_label = self.get_label()
        end_label = self.get_label()
        if node.children[2] != None:
          end_else_label = self.get_label()
        self.append(f"jnz\tr{cond_reg}, L{ok_label}")
        self.append(f"jmp\tL{end_label}")
        self.append(f".L{ok_label}:", level=0)
        self.free_reg(cond_reg)
        self.process(node.children[1])
        if node.children[2] != None:
          self.append(f"jmp\tL{end_else_label}")
        self.append(f".L{end_label}:", level=0)
        if node.children[2] != None:
          self.process(node.children[2])
          self.append(f".L{end_else_label}:", level=0)
      case AstNodeType.IF_BODY:
        self.process(node.children[0])
      case AstNodeType.ELSE_BODY:
        self.process(node.children[0])
      case AstNodeType.CONDITION:
        return self.process(node.children[0])
      case AstNodeType.POINTER:
        reg = self.process(node.children[0])
        value_reg = self.alloc_reg()
        self.append(f"mov\tr{value_reg}, [r{reg}]")
        self.free_reg(reg)
        return value_reg
      case AstNodeType.EQUAL:
        ra = self.process(node.children[0])
        rb = self.process(node.children[1])
        self.append(f"cmp\tr{ra}, r{rb}")
        self.append(f"flg\tr{ra}, FLAGS_EQUAL")
        self.free_reg(rb)
        return ra
      case AstNodeType.LESS_EQUAL_THAN:
        ra = self.process(node.children[0])
        rb = self.process(node.children[1])
        self.append(f"cmp\tr{ra}, r{rb}")
        self.append(f"flg\tr{ra}, FLAGS_LESSEQ")
        self.free_reg(rb)
        return ra
      case AstNodeType.RETURN:
        ret = self.process(node.children[0])
        self.append(f"mov\trv, r{ret}")
        self.free_reg(ret)
    #print(node)

  def __str__(self):
    return self.code