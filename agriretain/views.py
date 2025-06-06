import joblib
import pandas as pd
from django.shortcuts import render

# Load model at module level
model, feature_names = joblib.load('model_agri_retain/churn_model.pkl')

def predict_churn(request):
    if request.method == 'POST':
        # Gather inputs from form
        form_data = request.POST.dict()
        form_data.pop('csrfmiddlewaretoken', None)

        input_df = pd.DataFrame([form_data])

        # One-hot encode manually to match training features
        input_df = pd.get_dummies(input_df)
        for col in feature_names:
            if col not in input_df.columns:
                input_df[col] = 0  # Fill missing dummy columns

        input_df = input_df[feature_names]  # Reorder

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        context = {
            'prediction': 'Yes' if prediction == 1 else 'No',
            'probability': round(probability * 100, 2),
        }
        return render(request, 'agriretain/result.html', context)

    return render(request, 'agriretain/form.html')
