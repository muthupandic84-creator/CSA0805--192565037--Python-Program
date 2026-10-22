"""Rate card of the Ksheera Village Milk Co-operative."""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
REFERENCE_FAT = Decimal("3.5")
REFERENCE_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")
CENT = Decimal("0.01")

def _steps(value, reference):
    """Count nearest whole 0.1 percentage-point steps."""
    difference = Decimal(str(value)) - reference
    return int((difference / STEP_SIZE).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def rate_per_litre(fat, snf):
    """Return the price per litre, rounded to two decimals."""
    rate = BASE_RATE + _steps(fat, REFERENCE_FAT) * FAT_STEP_VALUE + _steps(snf, REFERENCE_SNF) * SNF_STEP_VALUE
    return rate.quantize(CENT, rounding=ROUND_HALF_UP)

def payout(litres, fat, snf):
    """Return the amount payable, rounded to the nearest paisa."""
    return (Decimal(str(litres)) * rate_per_litre(fat, snf)).quantize(CENT, rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate = rate_per_litre(fat, snf)
        amount = payout(litres, fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {amount:8.2f}")
