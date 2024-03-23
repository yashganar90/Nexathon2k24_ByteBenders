import random
from PIL import Image
from io import BytesIO
import tkinter as tk
from tkinter import filedialog
from flask import Flask, request

app = Flask(__name__)

# Hugging Face API key
api_key = "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"
# Number of images to generate for each prompt
max_images = 4


# Function to generate a random number between min and max (inclusive)
def get_random_number(min_val, max_val):
    return random.randint(min_val, max_val)

                
@app.route('/your_endpoint', methods=['POST'])
def receive_prompt():
  prompt = request.form['prompt']
  # Process the received prompt (e.g., store it in a database)
  print(f'Received prompt: {prompt}')
  return 'Prompt received successfully!', 200

if __name__ == '__main__':
  app.run(debug=True)
  
# Function to generate images
def generate_images(input_text):
    loading_label.config(text="Loading...")
    loading_label.update()

    image_urls = []

    for i in range(max_images):
        # Generate a random number between 1 and 10000 and append it to the prompt
        random_number = get_random_number(1, 10000)
        prompt = f"{prompt} {random_number}"

        # API request to Hugging Face
        response = requests.post(
            "https://api-inference.huggingface.co/models/prompthero/openjourney",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={"inputs": prompt}
        )

        if not response.ok:
            print("Failed to generate image!")
            return

        image_data = response.content
        image = Image.open(BytesIO(image_data))
        image_urls.append(image)

    loading_label.config(text="")
    loading_label.update()

    return image_urls


# Function to save the image
def save_image(image, image_number):
    filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                             filetypes=[("JPEG files", "*.jpg")])
    if filename:
        image.save(filename)


# Function to handle generate button click event
def generate_button_click():
    user_prompt = user_prompt_entry.get()
    if user_prompt:
        images = generate_images(user_prompt)
        if images:
            for i, img in enumerate(images):
                img.show()
                save_image(img, i)



# GUI setup
root = tk.Tk()
root.title("Image Generation")
root.geometry("400x200")

user_prompt_label = tk.Label(root, text="Enter Prompt:")
user_prompt_label.pack()

user_prompt_entry = tk.Entry(root, width=50)
user_prompt_entry.pack()

generate_button = tk.Button(root, text="Generate Images", command=generate_button_click)
generate_button.pack()

loading_label = tk.Label(root, text="")
loading_label.pack()

root.mainloop()
