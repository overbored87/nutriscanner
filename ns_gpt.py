# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 16:15:16 2025
@author: User
"""
import streamlit as st
from PIL import Image
import openai
import os
import io
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Configure OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Streamlit UI
st.title("🍽️ AI Nutritional Scanner")
st.write("Upload or take a photo of a food menu/signboard and get nutritional info!")

# Image capture using HTML5 camera API
st.write("### Capture or Upload an Image")
image_capture_html = """
<input type="file" accept="image/*" capture="environment">
"""
st.markdown(image_capture_html, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Or upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    # Convert image to base64 string
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="JPEG")
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    
    # Send to OpenAI GPT-4V (Vision Model)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract food items and provide estimated calories and sodium content."},
            {"role": "user", "content": [
                {"type": "text", "text": "What food items are in this image? Provide estimated calories and sodium content."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
            ]}
        ]
    )
    
    # Extracted text
    extracted_text = response.choices[0].message.content
    st.write("### Estimated Nutritional Information")
    st.write(extracted_text)
    
    st.success("Done! Try another image.")

