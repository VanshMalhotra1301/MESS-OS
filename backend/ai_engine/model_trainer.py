import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "../../data/random_mess_data_10000.csv")
MODEL_PATH = os.path.join(BASE_DIR, "food_waste_model.pkl")


def train_model():
    print("⏳ Loading dataset...")

    if not os.path.exists(DATA_PATH):
        print(f"❌ Dataset not found at: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    # --- Convert date ---
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # --- Time-based features ---
    df['day_of_week_num'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)
    df['is_weekend'] = (df['day_of_week_num'] >= 5).astype(int)

    # --- Encode meal type ---
    le_meal = LabelEncoder()
    df['meal_type_encoded'] = le_meal.fit_transform(df['meal_type'].str.lower())

    # --- Lag features ---
    df['lag_1'] = df['actual_attendance'].shift(1)
    df['lag_4'] = df['actual_attendance'].shift(4)
    df['lag_28'] = df['actual_attendance'].shift(28)

    # --- Rolling features ---
    df['rolling_7_mean'] = df['actual_attendance'].rolling(7).mean()
    df['rolling_14_mean'] = df['actual_attendance'].rolling(14).mean()

    # Remove rows with NaNs
    df = df.dropna()

    print(f"📊 Training samples after preprocessing: {len(df)}")

    # --- Feature list ---
    feature_order = [
        'day_of_week_num',
        'month',
        'day_of_year',
        'week_of_year',
        'is_weekend',
        'meal_type_encoded',
        'total_strength',
        'lag_1',
        'lag_4',
        'lag_28',
        'rolling_7_mean',
        'rolling_14_mean'
    ]

    X = df[feature_order]
    y = df['actual_attendance']

    # --- Time-based split ---
    split_index = int(len(df) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    print(f"🧪 Train size: {len(X_train)} | Test size: {len(X_test)}")

    # --- Model ---
    model = XGBRegressor(
        n_estimators=1200,
        learning_rate=0.03,
        max_depth=6,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_alpha=0.5,
        reg_lambda=1.0,
        random_state=42,
        n_jobs=-1
    )

    print("🧠 Training model...")
    model.fit(X_train, y_train)

    # --- Evaluation ---
    preds = model.predict(X_test)
    score = r2_score(y_test, preds)

    print(f"✅ Final R² Score: {score:.4f}")

    # --- Save artifacts ---
    artifacts = {
        'model': model,
        'le_meal': le_meal,
        'feature_order': feature_order
    }

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(artifacts, f)

    print(f"💾 Model saved successfully to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()
