"""Q4: Set operations for elective registration clashes."""
import random
import time

def reports(ai_elective, iot_elective, all_students):
    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)
    return both, exactly_one, neither

def benchmark():
    print("n,list_membership_seconds,set_membership_seconds")
    for n in (10_000, 100_000, 1_000_000):
        values = [f"R{i}" for i in range(n)]
        value_set = set(values)
        target = f"R{n-1}"
        start = time.perf_counter(); target in values; list_time = time.perf_counter()-start
        start = time.perf_counter(); target in value_set; set_time = time.perf_counter()-start
        print(f"{n},{list_time:.9f},{set_time:.9f}")

if __name__ == "__main__":
    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}
    both, exactly_one, neither = reports(ai_elective, iot_elective, all_students)
    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))

    # Equivalent set-method version
    assert both == ai_elective.intersection(iot_elective)
    assert exactly_one == ai_elective.symmetric_difference(iot_elective)
    assert neither == all_students.difference(ai_elective.union(iot_elective))
    print("Set-method verification: passed")
    print("Empty sets:", reports(set(), set(), all_students))
    print("Identical sets:", reports(ai_elective, ai_elective, all_students))
    benchmark()
