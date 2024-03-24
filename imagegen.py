import random
import requests
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
from flask import Flask, request,jsonify

app = Flask(__name__)

# Hugging Face API key
api_key = "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"
# Number of images to generate for each prompt
max_images = 4


# Function to generate a random number between min and max (inclusive)
def get_random_number(min_val, max_val):
    return random.randint(min_val, max_val)

                



  
# Function to generate images

# Function to generate images
def generate_images(input_text):
    image_urls = []

    for i in range(max_images):
        # Generate a random number between 1 and 10000 and append it to the prompt
        random_number = get_random_number(1, 10000)
        prompt = f"{input_text} {random_number}"

        # API request to Hugging Face
        response = requests.post(
            "https://api-inference.huggingface.co/models/prompthero/openjourney",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"inputs": prompt},
            
        )

        if not response.ok:
            print("Failed to generate image!")
            return []

        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image_urls.append(image)
    return image_urls


@app.route('/promt', methods=['POST'])
def receive_prompt():
    prompt = request.form['prompt']
    print(f'Received prompt: {prompt}')
    
    # Generate images
    image_urls = generate_images(prompt)
    
    # Convert images to base64 strings
    image_base64s = []
    for image_url in image_urls:
        with BytesIO() as output:
            image_url.save(output, format='JPEG')
            image_base64s.append(output.getvalue())

    return jsonify({'images': image_base64s}), 200

if __name__ == '__main__':
  app.run(debug=True)
  
# Function to save the image
def save_image(image, image_number):
    filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG files", "*.jpg")])
    if filename:
        image.save(filename)



