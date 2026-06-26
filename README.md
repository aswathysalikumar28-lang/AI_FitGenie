# 🏋️ FitGenie — AI Fitness Coach

A smart fitness web app built with Flask and Machine Learning that gives personalized workout recommendations, BMI analysis, calorie targets, diet plans, and weight tracking.

---

## 🚀 Live Demo

[fitgenie.onrender.com](https://fitgenie.onrender.com)

---

## ✨ Features

- **AI Workout Prediction** — ML model recommends workouts based on your age, BMI and goal
- **BMI Calculator** — calculates your BMI and category instantly
- **Calorie Target** — daily calorie recommendation using BMR + activity level
- **Diet Plan** — personalized meal plan based on your goal
- **Weight Tracker** — log and track your weight over time
- **Progress Graph** — interactive Chart.js graph of your weight history
- **Weight History** — full table of all entries with change tracking
- **Nutrition Calculator** — macro breakdown (protein, carbs, fat)
- **Water Intake Calculator** — daily water target based on weight, activity and climate
- **BMI Info Page** — detailed health info for each BMI category
- **Workout Tips** — full weekly plans for weight loss, muscle gain and maintenance
- **Streak & Motivation** — tracks your logging streak with badges and daily quotes
- **Sidebar Navigation** — clean sidebar layout across all pages
- **Mobile Responsive** — hamburger menu on mobile

---

## 🧠 Machine Learning

The ML model (`workout_model.pkl`) is trained using scikit-learn on a fitness dataset. It takes:

| Input | Description |
|-------|-------------|
| Age | User's age |
| BMI | Calculated from weight and height |
| Goal | Encoded goal (weight loss / muscle gain / maintenance) |

And predicts the most suitable **workout type** for the user.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| ML | scikit-learn, joblib |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Fonts | Google Fonts (Bebas Neue, DM Sans) |
| Deployment | Render |

---

## 📁 Project Structure

```
fitGenie/
├── app.py                  # Flask app and all routes
├── train_model.py          # ML model training script
├── fitness_data.csv        # Training dataset
├── workout_model.pkl       # Trained ML model
├── goal_encoder.pkl        # Label encoder for goal
├── weight_history.csv      # Saved weight entries
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment config
├── static/
│   └── progress.png
└── templates/
    ├── index.html          # Dashboard
    ├── graph.html          # Weight progress graph
    ├── history.html        # Weight history table
    ├── nutrition.html      # Macro calculator
    ├── water.html          # Water intake calculator
    ├── bmi_info.html       # BMI information
    ├── workout.html        # Workout plans
    └── streak.html         # Streak and motivation
```

---

## ⚙️ Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fitgenie.git
cd fitgenie
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Train the model (if needed)**
```bash
python train_model.py
```

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://localhost:5000
```

---

## 📦 Requirements

```
flask
joblib
scikit-learn
numpy
gunicorn
```

---

## 🌐 Deploy on Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a **New Web Service**
3. Connect your GitHub repo
4. Set the start command to `gunicorn app:app`
5. Click **Deploy**

---

## 📸 Screenshots

> Dashboard · Progress Graph · Nutrition Calculator · Streak Page

---

## 👨‍💻 Developer

Built by Aswathy Salikumar

---

## 📄 License

MIT License — free to use and modify.
