import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
import os

# --- SETTINGS ---
# IMPORTANT: You must download the 'PlantVillage' dataset from Kaggle
# and extract it into a folder named 'dataset' inside your project.
DATA_DIR = 'dataset/PlantVillage' 
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

def train():
    if not os.path.exists(DATA_DIR):
        print(f"ERROR: Dataset not found at {DATA_DIR}")
        print("Please download PlantVillage dataset from Kaggle and place it in the 'dataset' folder.")
        return

    # Data Generators (Augmentation)
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = train_datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    # Base Model (Transfer Learning)
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False  # Freeze base layers

    # Custom Head
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(train_generator.num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("Starting Training...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS
    )

    # Save Model
    if not os.path.exists('models'):
        os.makedirs('models')
    model.save('models/plant_disease_model.h5')
    print("Model saved to models/plant_disease_model.h5")

if __name__ == "__main__":
    train()