from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
REFERENCE_FAT = Decimal("3.5")
REFERENCE_SNF = Decimal("8.5")
STEP_SIZE = Decimal("0.1")
CENT = Decimal("0.01")

def steps(value, reference):
    """Return nearest whole 0.1 percentage-point step using Decimal arithmetic."""
    return int(((Decimal(str(value)) - reference) / STEP_SIZE).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def rate_per_litre(fat, snf):
    """Calculate and return the rate per litre rounded to two decimal places."""
    rate = BASE_RATE + steps(fat, REFERENCE_FAT) * FAT_STEP_VALUE + steps(snf, REFERENCE_SNF) * SNF_STEP_VALUE
    return rate.quantize(CENT, rounding=ROUND_HALF_UP)

def payout(litres, fat, snf):
    """Calculate the payment and return it rounded to the nearest paisa."""
    amount = Decimal(str(litres)) * rate_per_litre(fat, snf)
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)

def ten_day_total(payments):
    """Return the sum of payment amounts, rounded to two decimal places."""
    return sum((Decimal(str(p)) for p in payments), Decimal("0.00")).quantize(CENT, rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    for entry in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate = rate_per_litre(entry[1], entry[2])
        print(entry, "rate =", rate, "payout =", payout(*entry))
