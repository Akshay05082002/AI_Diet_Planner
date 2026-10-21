import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def local_ai_fallback(user_message, user_profile=None):
    """Enhanced fallback AI with comprehensive health, diet, and calorie knowledge"""
    user_message = (user_message or "").lower()
    
    # Protein queries
    if "protein" in user_message or "muscle" in user_message or "amino acid" in user_message:
        return (
            "🥩 **Protein Guidelines:**\n"
            "• Recommended: 0.8-1g per kg of body weight (or 1.6-2.2g if building muscle)\n"
            "• Best sources: Chicken, fish, eggs, Greek yogurt, cottage cheese, tofu, legumes, nuts\n"
            "• Spread protein across meals: breakfast, lunch, dinner (25-35g each)\n"
            "• Post-workout: Consume protein within 30-60 mins to aid muscle recovery\n"
            "• Plant-based option: Combine beans + rice for complete amino acid profile"
        )
    
    # Calorie & weight loss queries
    if "calorie" in user_message or "weight loss" in user_message or "lose weight" in user_message:
        return (
            "📊 **Calorie Management for Weight Loss:**\n"
            "• Create deficit: Burn 300-500 more calories than you eat daily (0.5kg/week loss)\n"
            "• Formula: BMR × Activity factor - 500 = Daily calorie goal\n"
            "• Focus on: Whole foods (vegetables, lean meat, brown rice, oats)\n"
            "• Avoid: Sugary drinks, processed snacks, excessive oil\n"
            "• Hydration: Drink 2-3L water daily (aids metabolism & reduces hunger)\n"
            "• Meal timing: Eat every 4-5 hours to maintain stable blood sugar"
        )
    
    # Weight gain queries
    if "weight gain" in user_message or "bulk" in user_message or "gain weight" in user_message:
        return (
            "📈 **Calorie Strategy for Weight Gain:**\n"
            "• Create surplus: Eat 300-500 more calories daily (0.5kg/week gain)\n"
            "• Choose nutrient-dense: Nuts, avocado, olive oil, whole milk, peanut butter\n"
            "• Protein boost: 1.6-2.2g per kg to maximize muscle gain\n"
            "• Carbs: Complex carbs (oats, sweet potato, brown rice) fuel workouts\n"
            "• Strength training: Combine with resistance training 3-4x/week\n"
            "• Meal frequency: 5-6 meals daily (includes snacks)"
        )
    
    # Carbs queries
    if "carb" in user_message or "carbohydrate" in user_message or "glucose" in user_message:
        return (
            "🍞 **Carbohydrate Guide:**\n"
            "• Recommended: 4-7g per kg of body weight (varies by activity)\n"
            "• Simple carbs (instant energy): White bread, sugar, fruit juice\n"
            "• Complex carbs (sustained energy): Oats, brown rice, sweet potato, beans\n"
            "• Best timing: Eat carbs pre/post-workout for energy and recovery\n"
            "• Fiber: Include 25-35g fiber daily (vegetables, whole grains)\n"
            "• Blood sugar control: Pair carbs with protein & healthy fats"
        )
    
    # Fat queries
    if "fat" in user_message or "lipid" in user_message or "cholesterol" in user_message:
        return (
            "🥑 **Healthy Fat Guide:**\n"
            "• Recommended: 0.5-1g per kg of body weight\n"
            "• Calories: 9 calories per gram (more than protein/carbs)\n"
            "• Good sources: Olive oil, avocado, nuts, fatty fish (salmon), coconut oil\n"
            "• Benefits: Hormone production, brain health, nutrient absorption\n"
            "• Avoid: Trans fats, excessive saturated fats\n"
            "• Ratio: 30-35% of total daily calories from fat"
        )
    
    # BMI & health metrics
    if "bmi" in user_message or "body mass" in user_message:
        return (
            "📏 **BMI & Health Metrics:**\n"
            "• BMI = Weight(kg) / Height(m)²\n"
            "• Underweight: BMI < 18.5 | Normal: 18.5-24.9 | Overweight: 25-29.9 | Obese: 30+\n"
            "• Note: BMI doesn't account for muscle, use with other metrics\n"
            "• Better metrics: Waist circumference, body fat %, photos progress\n"
            "• Healthy range for most: Focus on fitness, not just numbers"
        )
    
    # Meal planning
    if "meal" in user_message or "breakfast" in user_message or "lunch" in user_message or "dinner" in user_message or "snack" in user_message:
        return (
            "🍽️ **Balanced Meal Structure:**\n"
            "Each meal should have: 1 protein + 1 vegetable + 1 carb + 1 healthy fat\n\n"
            "✓ Breakfast: Oats + berries + Greek yogurt + almonds (400-500 cal)\n"
            "✓ Lunch: Grilled chicken + brown rice + broccoli + olive oil (500-700 cal)\n"
            "✓ Snack: Apple + peanut butter OR protein shake (200-300 cal)\n"
            "✓ Dinner: Fish + sweet potato + spinach + avocado (500-650 cal)\n\n"
            "Tip: Prep meals on Sunday, use different cooking methods for variety"
        )
    
    # General nutrition
    if "nutrition" in user_message or "healthy" in user_message or "diet" in user_message:
        return (
            "🥗 **Complete Nutrition Guide:**\n"
            "1. Eat whole foods: Minimize processed items (>90% of diet)\n"
            "2. Color variety: Include red, orange, green, purple vegetables\n"
            "3. Portion control: Use palm (protein), fist (carbs), thumb (fats)\n"
            "4. Hydration: 2-3L water daily (adjust for climate/exercise)\n"
            "5. Sleep: 7-9 hours (affects hunger hormones)\n"
            "6. Consistency: Small daily habits > drastic short-term changes\n"
            "7. Supplements: Only after meeting nutrition from food"
        )
    
    # Macros & micronutrients
    if "macro" in user_message or "vitamin" in user_message or "mineral" in user_message or "micronutrient" in user_message:
        return (
            "⚗️ **Macros & Micronutrients:**\n"
            "**Macronutrients (energy):**\n"
            "• Protein: 4 cal/g | Carbs: 4 cal/g | Fat: 9 cal/g\n\n"
            "**Micronutrients (function):**\n"
            "• Iron: Red meat, spinach (oxygen transport)\n"
            "• Calcium: Dairy, leafy greens (bone health)\n"
            "• Vitamin D: Sunlight, fatty fish (immune + mood)\n"
            "• Magnesium: Nuts, seeds, leafy greens (muscle function)\n"
            "• Potassium: Bananas, avocado, coconut water (heart health)"
        )
    
    # Exercise & nutrition
    if "workout" in user_message or "exercise" in user_message or "training" in user_message or "gym" in user_message:
        return (
            "💪 **Nutrition for Exercise:**\n"
            "**Pre-workout (30-60 min before):**\n"
            "• Carbs + light protein: Banana + almonds, rice cakes + peanut butter\n"
            "• Hydration: 500ml water\n\n"
            "**Post-workout (within 30-60 min):**\n"
            "• Protein + carbs: Chicken + rice, protein shake + fruit\n"
            "• Rehydration: 1.5L for every kg lost during exercise\n\n"
            "**Rest days:** Focus on recovery nutrition, lighter meals"
        )
    
    # Metabolism & BMR
    if "metabolism" in user_message or "bmr" in user_message or "basal" in user_message:
        return (
            "🔥 **Metabolism & BMR:**\n"
            "• BMR: Calories burned at rest (60-75% of daily burn)\n"
            "• TDEE: Total daily energy expenditure (BMR × activity factor)\n"
            "• Factors: Age, gender, weight, muscle mass, genetics\n"
            "• Increase metabolism: Build muscle, HIIT training, eat protein\n"
            "• Don't: Crash diet (slows metabolism)\n"
            "• Age effect: 5% per decade after 30 (can reverse with strength training)"
        )
    
    # Hydration
    if "water" in user_message or "hydration" in user_message or "drink" in user_message:
        return (
            "💧 **Hydration Guide:**\n"
            "• Baseline: 2-3 liters daily (varies by climate, activity)\n"
            "• Formula: 35ml per kg of body weight\n"
            "• During exercise: 200-300ml every 20 mins\n"
            "• Signs of dehydration: Dark urine, fatigue, dry mouth\n"
            "• Performance impact: 2% dehydration = 10% performance loss\n"
            "• Tip: Drink before thirst kicks in"
        )
    
    # Default response
    return (
        "Hi! I'm your AI Nutrition Coach. I can help with:\n"
        "• 🥩 Protein & muscle building\n"
        "• 📊 Calorie & weight management\n"
        "• 🍞 Carbs, fats & balanced nutrition\n"
        "• 🍽️ Meal planning & recipes\n"
        "• 💪 Workout nutrition strategies\n"
        "• 📏 BMI & health metrics\n"
        "• 💧 Hydration & supplements\n\n"
        "Ask me anything about diet, calories, nutrition, or fitness!"
    )


def get_ai_response(user_message, user_profile=None):
    """
    Generate a personalized diet/nutrition response using OpenAI with advanced health knowledge.
    Falls back to enhanced local AI if API unavailable.
    """
    if not client:
        return local_ai_fallback(user_message, user_profile)

    profile_text = "No profile data available."
    if user_profile:
        profile_text = f"""
        Age: {user_profile.get('age')}
        Gender: {user_profile.get('gender')}
        Height: {user_profile.get('height')} cm
        Weight: {user_profile.get('weight')} kg
        Activity Level: {user_profile.get('activity')}
        Goal: {user_profile.get('goal')}
        Diet Preference: {user_profile.get('preference')}
        """

    prompt = f"""
    You are an advanced AI Nutritionist and Health Coach with expertise in:
    - Macronutrient calculations (protein, carbs, fats)
    - Calorie management for weight loss/gain/maintenance
    - Meal planning and food combinations
    - Exercise nutrition timing and recovery
    - Health metrics (BMI, BMR, TDEE calculations)
    - Micronutrients and supplementation
    - Medical-grade nutrition guidelines
    
    User profile:
    {profile_text}

    User question: {user_message}

    Provide a detailed, actionable, personalized nutrition/diet answer:
    - Include specific numbers (grams, calories, percentages)
    - Give practical food examples relevant to their goal
    - Reference their profile when relevant
    - Use emoji for clarity
    - Keep advice evidence-based and safe
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert nutritionist and health coach. Provide detailed, actionable nutrition advice with specific numbers."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        # Fall back to enhanced local AI
        return local_ai_fallback(user_message, user_profile)