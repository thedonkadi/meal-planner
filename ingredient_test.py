from app.ingredient_parser import parse_ingredient

tests = [
    "200g tofu",
    "tofu 200g",
    "tofu, 200 g",
    "1 cup rice",
    "rice 1 cup",
    "3 cloves garlic"
]

for t in tests:
    print(parse_ingredient(t))