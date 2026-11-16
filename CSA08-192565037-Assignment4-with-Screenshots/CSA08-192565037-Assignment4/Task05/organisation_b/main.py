from attendance_utils import percentage, absent_three_days

if __name__ == "__main__":
    print("Percentage:", percentage(18, 2))
    print("Absent three consecutive days:", absent_three_days({"R1": ["A", "A", "A"]}))
