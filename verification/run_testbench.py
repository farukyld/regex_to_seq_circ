import subprocess
import sys
import random
import string
import json
from pathlib import Path
from color_print import print_green, print_red, print_yellow, print_cyan
import re2
from path_shortcuts import get_any_output_dir_and_json


def generate_random_input(length: int = 100) -> str:
  return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def main():
  output_dir, json_path = get_any_output_dir_and_json()

  # Load regex from json
  with open(json_path, 'r') as f:
    json_obj = json.load(f)
  regex_pattern_semicolon_inserted = json_obj.get("regex", "")
  if not regex_pattern_semicolon_inserted:
    raise RuntimeError(f"regex field read from {json_path} is empty")

  # Paths
  verilog_file = output_dir / "hw/seq_circuit.sv"
  tb_file = Path(__file__).parent / "testbench.sv"
  compile_path = output_dir / "verilator_objdir"
  exec_name = "sim.exe"
  sim_path = output_dir / "sim"
  sim_path.mkdir(exist_ok=True)
  exec_path = sim_path / exec_name
  input_path = sim_path / "input.txt"
  output_path = sim_path / "output.txt"

  # Compile using Verilator
  verilator_cmd = [
      "verilator",
      "--binary",
      "--Mdir", str(compile_path),
      "--top-module", "tb_seq_circt",
      "-o", str(exec_path),
      "-O2",
      str(verilog_file),
      str(tb_file),
      # "--trace",  # Optional: for waveform generation
  ]
  print_yellow("running command: ", ' '.join(verilator_cmd))
  sys.stdout.flush()
  sys.stderr.flush()
  subprocess.run(verilator_cmd, check=True)

  # Generate input
  input_str = generate_random_input(1000)

  with open(input_path, 'w') as sim_in:
    sim_in.write(input_str)

  with open(input_path, 'r') as sim_in, open(output_path, 'w') as sim_out:
    print_yellow("running command: ", ' '.join([str(exec_path)]))
    sys.stderr.flush()
    sys.stdout.flush()
    subprocess.run([str(exec_path)], stdin=sim_in,
                   stdout=sim_out, check=True)

  with open(output_path, 'r') as sim_out:
    sim_output = sim_out.read()

  regex_pattern_without_semicolon = str(
      regex_pattern_semicolon_inserted).replace(';', '')
  # Use RE2 to compute expected output
  print_cyan(regex_pattern_without_semicolon)

  import re2_substring_match
  re2_matches = re2_substring_match.has_match_ending_at_index(
      input_str, regex_pattern_without_semicolon)

  re2_output = ''.join('1' if m else '0' for m in re2_matches)

  # Compare
  if sim_output.strip().startswith(re2_output.strip()):
    print_green("Output matches expected regex matches.")
    print("input:")
    print(input_str)
    print("Verilator output:")
    print(sim_output)
    print("RE2 expected output:")
    print(re2_output)
  else:
    print_red("Mismatch between Verilator output and RE2 result.")
    print("Verilator output:")
    print(sim_output)
    print("RE2 expected output:")
    print(re2_output)


if __name__ == "__main__":
  main()
