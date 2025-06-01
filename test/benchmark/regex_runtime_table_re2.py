# see: https://chatgpt.com/share/683be524-76a0-800f-a50c-67d258b5c7b1
import subprocess
import numpy as np
import random
from collections import defaultdict
from util import simple_test_cases
import sys
EXECUTABLE = "./re2_dfa_performeter.elf"

# Configuration
input_length = 1_000_000  # 1MB input
max_mem_values = [50000, 40000, 30000, 20000, 10000]
alphabets = {
    "ab": "ab",
    "a": "a",
    "alphanum": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
}
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
         "--max_mem", str(max_mem),
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

  for full_match in [False, True]:
    match_mode = "FullMatch" if full_match else "PartialMatch"
    print(f"\n[Mode: {match_mode}]",file=sys.stderr)

    for regex in regexes:
      print(f"Regex: {compact_forms[regex]}",file=sys.stderr)
      for mem in max_mem_values:
        print(f"Testing max_mem = {mem} bytes...", file=sys.stderr)
        runtime, fallback = run_benchmark(regex, mem, input_data, full_match)
        all_results[alphabet_label][full_match][regex][mem] = (
            runtime, fallback)
        print(
            f"→ Runtime: {runtime:.2f} ms | Fallback: {'Yes' if fallback else 'No'}", file=sys.stderr)


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


print("Column headers are max_mem values,"
      "row  headers are regexes, "
      "cells are runtimes and if nfa fall back occured. ")
print_results(all_results)
