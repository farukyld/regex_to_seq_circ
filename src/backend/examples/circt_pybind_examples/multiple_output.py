import circt
from circt.ir import Context, InsertionPoint, IntegerType, Location, Module
from circt.dialects import hw, comb

with Context() as ctx, Location.unknown():
  circt.register_dialects(ctx)

  si32 = IntegerType.get_signless(32)

  m = Module.create()

  with InsertionPoint(m.body):

    def adder_body(adder_module):
      add_op = comb.AddOp.create(adder_module.a, adder_module.b)  # a + b
      sub_op = comb.SubOp.create(adder_module.a, adder_module.b)  # a - b
      
      hw.OutputOp([add_op,sub_op.opview])

    adder_module = hw.HWModuleOp(
        name="adder",
        input_ports=[("a", si32), ("b", si32)],
        output_ports=[("sum", si32), ("diff", si32)],
        body_builder=adder_body
    )

if __name__ =="__main__":
  print(m)
