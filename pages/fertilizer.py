import streamlit as st
import joblib, pickle
import numpy as np

@st.cache_resource
def load_assets():
    model = joblib.load("models/02_fertilizer_recommendation/fertilizer_model.pkl")
    crop_enc = pickle.load(open("models/02_fertilizer_recommendation/crop_encoder.pkl", "rb"))
    stage_enc = pickle.load(open("models/02_fertilizer_recommendation/stage_encoder.pkl", "rb"))
    soil_enc = pickle.load(open("models/02_fertilizer_recommendation/soil_encoder.pkl", "rb"))
    fert_enc = pickle.load(open("models/02_fertilizer_recommendation/fert_encoder.pkl", "rb"))
    return model, crop_enc, stage_enc, soil_enc, fert_enc

def fertilizer_page():
    model, crop_encoder, stage_encoder, soil_encoder, fert_encoder = load_assets()

    st.markdown('<div class="main-title">💧 Fertilizer Recommendation</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox("Crop", crop_encoder.classes_)
    with col2:
        stage = st.selectbox("Growth Stage", stage_encoder.classes_)
    with col3:
        soil = st.selectbox("Soil Type", soil_encoder.classes_)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        N = st.number_input("Nitrogen (N)", 0, 300, 50)
    with c2:
        P = st.number_input("Phosphorus (P)", 0, 300, 30)
    with c3:
        K = st.number_input("Potassium (K)", 0, 300, 40)
    with c4:
        pH = st.number_input("pH Level", 0.0, 14.0, 7.0)

    if st.button("🌱 Recommend Fertilizer"):
        arr = np.array([[
            crop_encoder.transform([crop])[0],
            stage_encoder.transform([stage])[0],
            soil_encoder.transform([soil])[0],
            N, P, K, pH
        ]])

        pred = model.predict(arr)[0]
        fert = fert_encoder.inverse_transform([pred])[0]

        st.markdown(
            f"""
            <div style="
                background:#1e7f43;
                padding:22px;
                margin-top:30px;
                border-radius:16px;
                text-align:center;
                color:white;
                font-size:24px;
                font-weight:700;
            ">
                🌱 Recommended Fertilizer<br>
                <span style="font-size:32px;">{fert}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
