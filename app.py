import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------- FUNCTIONS ---------- #

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# ---------- PROMPT ---------- #

input_prompt = """
You are an automobile expert.

Analyze the uploaded vehicle image carefully and provide details in this format:

Brand:
Model:
Launch Year:
Vehicle Type:
Key Features:
Mileage (km/l):
Average Price in India (INR):
Maintenance Details:
Approximate Resale Value after 10 years:
"""


# ---------- STREAMLIT UI ---------- #

st.set_page_config(page_title="AutoSage App")

st.header("🚗 AutoSage App - Vehicle Analyzer")

uploaded_file = st.file_uploader(
    "Choose a vehicle image...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")

# Button
if st.button("Tell me about Vehicle"):
    if uploaded_file is not None:
        with st.spinner("Analyzing vehicle... Please wait ⏳"):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)

        st.subheader("📋 Vehicle Details:")
        st.write(response)
    else:
        st.warning("Please upload an image first.")
