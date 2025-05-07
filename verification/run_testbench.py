import subprocess
import sys
import tempfile
import random
import string
import json
from pathlib import Path
from color_print import print_green, print_red, print_yellow,print_cyan
import re2
from path_shortcuts import get_any_output_dir_and_json


def generate_random_input(length: int = 100) -> str:
  return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def main():
  output_dir, json_path = get_any_output_dir_and_json()

  # Load regex from json
  with open(json_path, 'r') as f:
    json_obj = json.load(f)
  regex_pattern = json_obj.get("regex", "")

  # Paths
  verilog_file = output_dir / "hw/seq_circuit.sv"
  tb_file = Path(__file__).parent / "testbench.sv"
  dpi_defns = Path(__file__).parent / "dpi_defns.c"
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
      str(verilog_file),
      str(tb_file),
      str(dpi_defns),
      # "--trace",  # Optional: for waveform generation
  ]
  print_yellow("running command: ", ' '.join(verilator_cmd))
  sys.stdout.flush()
  sys.stderr.flush()
  subprocess.run(verilator_cmd, check=True)

  # Generate input
  # input_str = generate_random_input()
  input_str = "aaaabaabababa"

  f_sim_in = open(input_path, 'w+')
  f_sim_in.write(input_str)
  f_sim_in.flush()
  f_sim_in.seek(0,0)
  print_cyan(f_sim_in.read())
  print_cyan(input_str)
  f_sim_out = open(output_path, "w+")

  print_yellow("running command: ", ' '.join([str(exec_path)]))
  sys.stdout.flush()
  sys.stderr.flush()
  subprocess.run([str(exec_path)], stdin=f_sim_in,
                 stdout=f_sim_out, check=True)
  
  f_sim_out.flush()
  sim_output = f_sim_out.read()
  print_cyan(sim_output)

  # Use RE2 to compute expected output
  re2_matches = list(re2.finditer(regex_pattern, input_str))
  re2_output = ''.join('1' if (m.group(0)) else '0'  for m in re2_matches)

  # Compare
  if sim_output.strip() == re2_output.strip():
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
