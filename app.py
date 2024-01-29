import streamlit as st 
import google.generativeai as genai 
import os 
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_icon="logo.png", page_title="Nutrition Expert", layout="centered")
def get_gemini_response(input_promt, img):
    model= genai.GenerativeModel('gemini-pro-vision')
    response= model.generate_content([input_promt, img[0]])
    return response.text

def image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data= uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
st.header("Nutrition Expert")

uploaded_file= st.file_uploader("Choose an Image....", type=["jpg", "png", "jpeg"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    

submit= st.button("Get info about calories content")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
Finally you can also mention that the food is healthy or not and also mention the percentage split ratio of carbohydrates, fats ,proteins and sugar in detected food items and suggest what is required in out diet to be healthy
"""

if submit:
    img= image_setup(uploaded_file)
    response= get_gemini_response(input_prompt, img)
    st.header("The response is")
    st.write(response)
