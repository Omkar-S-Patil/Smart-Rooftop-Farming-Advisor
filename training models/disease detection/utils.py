import tensorflow as tf
import numpy as np
from PIL import Image

# --- CONFIGURATION ---
DEMO_MODE = False  # Set to False once you retrain!

# --- TOMATO REMEDIES KNOWLEDGE BASE ---
remedies = {
    "Tomato___Bacterial_spot": {
        "status": "Infected (Bacterial)",
        "description": "Small water-soaked spots on leaves that turn brown and scabby. Can cause severe defoliation.",
        "treatment": "1. Apply copper-based fungicides (bactericides).\n2. Avoid overhead irrigation to reduce spread.\n3. Remove infected plant debris immediately."
    },
    "Tomato___Early_blight": {
        "status": "Infected (Fungal)",
        "description": "Concentric rings ('bullseye' pattern) on lower older leaves, causing yellowing.",
        "treatment": "1. Prune lower leaves to improve airflow.\n2. Apply fungicides containing Mancozeb or Chlorothalonil.\n3. Stake plants to keep leaves off the ground."
    },
    "Tomato___healthy": {
        "status": "Healthy",
        "description": "The plant appears vibrant, green, and free of lesions or pests.",
        "treatment": "1. Maintain consistent watering.\n2. Fertilize with balanced N-P-K.\n3. Monitor weekly for early signs of issues."
    },
    "Tomato___Late_blight": {
        "status": "Infected (Critical)",
        "description": "Large, dark, water-soaked patches on leaves. White fungal growth may appear on undersides.",
        "treatment": "1. Destroy infected plants immediately (highly contagious).\n2. Apply fungicides with Copper or Metalaxyl.\n3. Ensure wide spacing between plants."
    },
    "Tomato___Leaf_Mold": {
        "status": "Infected (Fungal)",
        "description": "Yellow spots on upper leaf surface, olive-green mold on the underside.",
        "treatment": "1. Reduce humidity (ventilation is key).\n2. Water at the base, not on leaves.\n3. Apply fungicides like Difenoconazole."
    },
    "Tomato___Septoria_leaf_spot": {
        "status": "Infected (Fungal)",
        "description": "Small circular spots with dark borders and gray centers.",
        "treatment": "1. Remove lower infected leaves.\n2. Apply copper-based fungicides.\n3. Rotate crops every 3 years."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "status": "Infested (Pest)",
        "description": "Yellow stippling on leaves; fine webbing may be visible.",
        "treatment": "1. Spray with Neem oil or insecticidal soap.\n2. Introduce predatory mites (natural enemies).\n3. Spray water to dislodge mites."
    },
    "Tomato___Target_Spot": {
        "status": "Infected (Fungal)",
        "description": "Brown necrotic lesions with concentric rings, similar to early blight.",
        "treatment": "1. Improve air circulation.\n2. Apply fungicides (Chlorothalonil).\n3. Remove crop residue after harvest."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "status": "Infected (Viral)",
        "description": "Leaves curl upward, turn yellow, and become stunted. Spread by whiteflies.",
        "treatment": "1. Control whiteflies with sticky traps or insecticides.\n2. Use reflective mulches.\n3. Remove and destroy infected plants (no cure)."
    },
    "Tomato___Tomato_mosaic_virus": {
        "status": "Infected (Viral)",
        "description": "Mottled light and dark green pattern on leaves. Leaves may be distorted.",
        "treatment": "1. Wash hands/tools frequently (spread by touch/tobacco).\n2. Remove infected plants.\n3. Plant resistant varieties."
    }
    # "Tomato___healthy": {
    #     "status": "Healthy",
    #     "description": "The plant appears vibrant, green, and free of lesions or pests.",
    #     "treatment": "1. Maintain consistent watering.\n2. Fertilize with balanced N-P-K.\n3. Monitor weekly for early signs of issues."
    # }
}

def load_model():
    try:
        model = tf.keras.models.load_model('models/plant_disease_model.h5')
        return model
    except:
        return None

def process_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_disease(image_file):
    image = Image.open(image_file)
    
    if DEMO_MODE:
        import random
        # Simulation: Pick a random Tomato disease
        keys = list(remedies.keys())
        predicted_class = random.choice(keys) 
        confidence = random.uniform(88.0, 99.0)
        return predicted_class, confidence, remedies.get(predicted_class)

    else:
        model = load_model()
        if model is None:
            return "Model Missing", 0.0, None
            
        processed_img = process_image(image)
        predictions = model.predict(processed_img)
        
        # Ensure these indices match your training folder order!
        class_indices = {i: k for i, k in enumerate(sorted(remedies.keys()))}
        predicted_idx = np.argmax(predictions)
        predicted_class = class_indices.get(predicted_idx, "Unknown")
        confidence = np.max(predictions) * 100
        
        return predicted_class, confidence, remedies.get(predicted_class, {})