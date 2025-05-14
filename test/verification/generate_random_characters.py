# see: https://chatgpt.com/share/682429d1-4d7c-800f-b42a-50a6ab41cd5e
import argparse
import random
import string

def generate_random_alphanumerics(n):
  chars = string.ascii_letters + string.digits
  return ''.join(random.choices(chars, k=n))

def main():
  parser = argparse.ArgumentParser(description="Generate random alphanumeric characters.")
  parser.add_argument('-n', type=int, required=True, help='Number of characters to generate')
  args = parser.parse_args()

  print(generate_random_alphanumerics(args.n))

if __name__ == "__main__":
  main()
