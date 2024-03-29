import streamlit as st
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import csv
import speech_recognition as sr

# Function to read enhancements from a CSV file
def read_enhancements_from_csv(file_path):
    enhancements = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, enhancement = row
            enhancements[key.lower()] = enhancement
    return enhancements

# Function to enhance the input prompt with enhancements from a CSV file
def enhance_prompt_with_csv(prompt, csv_file_path):
    enhancements = read_enhancements_from_csv(csv_file_path)
    for key, enhancement in enhancements.items():
        if key in prompt.lower():
            prompt += " " + enhancement
            break
    general_enhancements = "Ensure high resolution, sharp focus on key elements, and a balanced composition."
    prompt += " " + general_enhancements
    return prompt

# Function to convert speech to text
def speech_to_text():
    st.info("Listening... Speak something.")
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source, timeout=5)  # Record audio for 5 seconds
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Modified function to generate images and overlay text
def generate_images_with_text(input_text, num_images, resolution, text, font_name, font_size, font_placement, text_color, stroke, shadow):
    image_outputs = []
    for _ in range(num_images):
        random_number = random.randint(1, 10000)
        enhanced_prompt = enhance_prompt_with_csv(input_text,"Path of enhancements.csv file")  # Update the path as necessary
        prompt = f"{enhanced_prompt} {random_number}"
        
        # Insert your Hugging Face API key here
        api_key = "Your hugging face API key"
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
            if font_placement == 'Top':
                text_position = (10, 10)
            elif font_placement == 'Center':
                text_position = ((512 - font_size) / 2, (512 - font_size) / 2)
            elif font_placement == 'Bottom':
                text_position = (10, 512 - font_size)
        elif resolution == '1024x1024':
            image = image.resize((1024, 1024))
            if font_placement == 'Top':
                text_position = (10, 10)
            elif font_placement == 'Center':
                text_position = ((1024 - font_size) / 2, (1024 - font_size) / 2)
            elif font_placement == 'Bottom':
                text_position = (10, 1024 - font_size)
        
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.truetype(font_name, font_size)
        except IOError:
            st.error(f"Font file {font_name} not found.")
            return
        
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
    background-image: url("https://cdn.dribbble.com/users/214929/screenshots/4967879/media/2882629854d56075fd86d61ddee25975.gif");
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
st.title("ByteBenders: AI-Powered Poster Generator")

# Add voice command button for AI Prompt
if st.button("Voice Input (AI Prompt)"):
    spoken_text = speech_to_text()
    if spoken_text:
        st.text_area("AI Prompt", spoken_text)  # Display recognized text in prompt box
        input_text = spoken_text

# Text area for manual input of AI Prompt
input_text = st.text_area("AI Prompt", "Describe the scene you want to generate.")

num_images = st.number_input("Number of Images", min_value=1, max_value=10, value=1)
resolution = st.selectbox("Resolution", ["512x512", "1024x1024"])
text_overlay = st.text_area("Text to Overlay", "Hello, World!")

# Font placement buttons
font_placement = st.radio("Font Placement", ("Top", "Center", "Bottom"))

font_option = st.radio("Font Option", ("Default", "Import Font"))
if font_option == "Import Font":
    uploaded_font = st.file_uploader("Upload Font File (TTF)", type=["ttf"])
    if uploaded_font is not None:
        font_path = uploaded_font.name
        with open(font_path, "wb") as f:
            f.write(uploaded_font.getvalue())
else:
    font_path = "arial.ttf"  # Default font
font_size = st.slider("Font Size", 10, 100, 20)
text_color = st.color_picker("Text Color", "#FFFFFF")
stroke = st.checkbox("Add Stroke")
shadow = st.checkbox("Add Shadow")

# Generate button to trigger image generation
if st.button("Generate"):
    images = generate_images_with_text(input_text, num_images, resolution, text_overlay, font_path, font_size, font_placement, text_color, stroke, shadow)
    if images:
        # Display generated images
        for image in images:
            st.image(image, use_column_width=True)