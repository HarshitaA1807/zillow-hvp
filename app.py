
import streamlit as st
import pickle
import numpy as np

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def format_indian(number):
    """Format number in Indian style (e.g., 1,23,45,678)"""
    num_str = str(int(number))
    if len(num_str) <= 3:
        return num_str
    last_three = num_str[-3:]
    rest = num_str[:-3]
    if rest:
        rest_formatted = rest[::-1]
        rest_formatted = ','.join(rest_formatted[i:i+2] for i in range(0, len(rest_formatted), 2))
        rest_formatted = rest_formatted[::-1]
        return rest_formatted + ',' + last_three
    return last_three

st.title("🏠 Zillow Home Value Predictor")

st.subheader("Enter Property Details")

bedrooms = st.number_input("Bedrooms", 1, 10, 3)
bathrooms = st.number_input("Bathrooms", 1, 10, 2)
sqft = st.number_input("Square Feet", 500, 10000, 1500)
floors = st.number_input("Floors", 1, 5, 1)

if st.button("Predict Price"):
    
    data = np.array([[bedrooms, bathrooms, sqft, floors]])
    
    prediction_usd = float(model.predict(data)[0])
    
    usd_to_inr = 83.5
    prediction_inr = prediction_usd * usd_to_inr
    
    formatted_price = format_indian(prediction_inr)
    
    st.success(f"Estimated Home Value: ₹{formatted_price}")
    
    if prediction_inr >= 10000000:
        crores = prediction_inr / 10000000
        st.info(f"📊 ≈ ₹{crores:.2f} Crore")
    elif prediction_inr >= 100000:
        lakhs = prediction_inr / 100000
        st.info(f"📊 ≈ ₹{lakhs:.2f} Lakh")
    

    
