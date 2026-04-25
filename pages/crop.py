import streamlit as st
import joblib, pickle
import numpy as np
import pandas as pd
import requests

from utils.watering import generate_watering_advice

@st.cache_resource
def load_crop_assets():
    pipeline = joblib.load("models/01_crop_recommendation/crop_xgb_pipeline.pkl")
    crop_enc = pickle.load(open("models/01_crop_recommendation/crop_encoder.pkl", "rb"))
    crop_dict = pickle.load(open("models/01_crop_recommendation/crop_dict.pkl", "rb"))


    district_encoder = pickle.load(open("models/01_crop_recommendation/district_encoder.pkl", "rb"))
    month_encoder = pickle.load(open("models/01_crop_recommendation/month_encoder.pkl", "rb"))
    soil_encoder = pickle.load(open("models/01_crop_recommendation/soil_encoder.pkl", "rb"))

    return pipeline, crop_enc, crop_dict, district_encoder, month_encoder, soil_encoder

pipeline, crop_enc, crop_dict, district_encoder, month_encoder, soil_encoder = load_crop_assets()


def get_weather(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            st.error(f"City not found or API error: {data.get('message')}")
            return None

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        rainfall = data.get("rain", {}).get("1h", 0)

        cloud = data["clouds"]["all"]
        sunlight_lux = (100 - cloud) / 100 * 50000  # ✅ convert to lux

        return temp, humidity, rainfall, sunlight_lux

    except Exception as e:
        st.error(f"Error fetching weather: {e}")
        return None


def crop_page():
    st.markdown('<div class="main-title">🌾 Crop Recommendation</div>', unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)
    with col1:
        district = st.selectbox("District / City", district_encoder.classes_)
    with col2:
        month = st.selectbox("Month", month_encoder.classes_)
    with col3:
        soil = st.selectbox("Soil Type", soil_encoder.classes_)

    api_key = "6e88e0c1ab371a9bad70427cdcade614"
    weather_data = get_weather(district, api_key)

    if weather_data:
        temp, humidity, rainfall, sunlight = weather_data
        st.markdown(
            f"""
            <div style="
                background: rgba(30,127,67,0.85);
                padding:14px 20px;
                border-radius:12px;
                color:white;
                font-size:16px;
                font-weight:600;
                margin-bottom:20px;
            ">
                🌡 Temp: {temp} °C |
                💧 Humidity: {humidity}% |
                ☔ Rainfall: {rainfall} mm |
                ☀️ Sunlight: {sunlight}%
            </div>
            """,
            unsafe_allow_html=True
        )



    else:
        st.warning("Weather data not available for this district.")


    N = st.number_input("N (Nitrogen)", 0, 200, 70)
    P = st.number_input("P (Phosphorus)", 0, 100, 40)
    K = st.number_input("K (Potassium)", 0, 100, 40)
    ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)


    if st.button("🌱 Recommend Crop"):
        if not weather_data:
            st.warning("Cannot recommend crop without weather data.")
        else:

            X = pd.DataFrame([{
                "District": district_encoder.transform([district])[0],
                "Month": month_encoder.transform([month])[0],
                "Soil_Type": soil_encoder.transform([soil])[0],

                "N": N,
                "P": P,
                "K": K,
                "pH": ph,

                "Temperature_C": temp,
                "Humidity_%": humidity,
                "Rainfall_mm": rainfall,
                "Sunlight_lux": sunlight
            }])

            pred_probs = pipeline.predict_proba(X)[0]
            top3_idx = np.argsort(pred_probs)[::-1][:3]

            st.markdown("## 🌾 Top 3 Recommended Crops")

            # for idx in top3_idx:
            #     crop_name = crop_dict[idx]
            #     prob = pred_probs[idx] * 100

            for idx in top3_idx:
                crop_name = crop_dict[idx]
                prob = pred_probs[idx] * 100

                # 🔥 Generate watering advice
                watering = generate_watering_advice(
                    soil=soil,
                    temp=temp,
                    humidity=humidity,
                    rainfall=rainfall,
                    crop=crop_name
                )

                # 🌱 Crop Card
                st.markdown(f"""
                    <div style="
                        background:#1e7f43;
                        padding:22px;
                        border-radius:16px;
                        text-align:center;
                        color:white;
                        margin-top:20px;
                        font-size:24px;
                        font-weight:700;
                    ">
                        🌱 <b>Recommended Crop:</b><br>
                        <span style="font-size:24px;">{crop_name}</span><br>
                        💧 <b>Watering Advice:</b><br>
                        <span style="font-size:24px;">{watering}</span>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
