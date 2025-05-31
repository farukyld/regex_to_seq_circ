from frontend.ast_to_formal_circuit import calculate_trig
from util.simple_test_cases import health_check
from util.color_print import introduce
from frontend.regex_parser import reg_exp

# for debugging
if __name__ == "__main__":
  introduce(__file__)
  test_results = {}
  for test_case in health_check:
    print("test case: ", test_case)
    # see: https://chatgpt.com/share/6805cea4-1810-800f-bc56-f79c9aca6dd5
    parse_result = reg_exp.parse_string(test_case, parse_all=True)
    test_results[test_case] = parse_result[0]

  trig_E_1 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({1}))
  trig_E_0 = calculate_trig(
      test_results["(a;b|b)*;b;a"], frozenset({0}))

  print("done")
