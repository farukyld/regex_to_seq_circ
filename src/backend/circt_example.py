# example from
# see: https://github.com/llvm/circt/blob/main/docs/PythonBindings.md
import circt
from circt.ir import Context, InsertionPoint, IntegerType, Location, Module
from circt.dialects import hw, comb

# location can be file_line_col, or any named location
# that helps locating the generated code which helps debugging.
with Context() as ctx, Location.unknown():
  # NOTE to myself:
  # with context() as ctx, loc.unknown(): is same as
  # with context() as ctx:
  #   with loc.unknown(): # not assigned to a varible.

  # this line must exist in almost every context creation for circt.
  circt.register_dialects(ctx)

  # type definition. signless (neither unsigned nor signed) 42 bits int type.
  # there are also float types and predefined operations for them.
  # signless makes sense in bitwise operations 
  # while (un)signed does so in arithmetic and comparison operations 
  # (I guess)
  i42 = IntegerType.get_signless(42)

  # this is kind of a translation unit. analog to a file (or more ?)
  #  in verilog that can contain more than one hardware module in it.
  m = Module.create()

  # print the empty version of that translation unit.
  print(m)

  # where the upcoming module definitons will go.
  # insertion point target may also 
  # be a submodule (created with HwModuleOp) body. 
  with InsertionPoint(m.body):

  # this method is used as a body_builder in a module 
  # definion done by HWModuleOp method. 
  # the insertion point is automatically set to the module being defined.
    def magic(module):
      xor = comb.XorOp.create(module.a, module.b)
      # the outputs may either be named like this:
      return {"c": xor}
      # or matched in order with:
      # hw.OutputOp([xor])

    # this is a module definition. 
    hw.HWModuleOp(name="magic",
                  input_ports=[("a", i42), ("b", i42)],
                  output_ports=[("c", i42)],
                  body_builder=magic)
  print(m)
