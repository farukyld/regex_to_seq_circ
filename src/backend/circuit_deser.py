class CircuitDeser:
  def __init__(self, regex: str, n_states: int, full_match: bool, accept_states: list[int], transitions: list[tuple[int, str, list[int]]]):
    self.regex = regex
    self.n_states = n_states
    self.full_match = full_match
    self.transitions = transitions
    self.accept_states = accept_states

  @classmethod
  def from_dict(cls, json_obj) -> 'CircuitDeser':
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
    regex: str = json_obj["regex_canonical"]
    n_states: int = json_obj["n_states"]
    full_match: bool = json_obj["full_match"]
    accept_states: list[int] = json_obj["accept_states"]
    transitions: list[dict[str, int | str |
                           list[int]]] = json_obj["transitions"]
    transition_tuples: list[tuple] = [
        (tr_dict["to_state"], tr_dict["must_read"],
         tr_dict["from_states"])
        for tr_dict in transitions
    ]

    return cls(regex, n_states, full_match, accept_states, transition_tuples)
