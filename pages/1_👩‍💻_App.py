import streamlit as st
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import csv

# Function to read enhancements from a CSV file
def read_enhancements_from_csv(file_path):
    enhancements = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, enhancement = row
            enhancements[key] = enhancement
    return enhancements

# Function to enhance the input prompt with enhancements from a CSV file
def enhance_prompt_with_csv(prompt, csv_file_path):
    enhancements = read_enhancements_from_csv(csv_file_path)
    for key, enhancement in enhancements.items():
        if key.lower() in prompt.lower():
            prompt += " " + enhancement
            break
    general_enhancements = "Ensure high resolution, sharp focus on key elements, and a balanced composition."
    prompt += " " + general_enhancements
    return prompt

# Modified function to generate images and overlay text
def generate_images_with_text(input_text, num_images, resolution, text, font_name, font_size, x_position, y_position, text_color, stroke, shadow):
    image_outputs = []
    for _ in range(num_images):
        random_number = random.randint(1, 10000)
        enhanced_prompt = enhance_prompt_with_csv(input_text, "D:/Sudheesh/content/enhancements.csv")  # Update the path as necessary
        prompt = f"{enhanced_prompt} {random_number}"
        
        # Insert your Hugging Face API key here
        api_key = "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"
        response = requests.post(
            "https://api-inference.huggingface.co/models/prompthero/openjourney",  # Update your model path
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "inputs": prompt,
            }
        )
        
        if not response.ok:
            st.error("Failed to generate image! Error: " + response.text)
            return []
        
        image_data = response.content
        image = Image.open(BytesIO(image_data))
        if resolution == '512x512':
            image = image.resize((512, 512))
        elif resolution == '1024x1024':
            image = image.resize((1024, 1024))
        
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype(font_name, font_size)
        except IOError:
            st.error(f"Font file {font_name} not found.")
            return
        
        text_position = (x_position, y_position)
        text_color = text_color
        if stroke:
            outline_color = "black"
            draw.text((text_position[0]-1, text_position[1]-1), text, font=font, fill=outline_color)
            draw.text((text_position[0]+1, text_position[1]-1), text, font=font, fill=outline_color)
            draw.text((text_position[0]-1, text_position[1]+1), text, font=font, fill=outline_color)
            draw.text((text_position[0]+1, text_position[1]+1), text, font=font, fill=outline_color)
        if shadow:
            shadow_color = "grey"
            draw.text((text_position[0]+2, text_position[1]+2), text, font=font, fill=shadow_color)
        draw.text(text_position, text, font=font, fill=text_color)
        
        image_outputs.append(image)
    return image_outputs

# Streamlit UI
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://c.tenor.com/BN_TOsFHUtYAAAAC/tenor.gif");
    background-size: cover;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);
}
[data-testid="stSidebar"] {
    background-image: linear-gradient(to bottom right, #290e47, #341c5c);
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)
st.title("AI-Powered Image and Text Overlay Generator")
input_text = st.text_area("AI Prompt", "Describe the scene you want to generate.")
num_images = st.number_input("Number of Images", min_value=1, max_value=10, value=1)
resolution = st.selectbox("Resolution", ["512x512", "1024x1024"])
text_overlay = st.text_input("Text to Overlay", "Hello, World!")
font_name = st.text_input("Font Name", "arial.ttf")
font_size = st.slider("Font Size", 10, 100, 20)
x_position = st.slider("X Position", 0, 1000, 100)
y_position = st.slider("Y Position", 0, 1000, 50)
text_color = st.color_picker("Text Color", "#FFFFFF")
stroke = st.checkbox("Add Stroke")
shadow = st.checkbox("Add Shadow")

if st.button("Generate"):
    images = generate_images_with_text(input_text, num_images, resolution, text_overlay, font_name, font_size, x_position, y_position, text_color, stroke, shadow)
    if images:
        for image in images:
            st.image(image, use_column_width=True)
