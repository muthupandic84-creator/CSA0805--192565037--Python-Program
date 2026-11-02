"""Q7: Merge contacts using normalised phone numbers as dictionary keys."""
import random
import re
import time

def normalize_phone(phone):
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    # Treat a leading Indian country code as equivalent to a 10-digit number.
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    return digits

def normalize_name(name):
    return " ".join(name.casefold().split()) if name else ""

def merge_contacts(contacts):
    merged = {}
    for contact in contacts:
        raw_numbers = contact.get("phones", [])
        normalized = {normalize_phone(p) for p in raw_numbers}
        normalized.discard("")
        if not normalized:
            # Missing-phone contacts cannot safely be deduplicated by number.
            key = f"no-phone:{len(merged)}"
        else:
            key = sorted(normalized)[0]
        if key not in merged:
            merged[key] = {"name": contact.get("name", "").strip(),
                           "phones": set(), "emails": set(), "aliases": set()}
        entry = merged[key]
        name = contact.get("name", "").strip()
        if name:
            if not entry["name"]:
                entry["name"] = name
            entry["aliases"].add(name)
        entry["phones"].update(normalized)
        email = contact.get("email", "").strip().casefold()
        if email:
            entry["emails"].add(email)
    return list(merged.values())

def benchmark():
    print("contacts,merge_seconds")
    for n in (1_000, 100_000):
        contacts = [{"name": f"Person {i}", "phones": [f"+91 90000 {i:05d}"], "email": f"p{i}@example.com"}
                    for i in range(n)]
        start = time.perf_counter()
        result = merge_contacts(contacts)
        elapsed = time.perf_counter() - start
        assert len(result) == n
        print(f"{n},{elapsed:.6f}")

if __name__ == "__main__":
    sample = [
        {"name": "Dr. Ravi", "phones": ["+91 98400 12345"], "email": "ravi@example.com"},
        {"name": "ravi kumar", "phones": ["9840012345"], "email": "rk@example.com"},
        {"name": "Meena", "phones": ["+91-90000-11111"], "email": ""},
        {"name": "No Phone Contact", "phones": [], "email": "none@example.com"},
        {"name": "No Phone Contact", "phones": [], "email": "another@example.com"},
    ]
    print("Merged sample:")
    for item in merge_contacts(sample):
        print(item)
    benchmark()
