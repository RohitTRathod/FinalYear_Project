import os
import uuid
import json
import numpy as np
import tensorflow as tf
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from tensorflow.keras.preprocessing import image

# Load your trained model
model = tf.keras.models.load_model('model_agro_lens/plant_disease_model.h5')

# Load class names from saved class_indices.json
with open('model_agro_lens/class_indices.json') as f:
    class_indices = json.load(f)

# Convert class_indices dict to ordered list
class_names = [None] * len(class_indices)
for label, index in class_indices.items():
    class_names[index] = label

def indexlens(request):
    if request.method == 'POST' and request.FILES.get('image'):
        img = request.FILES['image']

        #  Sanitize file name
        fs = FileSystemStorage(location='media/uploaded_images')
        filename = f"{uuid.uuid4().hex}.jpg"
        file_path = fs.save(filename, img)
        full_path = fs.path(file_path)

        #  Preprocess image
        img_loaded = image.load_img(full_path, target_size=(128, 128))
        img_array = image.img_to_array(img_loaded) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        #  Predict
        prediction = model.predict(img_array)
        predicted_index = np.argmax(prediction)
        predicted_class = class_names[predicted_index] if predicted_index < len(class_names) else "Unknown"

        
        return render(request, 'agrolens/indexlens.html', {
            'predicted_class': predicted_class,
            'image_url': fs.url(file_path)
        })

    return render(request, 'agrolens/indexlens.html')
