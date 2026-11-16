def read_status_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            fields = [x.strip() for x in line.strip().split(",")]
            if len(fields) == 2 and fields[1] in {"P", "A"}:
                rows.append((fields[0], fields[1]))
    return rows
