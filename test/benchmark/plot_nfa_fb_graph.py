import subprocess
import matplotlib.pyplot as plt
import numpy as np
from util.color_print import print_yellow

# Charsets to test
charsets = {
    "ab": "ab",
    "a": "a",
    "alphanum": "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
}

n_values = range(1, 60)
max_mem_values = np.linspace(90000, 3000, num=90, dtype=int)
EXECUTABLE = "./re2_dfa_size_est.elf"

results = {label: [] for label in charsets.keys()}

def run_regex_benchmark(regex, max_mem, charset):
    cmd = [EXECUTABLE, regex, "--max_mem", str(max_mem), "--charset", charset]
    # print_yellow("Running:")
    # print(*cmd)
    proc = subprocess.run(cmd, capture_output=True)
    stderr = proc.stderr.decode()
    return "DFA" not in stderr

# Benchmark loop
for charset_label, charset in charsets.items():
    print_yellow(f"\n[Running benchmarks for charset: {charset_label}]")
    for n in n_values:
        regex = "(a|b)*ab" + "(a|b)" * n
        fallback_mem = None
        for mem in max_mem_values:
            if not run_regex_benchmark(regex, mem, charset):
                fallback_mem = mem
                break
        if fallback_mem:
            results[charset_label].append((n, fallback_mem / 1024))  # Convert to KB
        else:
            results[charset_label].append((n, max_mem_values[-1] / 1024))

# Plotting function
def plot_data(data: dict[str, list[tuple[int, int]]], title, filename):
    plt.figure(figsize=(10, 6))
    for label, points in data.items():
        x_vals, y_vals = zip(*points)
        plt.plot(x_vals, y_vals, marker='o', label=label)
    plt.xlabel("n (Repetition count in regex)")
    plt.ylabel("Minimum max_mem before fallback (KB)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print_yellow(f"✅ Saved: {filename}")

# Combined plot
plot_data(
    results,
    "DFA to NFA Fallback Threshold vs Regex Size (All Charsets)",
    "dfa_fallback_all_charsets.png"
)

# Individual plots
for label, points in results.items():
    plot_data(
        {label: points},
        f"Charset: {label} — DFA to NFA Fallback",
        f"dfa_fallback_{label}.png"
    )
