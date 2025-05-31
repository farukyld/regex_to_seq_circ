#include <re2/re2.h>
#include <chrono>
#include <iostream>
#include <string>
#include <vector>
#include <cstring>

long int modular_random()
{
  static long int state = -1;

  long int a = 1664525;
  long int c = 1013904223;
  long int m = 4294967296;

  state = (a * state + c) % m;

  return state;
}

std::string generate_random_string(size_t length, std::string charset)
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

int main(int argc, char *argv[])
{
  if (argc < 2)
  {
    std::cerr << "Usage: " << argv[0]
              << " <regex> [--max_mem N]"
                 " [--charset <input alphabet string>]"
                 " [--full-match]"
                 " [--print-match-time]"
              << std::endl;
    return 1;
  }

  std::string regex = argv[1];
  int64_t max_mem = 0x800000;
  std::string charset =
      "0123456789"
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      "abcdefghijklmnopqrstuvwxyz";
  bool full_match = false;
  bool print_match_time = false;
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

  std::string input = generate_random_string(1 << 10, charset);

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
  float time_elapsed;
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
    time_elapsed = duration.count(); // time in milliseconds
    std::cout << "Match time: " << time_elapsed << " ms" << std::endl;
  }

  return 0;
}
