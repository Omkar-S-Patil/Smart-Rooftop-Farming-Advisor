import streamlit as st
from utils.common import load_img

def home_page():
    crop_img = load_img("assets/crop_recommendation.png")
    fert_img = load_img("assets/fertilizer_prediction.png")
    disease_img = load_img("assets/disease_detection.png")

    st.markdown('<div class="main-title">Smart Rooftop Farming Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AI-powered decision support system for urban farming</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/png;base64,{crop_img}" class="card-img">
            <h3>🌾 Crop Recommendation</h3>
            <p>
                Recommends the most suitable crop based on soil type,
                environmental conditions and seasonal patterns using
                machine learning classification.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("Explore Crop Recommendation"):
            st.session_state.page = "crop"
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/png;base64,{fert_img}" class="card-img">
            <h3>🧪 Fertilizer Recommendation</h3>
            <p>
                Predicts the optimal fertilizer using nutrient values
                (N, P, K), soil characteristics, crop and growth
                stage to maximize yield.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("Explore Fertilizer Recommendation"):
            st.session_state.page = "fertilizer"
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <img src="data:image/png;base64,{disease_img}" class="card-img">
            <h3>🦠 Disease Detection</h3>
            <p>
                Detects plant diseases from leaf images
                and provides early-stage treatment
                recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        if st.button("Explore Disease Detection"):
            st.session_state.page = "disease"
        st.markdown('</div>', unsafe_allow_html=True)
