import re
from fractions import Fraction

COMMON_UNITS = [
    "tablespoons", "tablespoon", "tbsp",
    "teaspoons", "teaspoon", "tsp",
    "cups", "cup",
    "grams", "gram", "g",
    "kilograms", "kilogram", "kg",
    "ounces", "ounce", "oz",
    "pounds", "pound", "lb",
    "cloves", "clove"
]

REMOVE_WORDS = [
    "chopped", "minced", "diced", "sliced",
    "fresh", "large", "small", "medium",
    "boneless", "skinless", "optional",
    "to taste", "halves", "cut", "into",
    "cooked", "raw"
]


def parse_fraction(text):
    try:
        if " " in text:
            whole, frac = text.split()
            return float(whole) + float(Fraction(frac))
        return float(Fraction(text))
    except:
        return None


def extract_quantity_unit(text):
    text = text.lower().strip()

    # Normalize commas and dashes
    text = text.replace(",", " ").replace("-", " ")

    # Pattern: quantity + unit (anywhere in string)
    pattern = r'(\d+\s\d+/\d+|\d+/\d+|\d+\.?\d*)\s*(tablespoons|tablespoon|tbsp|teaspoons|teaspoon|tsp|cups|cup|grams|gram|g|kilograms|kilogram|kg|ounces|ounce|oz|pounds|pound|lb|cloves|clove)'

    match = re.search(pattern, text)

    quantity = None
    unit = None

    if match:
        quantity_str = match.group(1)
        unit = match.group(2)

        quantity = parse_fraction(quantity_str)

        # Remove matched part from text
        text = text.replace(match.group(0), "").strip()

    return quantity, unit, text


def clean_ingredient_name(text):
    text = re.sub(r'[\(\),]', '', text)

    for word in REMOVE_WORDS:
        text = text.replace(word, "")

    text = re.sub(r'\s+', ' ', text).strip()

    return text


def parse_ingredient(text):
    quantity, unit, remaining = extract_quantity_unit(text)
    ingredient_name = clean_ingredient_name(remaining)

    return {
        "original": text,
        "quantity": quantity,
        "unit": unit,
        "ingredient": ingredient_name
    }