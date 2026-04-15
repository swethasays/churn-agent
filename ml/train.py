import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
import shap
import joblib
import os

def load_and_clean():
    df = pd.read_csv("data/telco_churn.csv")

    # Fix TotalCharges blank spaces
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Drop nulls
    df.dropna(inplace=True)

    # Drop customerID
    df.drop("customerID", axis=1, inplace=True)

    # Convert target to binary
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # Encode all categorical columns
    le = LabelEncoder()
    cat_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    return df

def train_model():
    df = load_and_clean()

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Print evaluation
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Save model and feature names
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/churn_model.pkl")
    joblib.dump(list(X.columns), "models/feature_names.pkl")

    print("Model saved to models/churn_model.pkl")

if __name__ == "__main__":
    train_model()