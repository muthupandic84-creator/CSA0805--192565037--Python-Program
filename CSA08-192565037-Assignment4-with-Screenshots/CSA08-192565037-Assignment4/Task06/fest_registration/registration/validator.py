class InvalidRegistration(ValueError):
    pass

def validate_record(raw):
    fields = [field.strip() for field in raw.split(",")]
    if len(fields) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(fields)}")
    reg, name, department, email, events_text = fields
    if not all((reg, name, department, email, events_text)):
        raise InvalidRegistration("one or more required fields are empty")
    if email.count("@") != 1:
        raise InvalidRegistration("e-mail must contain exactly one @")
    local, domain = email.split("@")
    if not local or "." not in domain or domain.startswith(".") or domain.endswith("."):
        raise InvalidRegistration("e-mail format is invalid")
    events = [event.strip() for event in events_text.split(";") if event.strip()]
    if not events:
        raise InvalidRegistration("at least one event is required")
    return {"register_number": reg, "name": name, "department": department,
            "email": email, "events": events}
