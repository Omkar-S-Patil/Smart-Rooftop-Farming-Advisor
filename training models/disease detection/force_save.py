import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os

# 1. Define the folder (so it doesn't crash)
if not os.path.exists('models'):
    os.makedirs('models')

# 2. Build the Model Structure (Exactly like the real one)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
# We assume 16 classes (standard for PlantVillage subset)
predictions = Dense(16, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

# 3. SAVE IT NOW
print("⚠️ Generating model file without training...")
model.save('models/plant_disease_model.h5')
print("✅ DONE! You have your 'plant_disease_model.h5' file.")
print("🚀 You can now push to GitHub.")