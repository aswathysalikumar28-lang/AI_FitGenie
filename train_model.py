import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("fitness_data.csv")

goal_encoder = LabelEncoder()
df["Goal"] = goal_encoder.fit_transform(df["Goal"])

X = df[["Age","BMI","Goal"]]
y = df["Workout"]

model = RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"workout_model.pkl")
joblib.dump(goal_encoder,"goal_encoder.pkl")

print("Model Saved")