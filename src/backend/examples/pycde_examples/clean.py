# clean.py
# in the parent directory of that file,
# locate the directories ending with _output
# remove them

import shutil
from path_shortcuts import OUTPUTS_PARENT, OUTPUT_DIR_SUFFIX


def remove_output_directories():
  """
  Locate and remove directories ending with _output
  in the parent directory of this file.
  """
  for item in OUTPUTS_PARENT.iterdir():
    if item.is_dir() and item.name.endswith(OUTPUT_DIR_SUFFIX):
      try:
        print(f"Removing directory: {item}")
        shutil.rmtree(item)
      except Exception as e:
        print(f"Error removing {item}: {e}")


if __name__ == "__main__":
  remove_output_directories()
