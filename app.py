
import streamlit as st
import pickle
import numpy as np

with open("model.pkl","rb") as f:
    model = pickle.load(f)

st.title("🏠 Zillow Home Value Predictor")

st.subheader("Enter Property Details")

bedrooms = st.number_input(
    "Bedrooms", 1, 10, 3
)

bathrooms = st.number_input(
    "Bathrooms", 1, 10, 2
)

sqft = st.number_input(
    "Square Feet", 500, 10000, 1500
)

floors = st.number_input(
    "Floors", 1, 5, 1
)

if st.button("Predict Price"):

    data = np.array([
        [bedrooms, bathrooms, sqft, floors]
    ])
    
    prediction_inr = model.predict(data)[0]

    usd_to_inr = 83.5
    prediction_inr = prediction_usd * usd_to_inr

    st.success(
        f"Estimated Home Value: ₹{prediction:,.0f}"
    )
    

    
