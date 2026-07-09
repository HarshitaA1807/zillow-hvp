
import streamlit as st
import pickle
import numpy as np
import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="🏠 Zillow Home Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 30px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 20px rgba(255, 75, 75, 0.4);
    }
    
    /* Success card */
    .result-card {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .result-card h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
    }
    .result-card p {
        color: #e8f5e9;
        font-size: 1.2rem;
        margin: 10px 0 0 0;
    }
    
    /* Info boxes */
    .info-box {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* Metric boxes */
    .metric-box {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL ====================
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("❌ Model file 'model.pkl' not found! Please upload it to the same folder.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()

model = load_model()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/real-estate.png", width=80)
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    
    # Exchange rate setting
    usd_to_inr = st.number_input(
        "💱 USD to INR Rate",
        min_value=50.0,
        max_value=100.0,
        value=83.5,
        step=0.1,
        help="Current exchange rate"
    )
    
    st.markdown("---")
    st.info("📊 **How it works**\n\nEnter property details and click 'Predict Price' to get an estimated home value in Indian Rupees.")
    
    st.markdown("---")
    st.caption(f"📅 Last updated: {datetime.datetime.now().strftime('%B %d, %Y')}")
    st.caption("🏗️ Built with Streamlit ❤️")

# ==================== MAIN CONTENT ====================
# Title
st.markdown('<h1 class="main-title">🏠 Zillow Home Value Predictor</h1>', unsafe_allow_html=True)
st.markdown("### 🇮🇳 Converted to Indian Rupees (₹)")
st.markdown("---")

# ==================== INPUT SECTION ====================
st.subheader("📝 Enter Property Details")

# Create two rows of columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    bedrooms = st.number_input("🛏️ Bedrooms", min_value=1, max_value=10, value=3, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    bathrooms = st.number_input("🛁 Bathrooms", min_value=1, max_value=10, value=2, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    sqft = st.number_input("📐 Square Feet", min_value=500, max_value=10000, value=1500, step=100)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    floors = st.number_input("🏗️ Floors", min_value=1, max_value=5, value=1, step=1)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== PREDICT BUTTON ====================
if st.button("🔮 Predict Price", type="primary"):
    try:
        # Show loading spinner
        with st.spinner("💰 Calculating your home value..."):
            # Prepare data
            data = np.array([[bedrooms, bathrooms, sqft, floors]])
            
            # Make prediction
            prediction_usd = float(model.predict(data)[0])
            prediction_inr = prediction_usd * usd_to_inr
            
            # ==================== DISPLAY RESULTS ====================
            st.markdown("### 📊 Prediction Results")
            
            # Result card with INR
            st.markdown(f"""
                <div class="result-card">
                    <p style="color: #e8f5e9; font-size: 1.2rem;">Estimated Home Value</p>
                    <h1>₹{prediction_inr:,.0f}</h1>
                    <p>≈ ${prediction_usd:,.0f} USD</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="💰 INR Value",
                    value=f"₹{prediction_inr:,.0f}",
                    delta=f"+{(prediction_inr/100000):.1f}K"
                )
            
            with col2:
                st.metric(
                    label="💵 USD Value",
                    value=f"${prediction_usd:,.0f}",
                    delta=f"{(prediction_usd/1000):.1f}K"
                )
            
            with col3:
                if prediction_inr >= 10000000:  # 1 Crore+
                    crores = prediction_inr / 10000000
                    st.metric(
                        label="📈 In Crores",
                        value=f"₹{crores:.2f} Cr",
                        delta="High Value"
                    )
                elif prediction_inr >= 100000:  # 1 Lakh+
                    lakhs = prediction_inr / 100000
                    st.metric(
                        label="📈 In Lakhs",
                        value=f"₹{lakhs:.2f} L",
                        delta="Medium Value"
                    )
                else:
                    st.metric(
                        label="📈 In Rupees",
                        value=f"₹{prediction_inr:,.0f}",
                        delta="Standard Value"
                    )
            
            # ==================== ADDITIONAL INFO ====================
            st.markdown("---")
            st.markdown("### 📋 Property Summary")
            
            summary_col1, summary_col2 = st.columns(2)
            with summary_col1:
                st.markdown(f"""
                    <div class="info-box">
                        <b>🏠 Bedrooms:</b> {bedrooms}<br>
                        <b>🛁 Bathrooms:</b> {bathrooms}<br>
                        <b>📐 Square Feet:</b> {sqft:,}<br>
                        <b>🏗️ Floors:</b> {floors}
                    </div>
                """, unsafe_allow_html=True)
            
            with summary_col2:
                st.markdown(f"""
                    <div class="info-box">
                        <b>💰 Estimated Value:</b> ₹{prediction_inr:,.0f}<br>
                        <b>💱 Exchange Rate:</b> 1 USD = ₹{usd_to_inr}<br>
                        <b>📅 Date:</b> {datetime.datetime.now().strftime('%B %d, %Y')}<br>
                        <b>📍 Currency:</b> Indian Rupee (₹)
                    </div>
                """, unsafe_allow_html=True)
            
            # ==================== CELEBRATION ====================
            st.balloons()
            
            st.success("✅ Prediction completed successfully!")
            
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")
        st.info("Please check your input values and try again.")

# ==================== FOOTER ====================
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("🏠 Zillow Home Value Predictor")
with footer_col2:
    st.caption("🇮🇳 Indian Rupee (₹)")
with footer_col3:
    st.caption(f"📅 {datetime.datetime.now().year}")

# ==================== HIDE STREAMLIT STYLE ====================
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
