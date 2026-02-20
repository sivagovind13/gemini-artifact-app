from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import random

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)


# Function to process uploaded image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image = {
            'mime_type': uploaded_file.type,
            'data': bytes_data
        }
        return image
    return None


# Function to get Gemini response
def get_gemini_response(input_text, image=None, prompt=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if image:
        response = model.generate_content([input_text, image, prompt])
    else:
        response = model.generate_content([input_text, prompt])
    return response.text


# Streamlit UI
st.set_page_config(page_title="Gemini Historical Artifact Description App", page_icon="🏺")
st.title("Gemini Historical Artifact Description App")

artifact_name = st.text_input("Enter Artifact Name or Historical Period:")
word_count = st.number_input("Desired Word Count:", min_value=100, max_value=3000, value=800, step=100)

uploaded_file = st.file_uploader("Upload an image of the artifact (optional):", type=["jpg", "jpeg", "png"])

historical_facts = [
    "The Rosetta Stone helped decipher Egyptian hieroglyphs.",
    "Leonardo da Vinci wrote in mirror script.",
    "The Bayeux Tapestry is nearly 70 meters long.",
    "Tutankhamun's tomb was discovered in 1922."
]

if st.button("Generate Artifact Description"):
    if artifact_name:
        with st.spinner(random.choice(historical_facts)):
            try:
                image = input_image_setup(uploaded_file)

                prompt = f"""
                Generate a detailed description of '{artifact_name}'
                in about {word_count} words.
                Include origin, materials, historical significance and cultural impact.
                """

                description = get_gemini_response(artifact_name, image, prompt)

                st.subheader("Generated Description:")
                st.write(description)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter artifact name.")