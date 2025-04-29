# clean.py

import shutil
import sys

from path_shortcuts import OUTPUTS_PARENT, FINAL_OUTPUTS, INTER_OUTPUTS


def remove_final_output_directories():
  """
  Locate and remove directories ending with _output
  in the parent directory of this file.
  """
  for item in FINAL_OUTPUTS.iterdir():
    if item.is_dir():
      try:
        print(f"Removing directory: {item}")
        shutil.rmtree(item)
      except Exception as e:
        print(f"Error removing {item}: {e}")


def remove_all_build_content(recreate_empty_directories=True):
  for item in OUTPUTS_PARENT.iterdir():
    shutil.rmtree(item)
  if recreate_empty_directories:
    INTER_OUTPUTS.mkdir(parents=True, exist_ok=True)
    FINAL_OUTPUTS.mkdir(parents=True, exist_ok=True)



if __name__ == "__main__":
  remove_final_output_directories()
  if len(sys.argv) == 1:
    print(f"to clean all build directory content, run:\n"
          f"python {__file__} all")
  elif not sys.argv[1] == "all":
    print(f"argument {sys.argv[1]} is not recognized. did you mean:\n"
          f"python {__file__} all")
  else:
    remove_all_build_content()
