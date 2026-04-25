import streamlit as st
import base64
import os

def set_background(image_path: str):
    if not os.path.exists(image_path):
        return
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(
                rgba(0,0,0,0.45),
                rgba(0,0,0,0.45)
            ),
            url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def load_global_css():
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-top: 30px;
    }
    .sub-title {
        text-align: center;
        color: #e0f2f1;
        font-size: 1.2rem;
        margin-bottom: 50px;
    }
    label {
        color: white !important;
        font-weight: 600 !important;
    }
    .card {
        background: rgba(255,255,255,0.92);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        text-align: center;
        height: 320px;
    }
    .card-img {
        width: 160px;
        height: 100px;
        object-fit: contain;
        margin-bottom: 18px;
    }
    .stButton > button {
        background-color: #2e7d32;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 1rem;
    }
    .stButton > button:hover {
        background-color: #1b5e20;
    }
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1b5e20;
        margin-bottom: 15px;
    }
    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 18px;   
    }
    </style>
    """, unsafe_allow_html=True)
