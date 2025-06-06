import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import joblib
import os

# Load dataset
df = pd.read_csv("yieldsync/ml_model/yield.csv")
df['Yield'] = df['Production'] / df['Area']

# Label encode
le_state = LabelEncoder()
le_district = LabelEncoder()
le_season = LabelEncoder()
le_crop = LabelEncoder()

df['State'] = le_state.fit_transform(df['State'])
df['District'] = le_district.fit_transform(df['District'])
df['Season'] = le_season.fit_transform(df['Season'])
df['Crop'] = le_crop.fit_transform(df['Crop'])

X = df[['State', 'District', 'Year', 'Season', 'Crop', 'Area']]
y = df['Yield']

model = LinearRegression()
model.fit(X, y)

# Save model and encoders
joblib.dump(model, 'yieldsync/ml_model/yield_model.pkl')
joblib.dump(le_state, 'yieldsync/ml_model/le_state.pkl')
joblib.dump(le_district, 'yieldsync/ml_model/le_district.pkl')
joblib.dump(le_season, 'yieldsync/ml_model/le_season.pkl')
joblib.dump(le_crop, 'yieldsync/ml_model/le_crop.pkl')

print("Model training complete and saved.")
