from flask import Flask, render_template, request
import joblib
import os
import random

app = Flask(__name__)

# File path — works on both local and Render
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'weight_history.csv')

# Load ML model and encoder
model = joblib.load("workout_model.pkl")
goal_encoder = joblib.load("goal_encoder.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    age = int(request.form['age'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    gender = request.form['gender']
    activity = request.form['activity']
    goal = request.form['goal']

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal Weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Workout Prediction (ML model)
    goal_encoded = goal_encoder.transform([goal])[0]

    workout = model.predict([
        [age, bmi, goal_encoded]
    ])[0]

    # BMR
    if gender == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Activity Multiplier
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }

    calories = round(
        bmr * activity_multipliers.get(activity, 1.2)
    )

    # Tips
    if bmi < 18.5:
        tip = "Increase calorie intake and focus on strength training."
    elif bmi < 25:
        tip = "Maintain a balanced diet and regular exercise routine."
    elif bmi < 30:
        tip = "Focus on cardio workouts and healthy eating habits."
    else:
        tip = "Aim for gradual weight loss through diet and exercise."

    # Diet Recommendation
    if goal == "weight_loss":
        diet = """
Breakfast:
• Oats + Fruits

Lunch:
• Rice + Vegetables + Lean Protein

Dinner:
• Salad + Soup
"""

    elif goal == "muscle_gain":
        diet = """
Breakfast:
• Eggs + Milk + Banana

Lunch:
• Rice + Chicken/Fish + Vegetables

Dinner:
• Chapati + Paneer/Eggs
"""

    else:
        diet = """
Breakfast:
• Healthy Balanced Meal

Lunch:
• Rice + Protein + Vegetables

Dinner:
• Light Balanced Dinner
"""

    return render_template(
        'index.html',
        bmi=bmi,
        category=category,
        workout=workout,
        calories=calories,
        tip=tip,
        diet=diet
    )


@app.route('/save_weight', methods=['POST'])
def save_weight():

    current_weight = request.form['current_weight']

    with open(HISTORY_FILE, 'a') as file:
        file.write(f"{current_weight}\n")

    with open(HISTORY_FILE, 'r') as file:
        total_entries = len(file.readlines())

    return render_template(
        'index.html',
        message='Weight saved successfully!',
        total_entries=total_entries
    )


@app.route('/history')
def history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            history = [float(line.strip()) for line in file if line.strip()]
    except FileNotFoundError:
        history = []
    return render_template('history.html', history=history)


@app.route('/nutrition', methods=['GET', 'POST'])
def nutrition():
    if request.method == 'POST':
        weight   = float(request.form['weight'])
        calories = int(request.form['calories'])
        goal     = request.form['goal']

        if goal == 'muscle_gain':
            protein_g = round(weight * 2.0)
        elif goal == 'weight_loss':
            protein_g = round(weight * 1.8)
        else:
            protein_g = round(weight * 1.6)

        protein_cal = protein_g * 4

        if goal == 'weight_loss':
            fat_cal  = round(calories * 0.25)
            carb_cal = calories - protein_cal - fat_cal
        elif goal == 'muscle_gain':
            fat_cal  = round(calories * 0.25)
            carb_cal = calories - protein_cal - fat_cal
        else:
            fat_cal  = round(calories * 0.30)
            carb_cal = calories - protein_cal - fat_cal

        fat_g  = round(fat_cal  / 9)
        carb_g = round(carb_cal / 4)

        protein_pct = round((protein_cal / calories) * 100)
        carbs_pct   = round((carb_cal    / calories) * 100)
        fat_pct     = round((fat_cal     / calories) * 100)

        return render_template('nutrition.html',
            protein=protein_g, carbs=carb_g, fat=fat_g,
            calories=calories,
            protein_pct=protein_pct,
            carbs_pct=carbs_pct,
            fat_pct=fat_pct
        )
    return render_template('nutrition.html')


@app.route('/bmi-info')
def bmi_info():
    return render_template('bmi_info.html')


@app.route('/water', methods=['GET', 'POST'])
def water():
    if request.method == 'POST':
        weight   = float(request.form['weight'])
        activity = request.form['activity']
        climate  = request.form['climate']

        base = weight * 0.033

        activity_add = {'sedentary': 0, 'light': 0.3, 'moderate': 0.5, 'active': 0.7}
        climate_add  = {'cool': 0, 'moderate': 0.2, 'hot': 0.5}

        total = base + activity_add.get(activity, 0) + climate_add.get(climate, 0)
        water_liters = round(total, 1)
        water_ml     = int(water_liters * 1000)
        glasses      = round(water_ml / 250)

        return render_template('water.html',
            water_liters=water_liters,
            water_ml=water_ml,
            glasses=glasses
        )
    return render_template('water.html')


@app.route('/streak')
def streak():
    quotes = [
        "Small steps every day lead to big results.",
        "Discipline is choosing between what you want now and what you want most.",
        "Your body can stand almost anything. It's your mind you have to convince.",
        "The only bad workout is the one that didn't happen.",
        "Sweat now, shine later.",
        "Push yourself because no one else is going to do it for you.",
        "Don't stop when you're tired. Stop when you're done.",
    ]

    try:
        with open(HISTORY_FILE, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
        total = len(lines)
    except FileNotFoundError:
        total = 0

    week_entries = min(total, 7)
    streak = total

    return render_template('streak.html',
        streak=streak,
        total=total,
        week_entries=week_entries,
        quote=random.choice(quotes)
    )


@app.route('/workout-tips')
def workout_tips():
    return render_template('workout.html')


@app.route('/graph')
def graph():
    try:
        with open(HISTORY_FILE, 'r') as f:
            weights = [float(l.strip()) for l in f if l.strip()]
    except FileNotFoundError:
        weights = []
    return render_template('graph.html', weights=weights)


if __name__ == "__main__":
    app.run(debug=True)