# example from
# see: https://github.com/llvm/circt/blob/main/docs/PythonBindings.md
import circt
from circt.ir import Context, InsertionPoint, IntegerType, Location, Module, Attribute
from circt.dialects import hw, comb, seq  # Importing the seq dialect

# location can be file_line_col, or any named location
# that helps locating the generated code which helps debugging.
with Context() as ctx, Location.unknown():
  # Register CIRCT dialects with the context.
  circt.register_dialects(ctx)

  # Define a signless 42-bit integer type.
  i42 = IntegerType.get_signless(42)

  # Create the main module.
  m = Module.create()

  # Print the empty version of that translation unit.
  if __name__ == "__main__":
    print(m)

  # Define an insertion point for the main module.
  with InsertionPoint(m.body):

    # Define the body of the hardware module.
    def magic(module):
      # Create an XOR operation.
      xor = comb.XorOp.create(module.a, module.b)
      
      # Define a register to store the XOR result using seq dialect.
      # reg = seq.CompRegOp(clk=clock, input=xor, name="xor_reg")  # Create a register for the XOR result
      
      # Return the output through the register.
      return {"c": xor}

    # Define the hardware module with input and output ports.
    hw.HWModuleOp(name="magic",
                  input_ports=[("a", i42), ("b", i42)],
                  output_ports=[("c", i42)],
                  body_builder=magic)

if __name__ == "__main__":
  print(m)
