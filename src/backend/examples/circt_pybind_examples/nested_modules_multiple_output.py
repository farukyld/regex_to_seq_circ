import circt
from circt.ir import Context, InsertionPoint, IntegerType, Location, Module, ArrayAttr
from circt.dialects import hw, comb
from circt.passmanager import PassManager


with Context() as ctx, Location.unknown():
  circt.register_dialects(ctx)
  i32 = IntegerType.get_signless(32)
  m = Module.create()

  with InsertionPoint(m.body):

    # Define the 'magic' module
    def magic(module):
      xor_op = comb.XorOp.create(module.sub1_a, module.sub1_b)
      hw.OutputOp([xor_op])

    magic_def = hw.HWModuleOp(name="magic",
                              input_ports=[("sub1_a", i32), ("sub1_b", i32)],
                              output_ports=[("sub1_c", i32)],
                              body_builder=magic)

    # Define the 'other_magic' module
    def other_magic(module):
      and_op = comb.AndOp.create(module.sub2_a, module.sub2_b)
      or_op = comb.OrOp.create(module.sub2_a, module.sub2_b)
      hw.OutputOp([and_op, or_op])

    other_magic_def = hw.HWModuleOp(name="other_magic",
                                    input_ports=[("sub2_a", i32),
                                                 ("sub2_b", i32)],
                                    output_ports=[
                                        ("sub2_c", i32), ("sub2_d", i32)],
                                    body_builder=other_magic)

    # # Define the top module
    def top_module_builder(module: hw.HWModuleOp):
      # Create instances of the 'magic' and 'other_magic' modules
      inst1 = magic_def.instantiate(
          "magic_inst1", sub1_a=module.a, sub1_b=module.b)
      inst2 = other_magic_def.instantiate(
          "magic_inst2", sub2_a=module.a, sub2_b=module.b)
      # # Connect outputs from both instances to top module output ports
      sub2_c, sub2_d = inst2.opview.results
      sub1_c = inst1.opview.results

      hw.OutputOp([sub2_c, sub1_c, sub2_d])

      # ????
      # output_dict = module.outputs()
      # print(type(module.type.output_names))
      # print(module.type.output_names)
      # output_names: list[str] = module.type.output_names
      # output_list = [None]*len(output_names)
      # output_list[output_names.index("other_magic_result1")] = sub2_c
      # output_list[output_names.index("other_magic_result2")] = sub2_d
      # output_list[output_names.index("magic_result")] = sub1_c

      # hw.OutputOp(output_list)

    # # Define the top module with inputs and multiple outputs
    top_module = hw.HWModuleOp(name="top_module",
                               input_ports=[("a", i32), ("b", i32)],
                               output_ports=[
                                   ("other_magic_result1", i32),
                                   ("magic_result", i32),
                                   ("other_magic_result2", i32)],
                               body_builder=top_module_builder)

  if __name__ == "__main__":

    pm = PassManager.parse("builtin.module(export-verilog)")
    pm.run(m.operation)
