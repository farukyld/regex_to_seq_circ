
import json


class Circuit:
  def __init__(self, n_states: int, full_match: bool, transitions: list[tuple[int, str, frozenset]]):
    self.n_states = n_states
    self.full_match = full_match
    self.transitions = transitions
    pass

  @classmethod
  def from_json(cls, json_obj) -> 'Circuit':
    """create Circuit object from previously generated json file. <p>
      useful for naming fields 

    Args:
        json_obj (_type_): the data returned by json.load method
    """
    # was serialized like:
    # circuit_dict = {
    #     "n_states": RegexASTNode._literals_created + 1,
    #     "full_match": full_match,
    #     "transitions": [
    #         {
    #             "to_state": i,
    #             "must_read": a,
    #             "from_states": list(h),
    #         } for i, a, h in self.trig
    #     ]
    # }

    n_states = json_obj["n_states"]
    full_match = json_obj["full_match"]
    transitions: list[dict[str,int|str|list[int]]] = json_obj["transitions"]
    transition_tuples: list[tuple] = [
        (tr_dict["to_state"], tr_dict["must_read"],
         frozenset(tr_dict["from_states"]))
        for tr_dict in transitions
    ]

    return cls(n_states, full_match, transition_tuples)


if __name__ == "__main__":

  with open("circuit_json.json", "r") as file:
    circuit_info = json.load(file)
    circuit_obj = Circuit.from_json(circuit_info)