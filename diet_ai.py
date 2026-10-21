import random
import os

# Food dataset (expand anytime)
FOODS = {
    "breakfast": [
        {"name": "Oats with Milk", "cal": 300, "protein": 12, "carbs": 45, "fat": 8},
        {"name": "Idli + Sambar", "cal": 250, "protein": 10, "carbs": 40, "fat": 5},
        {"name": "Poha", "cal": 280, "protein": 8, "carbs": 45, "fat": 7},
        {"name": "Boiled Eggs (2)", "cal": 200, "protein": 14, "carbs": 2, "fat": 13},
        {"name": "Upma", "cal": 270, "protein": 9, "carbs": 42, "fat": 6},
    ],
    "lunch": [
        {"name": "Rice + Dal + Veg Curry", "cal": 520, "protein": 18, "carbs": 80, "fat": 12},
        {"name": "Chapati + Paneer Curry", "cal": 560, "protein": 22, "carbs": 60, "fat": 20},
        {"name": "Chicken Curry + Rice", "cal": 620, "protein": 32, "carbs": 70, "fat": 18},
        {"name": "Veg Biryani", "cal": 540, "protein": 15, "carbs": 85, "fat": 15},
        {"name": "Curd Rice", "cal": 480, "protein": 14, "carbs": 75, "fat": 10},
    ],
    "snacks": [
        {"name": "Banana", "cal": 105, "protein": 1, "carbs": 27, "fat": 0},
        {"name": "Sprouts Salad", "cal": 180, "protein": 12, "carbs": 25, "fat": 4},
        {"name": "Protein Shake", "cal": 220, "protein": 20, "carbs": 15, "fat": 6},
        {"name": "Peanut Chikki", "cal": 160, "protein": 6, "carbs": 14, "fat": 9},
        {"name": "Apple", "cal": 80, "protein": 0, "carbs": 21, "fat": 0},
    ],
    "dinner": [
        {"name": "Soup + Salad", "cal": 260, "protein": 10, "carbs": 25, "fat": 8},
        {"name": "Chapati + Veg Curry", "cal": 450, "protein": 14, "carbs": 60, "fat": 14},
        {"name": "Egg Curry + Chapati", "cal": 510, "protein": 22, "carbs": 45, "fat": 22},
        {"name": "Fish Curry + Rice", "cal": 540, "protein": 28, "carbs": 60, "fat": 18},
        {"name": "Khichdi", "cal": 420, "protein": 16, "carbs": 65, "fat": 10},
    ],
}


def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    return "Obese"


def calculate_bmr(gender, weight_kg, height_cm, age):
    gender = gender.lower()
    if gender == "male":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee(bmr, activity):
    activity_factors = {
        "low": 1.2,
        "medium": 1.55,
        "high": 1.725
    }
    return round(bmr * activity_factors.get(activity, 1.2), 2)


def goal_calories(tdee, goal):
    if goal == "loss":
        return int(tdee - 500)
    elif goal == "gain":
        return int(tdee + 500)
    return int(tdee)


def generate_diet_plan(calories, preference="veg"):
    """
    Simple AI planner (rule-based):
    - Randomly selects meals from dataset
    - You can improve by filtering veg/nonveg later
    """
    plan = {
        "target_calories": calories,
        "meals": {}
    }

    for meal in ["breakfast", "lunch", "snacks", "dinner"]:
        plan["meals"][meal] = random.choice(FOODS[meal])

    total_cal = sum(plan["meals"][m]["cal"] for m in plan["meals"])
    total_protein = sum(plan["meals"][m]["protein"] for m in plan["meals"])
    total_carbs = sum(plan["meals"][m]["carbs"] for m in plan["meals"])
    total_fat = sum(plan["meals"][m]["fat"] for m in plan["meals"])

    plan["total_calories"] = total_cal
    plan["total_protein"] = total_protein
    plan["total_carbs"] = total_carbs
    plan["total_fat"] = total_fat

    return plan


def estimate_calories(food_name: str) -> int:
    """
    Estimate calories for a free-text food name.
    Strategy:
    - Try to find a matching item from FOODS by substring match.
    - If not found, use keyword heuristics for common foods.
    - Fall back to a conservative default (200 kcal).
    """
    if not food_name:
        return 0

    key = food_name.strip().lower()

    # direct match search in dataset
    for cat in FOODS:
        for item in FOODS[cat]:
            if item["name"].lower() in key or key in item["name"].lower():
                return int(item.get("cal", 0))

    # substring match
    for cat in FOODS:
        for item in FOODS[cat]:
            if any(tok in key for tok in item["name"].lower().split()):
                return int(item.get("cal", 0))

    # heuristics
    heur = {
        "banana": 105,
        "apple": 95,
        "egg": 78,
        "rice": 200,
        "bread": 80,
        "toast": 75,
        "chicken": 240,
        "paneer": 300,
        "salad": 80,
        "milk": 120,
        "oats": 150,
        "pizza": 285,
        "burger": 320,
        "pasta": 350,
        "fish": 220,
        "soup": 150,
        "shake": 200,
        "yogurt": 100,
    }

    for k, v in heur.items():
        if k in key:
            return v

    # fallback
    return 200


def recognize_image_stub(image_path: str):
    """
    Prototype image recognition stub.
    - For now, uses filename heuristics to "detect" items in the image.
    - Returns a list of dicts: [{"name": "Grilled Chicken", "calories": 240}, ...]
    Replace with a real vision model / API (Gemini Vision, CLIP, etc.) later.
    """
    if not image_path:
        return []

    fname = os.path.basename(image_path).lower()
    preds = []

    # Simple filename heuristics: look for common tokens
    tokens = ["chicken", "salad", "pizza", "burger", "banana", "egg", "rice", "pasta", "fish", "apple"]
    for t in tokens:
        if t in fname:
            name = t.capitalize()
            cal = estimate_calories(name)
            preds.append({"name": name, "calories": cal})

    # If nothing detected from filename, return a conservative default suggestion
    if not preds:
        # return a generic plate suggestion
        preds.append({"name": "Mixed Plate (est)", "calories": 400})

    return preds
