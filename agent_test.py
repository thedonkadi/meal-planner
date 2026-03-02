

import requests

# 🔑 Put your USDA API key here
API_KEY = "wIFT7ccBcBcKmiQhAom1bUoQDdraOJTGpcLc0eRc"

BASE_URL = "https://api.nal.usda.gov/fdc/v1"


def test_usda_api():
    print("🔎 Testing USDA API...\n")

    search_url = f"{BASE_URL}/foods/search?api_key={API_KEY}"

    payload = {
        "query": "chicken breast raw",
        "pageSize": 1,
        "dataType": ["Foundation", "SR Legacy"]
    }

    search_response = requests.post(search_url, json=payload)

    print("Search Status Code:", search_response.status_code)

    if search_response.status_code != 200:
        print("❌ Search failed!")
        print(search_response.text)
        return

    search_data = search_response.json()

    if not search_data.get("foods"):
        print("❌ No foods found!")
        return

    food = search_data["foods"][0]
    fdc_id = food["fdcId"]

    print("✅ Found:", food["description"])
    print("FDC ID:", fdc_id)

    # Step 2: Get food details
    details_url = f"{BASE_URL}/food/{fdc_id}?api_key={API_KEY}"
    details_response = requests.get(details_url)

    print("\nDetails Status Code:", details_response.status_code)

    if details_response.status_code != 200:
        print("❌ Details fetch failed!")
        print(details_response.text)
        return

    details_data = details_response.json()

    serving_size = details_data.get("servingSize")
    serving_unit = details_data.get("servingSizeUnit")

    print("\nServing Size:", serving_size, serving_unit)

    print("\n📊 Nutrition per 100g:")

    for nutrient in details_data.get("foodNutrients", []):
        name = nutrient.get("nutrient", {}).get("name")
        value = nutrient.get("amount")

        if not name or value is None:
            continue

        if serving_size and serving_unit == "g":
            per_100g = (value / serving_size) * 100
        else:
            per_100g = value  # fallback

        if name in ["Energy", "Protein", "Carbohydrate, by difference", "Total lipid (fat)"]:
            print(f"{name}: {round(per_100g, 2)}")

    print("\n🎉 USDA API test completed!")


if __name__ == "__main__":
    test_usda_api()