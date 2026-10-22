"""Season-aware milk payment calculator for the changed requirements."""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")
STEP_SIZE = Decimal("0.1")
REFERENCE_FAT = Decimal("3.5")
REFERENCE_SNF = Decimal("8.5")

RATE_CARDS = {
    "regular": {"base": Decimal("30.00"), "fat": Decimal("0.40"), "snf": Decimal("0.30")},
    "april_june": {"base": Decimal("32.00"), "fat": Decimal("0.45"), "snf": Decimal("0.30")},
}

def count_steps(value, reference):
    """Round a two-decimal analyser reading to the nearest 0.1-point step."""
    return int(((Decimal(str(value)) - reference) / STEP_SIZE).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def rate_per_litre(fat, snf, season="regular"):
    """Calculate the seasonal litre rate from the selected rate card."""
    if season not in RATE_CARDS:
        raise ValueError("Unknown season")
    card = RATE_CARDS[season]
    rate = card["base"] + count_steps(fat, REFERENCE_FAT) * card["fat"] + count_steps(snf, REFERENCE_SNF) * card["snf"]
    return rate.quantize(CENT, rounding=ROUND_HALF_UP)

def ten_day_payout(litres, fat, snf, season="regular", ten_day_litres=0):
    """Calculate payment and add Rs 0.50/litre bonus when ten-day volume exceeds 500 L."""
    litres = Decimal(str(litres))
    amount = litres * rate_per_litre(fat, snf, season)
    if Decimal(str(ten_day_litres)) > Decimal("500"):
        amount += litres * Decimal("0.50")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    tests = [
        ("regular", 10, 3.5, 8.5, 300),
        ("april_june", 10, 3.5, 8.5, 300),
        ("april_june", 20, 4.25, 8.55, 520),
        ("april_june", 20, 4.25, 8.55, 500),
    ]
    for season, litres, fat, snf, ten_day in tests:
        print(season, litres, fat, snf, "10-day litres", ten_day,
              "rate", rate_per_litre(fat, snf, season),
              "payout", ten_day_payout(litres, fat, snf, season, ten_day))
