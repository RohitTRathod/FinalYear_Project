import os
import pickle
from django.shortcuts import render
from seedsense.forms import CropInputForm  # adjust import as needed

# Construct the correct path to the model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model_seedsense', 'crop_recommendation_model.pkl')

# Load the model once
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

def recommend_crop(request):
    prediction = None
    if request.method == 'POST':
        form = CropInputForm(request.POST)
        if form.is_valid():
            data = [
                form.cleaned_data['N'],
                form.cleaned_data['P'],
                form.cleaned_data['K'],
                form.cleaned_data['temperature'],
                form.cleaned_data['humidity'],
                form.cleaned_data['ph'],
                form.cleaned_data['rainfall']
            ]
            prediction = model.predict([data])[0]
    else:
        form = CropInputForm()

    return render(request, 'seedsense/recommend_crop.html', {'form': form, 'prediction': prediction})
