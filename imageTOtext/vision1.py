from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

## Function to load Gemini Pro Model and get responses
def get_gemini_response(input, image, api_key):
    genai.configure(api_key=api_key)  # Configure with the provided API key
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)

    return response.text

## Initialize our Streamlit app
st.set_page_config(page_title="Text Extracter")
st.header("SecuQR Application")

# User enters API key at runtime
api_key = st.text_input("Enter your Gemini API key:", type="password")

input = st.text_input("Input Prompt:", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Enter")

## When submit is clicked
if submit:
    if api_key:
        try:
            response = get_gemini_response(input, image, api_key)
            st.header("The Response is:")
            st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a valid API key.")
