from reader import read_status_rows
from stats import percentage, absent_three_days
from report import write_summary

if __name__ == "__main__":
    data = read_status_rows("sample_status.csv")
    history = {}
    for reg, status in data:
        history.setdefault(reg, []).append(status)
    print("Percentage:", percentage(18, 2))
    print("Absent three days:", absent_three_days(history))
    write_summary("summary.txt", [("present", 18), ("absent", 2)])
