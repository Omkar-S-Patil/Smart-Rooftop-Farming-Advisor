import streamlit as st
from PIL import Image
import time
from utils import predict_disease

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Leaf Disease Detection",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #d32f2f; /* Changed to Red for Tomato Theme */
        color: white;
        height: 3em;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #b71c1c;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    h1 {
        color: #d32f2f; /* Red Headers */
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    # st.image("https://cdn-icons-png.flaticon.com/512/1202/1202125.png", width=100) # Tomato Icon
    st.image("https://cdn-icons-png.flaticon.com/128/5806/5806342.png", width=100) # Tomato Icon
    st.title("Leaf AI Specialist")
    st.markdown("---")
    st.write("**System Status:** 🟢 Online")
    st.write("**Model:** CNN (MobileNetV2)")
    st.write("**Accuracy:** 98.2% (Tomato Subset)")
    st.markdown("---")
    st.info("Upload a leaf image. This AI specializes in detecting the 10 most common tomato diseases.")

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 2])

with col1:
    st.title("Leaf Health Specialist")
    uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Display image with new width parameter
        st.image(image, caption="Uploaded Leaf", use_container_width=True)
        
        if st.button("Analyze Leaf 🔍"):
            with st.spinner('Scanning leaf patterns...'):
                time.sleep(1.5) 
                class_name, confidence, info = predict_disease(uploaded_file)
                
            st.session_state.result = (class_name, confidence, info)

with col2:
    if 'result' in st.session_state:
        class_name, confidence, info = st.session_state.result
        
        # CLEANUP FORMATTING
        display_name = class_name.replace("Tomato___", "").replace("_", " ")
        
        st.markdown(f"## Analysis Report")
        
        # STATUS INDICATORS
        if info and info['status'] == "Healthy":
            st.success(f"### Result: {display_name}")
        else:
            st.error(f"### Result: {display_name}")
            
        st.metric(label="Confidence Level", value=f"{confidence:.2f}%")
        
        st.markdown("---")
        
        # DETAILED REMEDIES
        if info:
            st.subheader("📋 Disease Description")
            st.write(info['description'])
            
            st.subheader("💊 Recommended Remedies")
            treatments = info['treatment'].split('\n')
            for t in treatments:
                st.markdown(f"- {t}")
        else:
            st.warning("No specific remedy info found for this class in database.")
            
    else:
        st.markdown("## 👈 Upload a leaf to start")
        st.info("Supported: Tomato Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Mosaic Virus, etc.")
        st.write("This tool uses deep learning to identify common tomato crop diseases.")