def percentage(present, absent):
    total = present + absent
    return present * 100 / total if total else 0

def absent_three_days(records):
    return [reg for reg, statuses in records.items()
            if len(statuses) >= 3 and statuses[-3:] == ["A", "A", "A"]]
