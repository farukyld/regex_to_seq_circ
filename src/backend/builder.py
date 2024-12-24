import json
from pycde import Module, System, Clock, Reset, Output, Input, generator, modparams
from pycde.types import Bits
from pycde.constructs import Reg, Wire,NamedWire
from pycde.signals import BitsSignal
from pycde import signals
from pycde.circt.dialects import comb


from backend.circuit_deser import CircuitDeser
from path_shortcuts import TEST_0_JSON_PATH, generate_sv_output_dir_name


@modparams
def seq_circt_builder(formal_circuit: CircuitDeser):
  class SeqCircuit(Module):
    clk = Clock()
    rst = Reset()
    y_o = Output(Bits(1))
    x_i = Input(Bits(8))

    @generator
    def build(ports):
      # start at zeroth position (to be 1) at reset
      first_position = Bits(1)(1)
      remaining_positions = Bits(formal_circuit.n_states-1)(0)
      initial_value = BitsSignal.concat([remaining_positions, first_position])

      # Create a register using the Reg construct
      state = Reg(Bits(formal_circuit.n_states), clk=ports.clk,
                  rst=ports.rst, rst_value=initial_value)
      state.name = "state"

      transition_functions = []

      # activate state[0] always if partial_match flag is set
      transition_functions.append(Bits(1)(not formal_circuit.full_match))

      formal_circuit.transitions.sort(key=lambda tr: tr[0]) # sort by to_state
      for transition in formal_circuit.transitions:
        input_to_consume = transition[1]
        from_states = transition[2]

        transition_functions.append(
            signals.And(
                # input is equal to transsitions consume target
                ports.x_i == Bits(8)(input_to_consume.encode()[0]),
                # and
                # one of the bits of current state
                # indicated by from_states of the transition is active
                signals.Or(*[state[from_state]
                                   for from_state in from_states])
            )
        )

      ports.y_o = signals.Or(*[
        transition_functions[accept_state_index]
        for accept_state_index in formal_circuit.accept_states
      ])


      transition_functions.reverse()
      state.assign(BitsSignal.concat(transition_functions))

  return SeqCircuit


def main():
  # Example usage
  # Instantiate the parametric register with a bit width of 16
  with open(TEST_0_JSON_PATH, "r") as f:
    json_obj = json.load(f)
  formal_circuit = CircuitDeser.from_dict(json_obj)
  output_dir = generate_sv_output_dir_name(__file__)
  system = System([seq_circt_builder(formal_circuit)], name="seq_circuit",
                  output_directory=output_dir)
  system.compile()


if __name__ == "__main__":
  main()
