"""Executable reference for Task 8's algorithmic plan."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Task07'))

from milkrate import payout

def total_for_entries(entries):
    """Compute payment per entry and the total for a list of (litres, fat, snf)."""
    total = 0
    results = []
    for litres, fat, snf in entries:
        amount = payout(litres, fat, snf)
        results.append(amount)
        total += amount
    return results, total

if __name__ == "__main__":
    sample = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
    results, total = total_for_entries(sample)
    print("Payments:", results)
    print("Total:", total)
