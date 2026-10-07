import os
import requests
import streamlit as st
import pandas as pd

API_BASE_URL = os.getenv("FLASK_API_URL", "http://127.0.0.1:5000").rstrip("/")
st.set_page_config(page_title="MNIST Digit Recognition - Task 11", page_icon="🔢", layout="centered")
st.title("MNIST Digit Recognition")
st.subheader("Task 11 - Full Dockerized Application")
st.write("Upload a handwritten digit image. Streamlit runs in its own Docker container and sends the image to the Flask API container for CNN prediction.")
st.divider()
uploaded_file = st.file_uploader("Upload a handwritten digit image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", width=280)
    if st.button("Predict Digit", type="primary"):
        try:
            response = requests.post(f"{API_BASE_URL}/predict", files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")}, timeout=30)
            if response.status_code != 200:
                st.error(response.text)
            else:
                result = response.json()
                if result.get("success"):
                    digit = int(result["predicted_digit"])
                    confidence = float(result["confidence"])
                    probabilities = result["probabilities"]
                    st.success(f"Predicted Digit: {digit}")
                    st.metric("Prediction Confidence", f"{confidence * 100:.2f}%")
                    chart_data = pd.DataFrame({"Digit": list(range(10)), "Probability": probabilities}).set_index("Digit")
                    st.subheader("Prediction Probabilities")
                    st.bar_chart(chart_data)
                else:
                    st.error(result.get("error", "Prediction failed"))
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Flask API. Verify that both Docker services are running.")
        except requests.exceptions.Timeout:
            st.error("The prediction request timed out.")
else:
    st.info("Choose a PNG, JPG, or JPEG image to begin.")
st.divider()
st.info(f"Backend API: {API_BASE_URL}")