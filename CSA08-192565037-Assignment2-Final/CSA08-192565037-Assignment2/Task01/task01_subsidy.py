"""Q1: State electricity subsidy – separate if vs if-elif-else."""

def separate_if(units, ration_card, elderly_over_80):
    results = []
    if units <= 100:
        results.append("Full subsidy")
    if 101 <= units <= 200 and ration_card:
        results.append("Partial subsidy")
    if units > 200 and elderly_over_80:
        results.append("Special elderly exemption")
    if not results:
        results.append("No subsidy")
    return results

def chained_decision(units, ration_card, elderly_over_80):
    if units <= 100:
        return "Full subsidy"
    elif 101 <= units <= 200:
        if ration_card:
            return "Partial subsidy"
        else:
            return "No subsidy"
    elif units > 200:
        if elderly_over_80:
            return "Special elderly exemption"
        else:
            return "No subsidy"

def main():
    households = [
        ("H1", 99, False, False),
        ("H2", 100, True, False),
        ("H3", 101, True, False),
        ("H4", 101, False, False),
        ("H5", 150, True, False),
        ("H6", 200, False, True),
        ("H7", 201, False, False),
        ("H8", 250, False, True),
    ]
    print("ID  Units  Ration  >80  Separate-if result                 Chained result")
    for hid, units, ration, elderly in households:
        s = ", ".join(separate_if(units, ration, elderly))
        c = chained_decision(units, ration, elderly)
        print(f"{hid:<3} {units:<6} {str(ration):<7} {str(elderly):<4} {s:<35} {c}")

    print("\nBoundary checks (100, 101, 200, 201):")
    for units in (100, 101, 200, 201):
        print(units, "=>", chained_decision(units, True, units > 200))

    print("\nDesign decision: use if-elif-else for mutually exclusive unit bands.")
    print("Nested checks keep the eligibility conditions close to each band.")

if __name__ == "__main__":
    main()
