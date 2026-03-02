UNIT_TO_GRAMS = {
    "g": 1,
    "gram": 1,
    "grams": 1,
    "kg": 1000,
    "kilogram": 1000,
    "oz": 28.35,
    "ounce": 28.35,
    "lb": 453.6,
    "pound": 453.6
}

UNIT_TO_ML = {
    "tsp": 5,
    "teaspoon": 5,
    "tbsp": 15,
    "tablespoon": 15,
    "cup": 240
}

DENSITY_MAP = {
    "olive oil": 0.91,
    "sunflower oil": 0.92,
    "water": 1.0,
    "milk": 1.03
}

COUNT_BASED_WEIGHTS = {
    "garlic": 5,
    "chicken breast": 150
}


def convert_to_grams(quantity, unit, ingredient):
    if quantity is None:
        return None

    # Direct gram units
    if unit in UNIT_TO_GRAMS:
        return quantity * UNIT_TO_GRAMS[unit]

    # Volume units
    if unit in UNIT_TO_ML:
        ml = quantity * UNIT_TO_ML[unit]

        for key in DENSITY_MAP:
            if key in ingredient:
                return ml * DENSITY_MAP[key]

        return ml * 1.0  # assume water density

    # Count-based
    if unit in ["clove", "cloves", None]:
        for key in COUNT_BASED_WEIGHTS:
            if key in ingredient:
                return quantity * COUNT_BASED_WEIGHTS[key]

    return None