"""Q2: OTP attempts using while and for range(3), plus loop controls."""
CORRECT_OTP = "246810"

def verify_while(entries, max_attempts=3):
    attempts = 0
    index = 0
    while attempts < max_attempts and index < len(entries):
        entered = entries[index]
        index += 1
        if entered.strip() == "":
            print("Blank entry: not counted")
            continue
        attempts += 1
        if entered == CORRECT_OTP:
            print("OTP verified using while loop")
            break
        print(f"Wrong OTP ({attempts}/{max_attempts})")
    else:
        if attempts == max_attempts:
            print("Account locked for 30 minutes")
        else:
            print("No more supplied entries")

def verify_for(entries, max_attempts=3):
    iterator = iter(entries)
    for attempt_number in range(max_attempts):
        entered = next(iterator, None)
        if entered is None:
            print("No more supplied entries")
            break
        if entered.strip() == "":
            print("Blank entry: not counted")
            # A blank is not an attempt, so compensate by extending the range.
            # This loop is demonstration-oriented; the while design is preferable
            # when skipped blanks must not consume one of the fixed attempts.
            continue
        if entered == CORRECT_OTP:
            print("OTP verified using for loop")
            break
        print(f"Wrong OTP ({attempt_number + 1}/{max_attempts})")
    else:
        print("Account locked for 30 minutes")

def recursive_verify(entries, index=0, attempts=0, max_attempts=3):
    if index >= len(entries):
        return "Account locked for 30 minutes" if attempts >= max_attempts else "No more entries"
    if attempts >= max_attempts:
        return "Account locked for 30 minutes"
    entered = entries[index]
    if entered.strip() == "":
        return recursive_verify(entries, index + 1, attempts, max_attempts)
    if entered == CORRECT_OTP:
        return "OTP verified"
    return recursive_verify(entries, index + 1, attempts + 1, max_attempts)

def main():
    print("WHILE DEMO:")
    verify_while(["", "111111", "222222", "246810"])
    print("\\nFOR RANGE(3) DEMO:")
    verify_for(["111111", "222222", "333333"])
    print("\\nRECURSIVE DEMO:", recursive_verify(["111111", "222222", "333333"]))
    if False:
        pass  # pass is a no-operation statement; shown here as a placeholder.
    print("\\nChanged condition: after successful security answer, call with max_attempts=5.")
    print("A while loop handles skipped blank entries and dynamically changed limits more naturally.")

if __name__ == "__main__":
    main()
