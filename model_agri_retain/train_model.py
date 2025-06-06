# ml/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv('dataset/churndataset.csv')
df.columns = df.columns.str.strip()
df = df.replace(' ', pd.NA).dropna()

# Preprocessing
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
df['SeniorCitizen'] = df['SeniorCitizen'].astype(int)

categorical_cols = [
    'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
    'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df.drop(['customerID', 'Churn', 'TotalCharges'], axis=1)
y = df['Churn']

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump((model, X.columns), 'model_agri_retain/churn_model.pkl')
print("Model trained and saved.")
