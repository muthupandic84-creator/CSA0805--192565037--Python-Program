"""Load a rate card from JSON to make seasonal revisions easier."""
import json
from decimal import Decimal
from pathlib import Path

RATE_FILE = Path(__file__).resolve().with_name("rate_card.json")

def load_rate_card(path=RATE_FILE):
    """Load a JSON rate card and convert numeric values to Decimal."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {key: Decimal(str(value)) for key, value in data.items()}

if __name__ == "__main__":
    print(load_rate_card())
