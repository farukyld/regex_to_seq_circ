import shutil

from util.path_shortcuts import OUTPUTS_PARENT
from util.color_print import introduce


def remove_output_directories():
  """
  Locate and remove directories ending with _output
  in the parent directory of this file.
  """
  for item in OUTPUTS_PARENT.iterdir():
    if item.is_dir():
      try:
        print(f"Removing directory: {item}")
        shutil.rmtree(item)
      except Exception as e:
        print(f"Error removing {item}: {e}")


if __name__ == "__main__":
  introduce(__file__)
  remove_output_directories()
