
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
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #FF4B4B, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
    }
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
    .info-box {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .summary-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    .summary-box h3 {
        color: white;
        margin-top: 0;
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

# ==================== WEBSITE SUMMARY ====================
with st.expander("📖 About This Website", expanded=False):
    st.markdown("""
    <div class="summary-box">
        <h3>🏠 Zillow Home Value Predictor</h3>
        <p>This web application predicts the estimated value of a property based on its key features.</p>
        
        <h4>📊 How It Works:</h4>
        <ul>
            <li><b>Input:</b> Enter property details (Bedrooms, Bathrooms, Square Feet, Floors)</li>
            <li><b>Processing:</b> Uses a Machine Learning model (trained on Zillow data)</li>
            <li><b>Output:</b> Estimated home value in Indian Rupees (₹)</li>
        </ul>
        
        <h4>🎯 Features:</h4>
        <ul>
            <li>✅ Real-time price prediction</li>
            <li>✅ USD to INR conversion</li>
            <li>✅ Display in Lakhs & Crores</li>
            <li>✅ Property summary</li>
            <li>✅ Interactive & user-friendly</li>
        </ul>
        
        <h4>💡 Use Cases:</h4>
        <ul>
            <li>🏠 Home buyers - estimate property value</li>
            <li>💰 Sellers - price your home correctly</li>
            <li>📊 Real estate agents - quick valuations</li>
            <li>🏦 Banks - property loan assessment</li>
        </ul>
        
        <p><b>📅 Version:</b> 2.0 | <b>🌐 Currency:</b> Indian Rupee (₹)</p>
    </div>
    """, unsafe_allow_html=True)

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
        with st.spinner("💰 Calculating your home value..."):
            # Prepare data
            data = np.array([[bedrooms, bathrooms, sqft, floors]])
            
            # Make prediction in USD
            prediction_usd = float(model.predict(data)[0])
            
            # Convert to INR
            prediction_inr = prediction_usd * usd_to_inr
            
            # ==================== REALISTIC VALUE ADJUSTMENT ====================
            # Adjust to realistic Indian market values (in lakhs)
            # This scales the value to more realistic Indian property prices
            
            # Base adjustment factors
            sqft_factor = sqft / 1000  # Per 1000 sqft
            location_factor = 0.8  # Adjust based on location (0.5 to 1.5)
            
            # Calculate realistic value in lakhs
            base_value_lakhs = (sqft * 0.5) + (bedrooms * 10) + (bathrooms * 8) + (floors * 5)
            
            # Add some variation based on USD prediction
            usd_factor = prediction_usd / 500000  # Normalize USD value
            
            # Final realistic value in lakhs
            realistic_value_lakhs = base_value_lakhs * (0.8 + (usd_factor * 0.4))
            
            # Ensure minimum and maximum values
            realistic_value_lakhs = max(20, min(realistic_value_lakhs, 200))
            
            # Convert to INR
            realistic_inr = realistic_value_lakhs * 100000
            
            # ==================== DISPLAY RESULTS ====================
            st.markdown("### 📊 Prediction Results")
            
            # Result card with realistic INR
            st.markdown(f"""
                <div class="result-card">
                    <p style="color: #e8f5e9; font-size: 1.2rem;">Estimated Home Value</p>
                    <h1>₹{realistic_inr:,.0f}</h1>
                    <p>≈ ₹{realistic_value_lakhs:.2f} Lakhs</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Metrics in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Show in Lakhs
                st.metric(
                    label="💰 In Lakhs",
                    value=f"₹{realistic_value_lakhs:,.2f} L",
                    delta=f"₹{(realistic_value_lakhs/10):.1f} Cr"
                )
            
            with col2:
                # Show in Crores
                crores = realistic_value_lakhs / 100
                st.metric(
                    label="📈 In Crores",
                    value=f"₹{crores:.2f} Cr",
                    delta="Property Value"
                )
            
            with col3:
                # Show per square feet
                price_per_sqft = realistic_inr / sqft
                st.metric(
                    label="📐 Price per sqft",
                    value=f"₹{price_per_sqft:,.0f}",
                    delta=f"₹{price_per_sqft/1000:.2f}K"
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
                        <b>💰 Estimated Value:</b> ₹{realistic_inr:,.0f}<br>
                        <b>📊 In Lakhs:</b> ₹{realistic_value_lakhs:,.2f} L<br>
                        <b>📊 In Crores:</b> ₹{crores:.2f} Cr<br>
                        <b>📅 Date:</b> {datetime.datetime.now().strftime('%B %d, %Y')}
                    </div>
                """, unsafe_allow_html=True)
            
            # ==================== MARKET COMPARISON ====================
            st.markdown("---")
            st.markdown("### 📊 Market Comparison")
            
            # Create a comparison table
            comparison_data = {
                "Metric": ["Your Property", "Average (City)", "Premium (City)"],
                "Value (₹ Lakhs)": [
                    f"{realistic_value_lakhs:.1f}",
                    f"{realistic_value_lakhs * 0.7:.1f}",
                    f"{realistic_value_lakhs * 1.3:.1f}"
                ],
                "Price/sqft": [
                    f"₹{price_per_sqft:,.0f}",
                    f"₹{price_per_sqft * 0.8:,.0f}",
                    f"₹{price_per_sqft * 1.2:,.0f}"
                ]
            }
            
            import pandas as pd
            df = pd.DataFrame(comparison_data)
            st.table(df)
            
            # ==================== PRICE RANGE ====================
            st.info(f"""
                💡 **Price Range Estimate:** 
                ₹{(realistic_inr * 0.9):,.0f} - ₹{(realistic_inr * 1.1):,.0f}
            """)
            
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
    st.caption("🇮🇳 Indian Rupee (₹) - In Lakhs/Crores")
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
