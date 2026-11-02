"""Q5: Clean sensor readings and convert Celsius to Fahrenheit."""
import random
import sys
import time

def loop_version(readings):
    valid_c = []
    for c in readings:
        if -50 <= c <= 50:
            valid_c.append(c)
    valid_f = []
    for c in valid_c:
        valid_f.append(c * 9 / 5 + 32)
    return valid_c, valid_f

def comprehension_version(readings):
    valid_c = [c for c in readings if -50 <= c <= 50]
    valid_f = [c * 9 / 5 + 32 for c in valid_c]
    return valid_c, valid_f

def map_filter_version(readings):
    valid_c = list(filter(lambda c: -50 <= c <= 50, readings))
    valid_f = list(map(lambda c: c * 9 / 5 + 32, valid_c))
    return valid_c, valid_f

def alarm_minutes(readings):
    return [minute for minute, c in enumerate(readings, start=1) if c < 2 or c > 8]

def benchmark():
    random.seed(42)
    print("n,loop_seconds,comprehension_seconds,map_filter_seconds")
    for n in (10_000, 100_000, 1_000_000):
        data = [random.uniform(-60, 60) for _ in range(n)]
        timings = []
        outputs = []
        for fn in (loop_version, comprehension_version, map_filter_version):
            start = time.perf_counter(); result = fn(data); timings.append(time.perf_counter()-start); outputs.append(result)
        assert outputs[0] == outputs[1] == outputs[2]
        print(f"{n},{timings[0]:.6f},{timings[1]:.6f},{timings[2]:.6f}")

if __name__ == "__main__":
    readings = [4.0, 7.5, 55.0, -60.0, 1.0, 9.0, 6.0]
    print("Loop:", loop_version(readings))
    print("Comprehension:", comprehension_version(readings))
    print("map/filter:", map_filter_version(readings))
    print("Alarm minutes:", alarm_minutes(readings))
    print("All valid test:", comprehension_version([1, 2, 3]))
    print("All invalid test:", comprehension_version([100, -100]))
    generator = (x for x in range(1000))
    print("Container sizes:", sys.getsizeof([x for x in range(1000)]), sys.getsizeof(generator))
    benchmark()
