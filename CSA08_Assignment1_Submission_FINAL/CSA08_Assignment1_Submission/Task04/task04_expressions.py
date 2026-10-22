def steps(value, reference):
    """Count 0.1 percentage-point steps, rounding to nearest whole step."""
    return round((value - reference) / 0.1)

if __name__ == "__main__":
    print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
    print("round((4.2 - 3.5) / 0.1) =", steps(4.2, 3.5))
    print("0.1 + 0.2 =", 0.1 + 0.2)
    print("7 / 2 =", 7 / 2, "| 7 // 2 =", 7 // 2, "| 7 % 2 =", 7 % 2)
    print("-7 // 2 =", -7 // 2, "| int(-7 / 2) =", int(-7 / 2))
