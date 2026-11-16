def percentage(present, absent):
    total = present + absent
    return present * 100 / total if total else 0

def absent_three_days(records):
    # records: {register: [daily statuses]}
    return [reg for reg, statuses in records.items()
            if len(statuses) >= 3 and statuses[-3:] == ["A", "A", "A"]]

if __name__ == "__main__":
    print("Percentage:", percentage(18, 2))
    print("Absent three consecutive days:", absent_three_days({"R1": ["A", "A", "A"], "R2": ["P", "A", "A"]}))
