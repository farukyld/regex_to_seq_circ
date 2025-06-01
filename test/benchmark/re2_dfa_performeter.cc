#include <re2/re2.h>
#include <chrono>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>
#include <sstream>

// see: https://chatgpt.com/share/683bc89a-b834-800f-a360-0ce44cc621c7

// Simple linear congruential generator
long int modular_random()
{
  static long int state = 123456789; // Updated initial state for determinism

  long int a = 1664525;
  long int c = 1013904223;
  long int m = 4294967296;

  state = (a * state + c) % m;

  return state;
}

std::string generate_random_string(size_t length, const std::string& charset)
{
  std::string result;
  result.reserve(length);
  for (size_t i = 0; i < length; ++i)
  {
    result += charset[modular_random() % charset.length()];
  }
  return result;
}

int64_t parse_arg(const char *arg)
{
  return strtoull(arg, nullptr, 0);
}

void print_help_message(std::string prog_name)
{
  std::cerr << "Usage: " << prog_name
            << " <regex> [--max_mem <N>]"
               " [--charset <input alphabet>]"
               " [--input-length <N>]"
               " [--full-match]"
               " [--print-match-time]"
            << std::endl;
  std::cerr << " or " << std::endl;

  std::cerr << "Usage: " << prog_name
            << " <regex> [--max_mem <N>]"
               " [--input-stdin]"
               " [--full-match]"
               " [--print-match-time]"
            << std::endl;

  std::cerr << " or " << std::endl;

  std::cerr << "Usage: " << prog_name << " --help" << std::endl;

  std::cerr << "\nExplanation of flags:\n"
            << "--max_mem <N>         Maximum memory (in bytes) for RE2 engine.\n"
            << "--charset <str>       Character set for random input string generation. (input alphabet)\n"
            << "--input-length <N>    Length of the randomly generated input string.\n"
            << "--input-stdin         Use standard input as input instead of random.\n"
            << "--full-match          Use RE2::FullMatch instead of PartialMatch.\n"
            << "--print-match-time    Print time taken to match the regex.\n";
}

int main(int argc, char *argv[])
{
  if (argc < 2 || strcmp(argv[1], "--help") == 0)
  {
    print_help_message(argv[0]);
    return 1;
  }

  std::string regex = argv[1];
  int64_t max_mem = 0x800000;
  size_t input_length = 1024; // Default to 1 KiB
  std::string charset =
      "0123456789"
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      "abcdefghijklmnopqrstuvwxyz";
  bool full_match = false;
  bool print_match_time = false;
  bool use_stdin_as_input = false;

  for (int i = 2; i < argc; i++)
  {
    if (strcmp(argv[i], "--max_mem") == 0 && i + 1 < argc)
    {
      max_mem = parse_arg(argv[i + 1]);
      i++;
    }
    else if (strcmp(argv[i], "--charset") == 0 && i + 1 < argc)
    {
      charset = std::string(argv[i + 1]);
      i++;
    }
    else if (strcmp(argv[i], "--input-length") == 0 && i + 1 < argc)
    {
      input_length = parse_arg(argv[++i]);
    }
    else if (strcmp(argv[i], "--input-stdin") == 0)
    {
      use_stdin_as_input = true;
    }
    else if (strcmp(argv[i], "--full-match") == 0)
    {
      full_match = true;
    }
    else if (strcmp(argv[i], "--print-match-time") == 0)
    {
      print_match_time = true;
    }
    else
    {
      std::cerr << "Unknown or malformed argument: " << argv[i] << std::endl;
      return 1;
    }
  }

  std::string input;
  if (use_stdin_as_input)
  {
    std::ostringstream ss;
    ss << std::cin.rdbuf(); // Read entire stdin buffer
    input = ss.str();
  }
  else
  {
    input = generate_random_string(input_length, charset);
  }

  re2::RE2::Options options;
  options.set_never_capture(true);
  options.set_max_mem(max_mem);
  re2::RE2 re(regex, options);

  if (!re.ok())
  {
    std::cerr << "Failed to compile regex at max_mem = " << max_mem << ": "
              << re.error() << std::endl;
    return 1;
  }

  auto start = std::chrono::high_resolution_clock::now();

  volatile bool match;
  if (full_match)
  {
    match = re2::RE2::FullMatch(input, re);
  }
  else
  {
    match = re2::RE2::PartialMatch(input, re);
  }

  auto end = std::chrono::high_resolution_clock::now();

  if (print_match_time)
  {
    std::chrono::duration<float, std::milli> duration = end - start;
    std::cout << "Match time: " << duration.count() << " ms" << std::endl;
  }

  return 0;
}
