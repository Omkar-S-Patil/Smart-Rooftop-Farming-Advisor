import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image


MODEL_PATH = "models/03_disease_detection/plant_disease_model.h5"

@st.cache_resource
def load_model():
    try:
        return tf.keras.models.load_model(MODEL_PATH)
    except:
        return None



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
}


def process_image(image):
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def disease_page():

    st.markdown('<div class="main-title">🦠 Tomato Disease Detection</div>', unsafe_allow_html=True)

    model = load_model()
    if model is None:
        st.error("Model file not found!")
        return

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("Upload Tomato Leaf Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)

    with col2:
        if uploaded_file and st.button("🔍 Analyze Leaf"):

            processed_img = process_image(image)
            predictions = model.predict(processed_img)

            class_indices = {i: k for i, k in enumerate(sorted(remedies.keys()))}

            predicted_idx = np.argmax(predictions)
            predicted_class = class_indices.get(predicted_idx, "Unknown")
            confidence = float(np.max(predictions)) * 100

            info = remedies.get(predicted_class, {})

            st.markdown(
                f"""
                <div style="
                    background:#1e7f43;
                    padding:22px;
                    margin-top:30px;
                    border-radius:16px;
                    text-align:left;
                    color:white;
                    font-size:18px;
                    font-weight:500;
                ">
                    <center>
                    <span style="font-size:26px; font-weight:700;">
                        🧪 {predicted_class.replace('Tomato___', '').replace('_', ' ')}
                    </span><br><br>
                    Confidence: {confidence:.2f}%
                    </center>
                    <br>
                    <b>Status:</b> {info.get("status","-")}<br><br>
                    <b>Description:</b> {info.get("description","-")}<br><br>
                    <b>Treatment:</b><br>
                    {info.get("treatment","-").replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"