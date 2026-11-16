def write_summary(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(",".join(map(str, row)) + "\n")
