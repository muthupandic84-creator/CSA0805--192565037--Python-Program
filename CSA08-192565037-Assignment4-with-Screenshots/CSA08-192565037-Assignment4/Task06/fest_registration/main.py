from pathlib import Path
from registration.processor import process_files

HERE = Path(__file__).parent
if __name__ == "__main__":
    master, errors = process_files(
        HERE / "input",
        HERE / "output",
        expected_departments=["CSE.txt", "ECE.txt", "EEE.txt", "MECH.txt", "CIVIL.txt"]
    )
    print(f"Valid registrations: {len(master)}")
    print(f"Logged issues: {len(errors)}")
    print("Reports written to output/")
