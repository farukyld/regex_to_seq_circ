# see: https://chatgpt.com/share/683be524-76a0-800f-a50c-67d258b5c7b1
import subprocess
import numpy as np
import random
from collections import defaultdict
from util import simple_test_cases
import sys
from pathlib import Path

EXECUTABLE = Path(__file__).parent / "re2_dfa_performeter.elf"

# Configuration
input_length = 1_000_000
max_mem_values = [1000, 2000, 5000, 10000, 30000, 60000]
alphabets = {
    "alphanum": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
}
minimum_of_how_many_runs = 10
regexes = simple_test_cases.benchmarking
compact_forms = simple_test_cases.benchmarking_compact_forms

# Storage:
# results[alphabet][full_match][regex][max_mem] = (runtime_ms, is_fallback_nfa)
all_results:  dict[str, dict[bool, dict[str, dict[int, tuple[int, bool]]]]] = defaultdict(
    lambda: defaultdict(lambda: defaultdict(dict)))


def generate_random_input(length, charset):
  return ''.join(random.choices(charset, k=length))


def run_benchmark(regex: str, max_mem: int, input_data: str, full_match=False):
  cmd = [EXECUTABLE, regex,
         "--max-mem", str(max_mem),
         "--input-stdin",
         "--print-match-time"]
  if full_match:
    cmd.append("--full-match")

  proc = subprocess.run(
      cmd,
      input=input_data.encode(),
      capture_output=True,
  )
  stderr = proc.stderr.decode()
  stdout = proc.stdout.decode()

  # Extract runtime in ms
  runtime_ms = None
  for line in stdout.splitlines():
    if "Match time:" in line:
      runtime_ms = float(line.split("Match time:")[1].split("ms")[0].strip())

  # Detect fallback
  fallback = "DFA" in stderr

  return runtime_ms, fallback


# Main benchmark loop
for alphabet_label, charset in alphabets.items():
  print(f"\n[Alphabet: {alphabet_label}] Generating input...", file=sys.stderr)
  input_data = generate_random_input(input_length, charset)

  for full_match in [True]:
    match_mode = "FullMatch" if full_match else "PartialMatch"
    print(f"\n[Mode: {match_mode}]", file=sys.stderr)

    for regex in regexes:
      print(f"Regex: {compact_forms[regex]}", file=sys.stderr)
      for mem in max_mem_values:
        print(f"Testing max_mem = {mem} bytes...", file=sys.stderr)
        runtime_fallbacks = [run_benchmark(regex, mem, input_data, full_match) for _ in range(minimum_of_how_many_runs)]
        runtime_fallbacks.sort()
        runtime, fallback = runtime_fallbacks[0]
        all_results[alphabet_label][full_match][regex][mem] = (
            runtime, fallback)
        if runtime and int(runtime):
          print(
              f"→ Runtime: {runtime:.2f} ms | Fallback: {'Yes' if fallback else 'No'}", file=sys.stderr)
        else:
          print("run failed", file=sys.stderr)


def print_results(all_results: dict[str, dict[bool, dict[str, dict[int, tuple[int, bool]]]]]):
  # see: https://chatgpt.com/share/683be3e7-6bd0-800f-91df-f56b68e3d165
  for alphabet, results_of_alphabet in all_results.items():
    for full_match, results_of_full_match_of_alphabet in results_of_alphabet.items():
      print(f"\nTable for alphabet='{alphabet}', full_match={full_match}:")

      # Collect all row names (regexes) and column names (max_mems)
      regexes = list(results_of_full_match_of_alphabet.keys())
      any_row = results_of_full_match_of_alphabet[regexes[0]]
      max_mems = list(any_row.keys())
      # Header row
      # header = [""] + [compact_forms[regex] for regex in regexes]
      header = [""] + [str(max_mem) for max_mem in max_mems]
      print("\t".join(header))

      # Each row
      for regex in regexes:
        row = [compact_forms[regex]]
        for mem in max_mems:
          cell = results_of_full_match_of_alphabet[regex].get(mem, "")
          row.append(str(cell))
        print("\t".join(row))


# print("Column headers are max_mem values,"
#       "row  headers are regexes, "
#       "cells are runtimes and if nfa fall back occured."
#       " minimum of runtime_ms' among"
#       f"{minimum_of_how_many_runs} runs are taken."
#       f"input length is {input_length}")

# print_results(all_results)




def print_results_as_latex(all_results: dict[str, dict[bool, dict[str, dict[int, tuple[float, bool]]]]]):
  for alphabet, results_of_alphabet in all_results.items():
    for full_match, results_of_full_match_of_alphabet in results_of_alphabet.items():
      match_label = "FullMatch" if full_match else "PartialMatch"
      print(f"\n% Table for alphabet='{alphabet}', mode='{match_label}'")

      regexes = list(results_of_full_match_of_alphabet.keys())
      max_mems = sorted(
          list(next(iter(results_of_full_match_of_alphabet.values())).keys()))
      col_format = "||p{4cm}" + "|p{1.5cm}" * len(max_mems) + "|"
      print("\\begin{table}[ht]")
      print("\\centering")

      print(f"\\begin{{tabular}}{{{col_format}}}")
      print("\\hline")
      header = ["Regex \\textbackslash{} MaxMem kB"] + [str(m//1000) for m in max_mems]
      print(" & ".join(header) + " \\\\")
      print("\\hline")

      for regex in regexes:
        # -replace "{", "\{" -replace "}", "\}" -replace "_", "\_"  -replace "\|", "\textbar{}"
        row_label = compact_forms.get(regex, regex).replace("{","\{").replace("}","\}").\
        replace('_', '\\_').replace("|","\\textbar{}")
        row = [row_label]
        for mem in max_mems:
          runtime_ms, fallback = results_of_full_match_of_alphabet[regex].get(
              mem, (None, None))
          if runtime_ms is None:
            cell = "--"
          else:
            rate_Mhz = (input_length / runtime_ms) / 1e3
            cell = f"{rate_Mhz:.2f} MHz"
          row.append(cell)
        print(" & ".join(row) + " \\\\")
      print("\\hline")
      print("\\end{tabular}")
      print(
      f"\\caption{{Char consumption rate (MHz) for alphabet=\\texttt{{{alphabet}}}, mode={match_label}}}")
      print("\\end{table}\n")

print("Column headers are max_mem values,"
      "row  headers are regexes, "
      "cells are speed."
      " minimum of runtime_ms' among "
      f"{minimum_of_how_many_runs} runs are taken."
      f" input length is {input_length}")

print_results_as_latex(all_results)