import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Set paths
train_dir = 'dataset/plantdisease'
model_dir = 'model_agro_lens'
os.makedirs(model_dir, exist_ok=True)

# Image generator
train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical'
)

# Define model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train
model.fit(train_generator, epochs=5)

# Save model
model.save(os.path.join(model_dir, 'plant_disease_model.h5'))

# Save class indices
with open(os.path.join(model_dir, 'class_indices.json'), 'w') as f:
    json.dump(train_generator.class_indices, f)

print("Model and class indices saved successfully.")
