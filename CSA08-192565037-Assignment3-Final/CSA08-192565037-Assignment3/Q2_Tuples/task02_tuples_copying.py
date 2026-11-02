"""Q2: Tuples, mutability, aliasing and copying."""
import copy
import sys
import time

def main():
    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7
    print("bad :", bad)
    print("good:", good)
    print(bad[0] is bad[1], good[0] is good[1])

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar"
    }
    print(stops[(13.0418, 80.2341)])
    try:
        stops[[13.0418, 80.2341]] = "Invalid key"
    except TypeError as error:
        print("List key error:", error)

    original = [[1, 2], [3, 4]]
    alias = original
    shallow_copy = copy.copy(original)
    slice_copy = original[:]
    deep_copy = copy.deepcopy(original)
    original[0][0] = 99
    print("Aliased object changed:", alias)
    print("Shallow copy shares inner list:", shallow_copy)
    print("Deep copy remains independent:", deep_copy)

    nested_tuple = ([10, 20], "stop")
    nested_tuple[0].append(30)
    print("Mutable list inside tuple:", nested_tuple)

    list_values = list(range(1_000_000))
    tuple_values = tuple(range(1_000_000))
    print("Container sizes (bytes):", sys.getsizeof(list_values), sys.getsizeof(tuple_values))

    start = time.perf_counter()
    _ = tuple(range(100_000))
    tuple_create = time.perf_counter() - start
    start = time.perf_counter()
    _ = list(range(100_000))
    list_create = time.perf_counter() - start
    print(f"Creation time: tuple={tuple_create:.6f}s list={list_create:.6f}s")

    start = time.perf_counter()
    _ = tuple_values[500_000]
    tuple_index = time.perf_counter() - start
    start = time.perf_counter()
    _ = list_values[500_000]
    list_index = time.perf_counter() - start
    print(f"Index time: tuple={tuple_index:.9f}s list={list_index:.9f}s")

if __name__ == "__main__":
    main()
