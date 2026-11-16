def demonstrate_hidden_error():
    total_present = 0
    try:
        total_presnt += 1  # Deliberate typo: wrong variable name
    except Exception:
        pass
    print("Program continues; the NameError was silently hidden.")

if __name__ == "__main__":
    demonstrate_hidden_error()
