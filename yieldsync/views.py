from django.shortcuts import render
import joblib
import numpy as np

def predict_yield(request):
    if request.method == 'POST':
        state = request.POST['state']
        district = request.POST['district']
        year = int(request.POST['year'])
        season = request.POST['season']
        crop = request.POST['crop']
        area = float(request.POST['area'])

        # Load model and encoders
        model = joblib.load('yieldsync/ml_model/yield_model.pkl')
        le_state = joblib.load('yieldsync/ml_model/le_state.pkl')
        le_district = joblib.load('yieldsync/ml_model/le_district.pkl')
        le_season = joblib.load('yieldsync/ml_model/le_season.pkl')
        le_crop = joblib.load('yieldsync/ml_model/le_crop.pkl')

        input_data = np.array([[
            le_state.transform([state])[0],
            le_district.transform([district])[0],
            year,
            le_season.transform([season])[0],
            le_crop.transform([crop])[0],
            area
        ]])

        prediction = model.predict(input_data)[0]
        return render(request, 'prediction/result.html', {'yield_prediction': round(prediction, 2)})

    return render(request, 'prediction/form.html')
