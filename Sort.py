# Group: Lauren Sdun, Julia Baumgarten

import importlib.util, types, random, time, csv, argparse
import matplotlib.pyplot as plt
from pathlib import Path

def load_hpfloat(path):
    spec = importlib.util.spec_from_file_location("hpfloat", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.HighPrecisionFloat

# Bubble sort method
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Merge sort method
def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)

def _merge(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if right[j] < left[i]:
            out.append(right[j]); j += 1
        else:
            out.append(left[i]); i += 1
    if i < len(left): out.extend(left[i:])
    if j < len(right): out.extend(right[j:])
    return out

def make_hp_list(HPF, n, bits=128, seed=42):
    rng = random.Random(seed)
    return [HPF(str(rng.random()), bits=bits) for _ in range(n)]

def time_sort(func, data_maker, n, repeats=3):
    best = float("inf")
    for _ in range(repeats):
        data = data_maker(n)
        t0 = time.perf_counter()
        res = func(data)
        t1 = time.perf_counter()
        best = min(best, t1 - t0)
        if not all(not (res[k+1] < res[k]) for k in range(len(res)-1)):
            raise RuntimeError(f"{func.__name__} produced an unsorted list at n={n}")
    return best

def main(bits):
    float_py = Path("float.py")
    if not float_py.exists():
        raise SystemExit("Could not find float.py in the current directory.")
    HPF = load_hpfloat(float_py)

    def maker(n):
        return make_hp_list(HPF, n, bits=bits, seed=42)

    sizes = [16, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 384, 448, 512]

    bubble_times, merge_times = [], []
    for n in sizes:
        bubble_times.append(time_sort(bubble_sort, maker, n))
        merge_times.append(time_sort(merge_sort, maker, n))

    with open("sort_timing.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "bubble_seconds", "merge_seconds"])
        for n, tb, tm in zip(sizes, bubble_times, merge_times):
            w.writerow([n, tb, tm])

    plt.figure()
    plt.plot(sizes, bubble_times, marker="o", label="Bubble sort (HighPrecisionFloat)")
    plt.plot(sizes, merge_times, marker="s", label="Merge sort (HighPrecisionFloat)")
    plt.xlabel("List length (n)")
    plt.ylabel("Best runtime over 3 runs (seconds)")
    plt.title(f"Sorting time vs list length (bits={bits})")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.savefig("sort_timing.png", dpi=150, bbox_inches="tight")
    print("Wrote sort_timing.csv and sort_timing.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bits", type=int, default=128, help="Precision in bits for HighPrecisionFloat")
    args = ap.parse_args()
    main(args.bits)
