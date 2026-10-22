BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
REFERENCE_FAT = 3.5
REFERENCE_SNF = 8.5
STEP_SIZE = 0.1
MIN_FAT = 2.0
MAX_FAT = 7.0

def describe_rate_card():
    """Return a readable description of the configured rate card."""
    return (f"Base Rs {BASE_RATE:.2f}; fat step Rs {FAT_STEP_VALUE:.2f}; "
            f"SNF step Rs {SNF_STEP_VALUE:.2f}; fat range {MIN_FAT}-{MAX_FAT}%")

if __name__ == "__main__":
    print(describe_rate_card())
