def percentage(present, absent):
    total = present + absent
    return present * 100 / total if total else 0

def absent_three_days(history):
    return [reg for reg, values in history.items()
            if len(values) >= 3 and values[-3:] == ["A", "A", "A"]]
