import random
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Hugging Face API key
api_key = "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"

# Function to generate a random number between min and max (inclusive)
def get_random_number(min_val, max_val):
    return random.randint(min_val, max_val)

# Function to enhance the input prompt
def enhance_prompt(prompt):
    """
    Enhances the input prompt to be more descriptive for image generation.
    """
    enhancements = {
        "dance competition": "with energetic dancers in vibrant costumes against a dynamic, colorfully lit background, emphasizing motion and excitement. Include text overlay with the event title, date, and venue in a bold, readable font.",
        "hackathon": "featuring a creative and technological atmosphere with digital motifs, code snippets, and innovative symbols. Highlight teamwork and brainstorming sessions. Add event details in a modern, tech-inspired font.",
        "coding competition": "with a visually engaging representation of programming languages and algorithms, showcasing screens filled with code and participants deeply focused on problem-solving. Use a sleek, digital font for text.",
        "music festival": "showcasing a diverse array of musicians and bands on stage with a vibrant crowd in the foreground. Use bright lights and a festival atmosphere, and include various musical instruments in the scene.",
        "film festival": "including a cinematic aura with vintage film reels, a red carpet, and spotlights. Highlight the glamour and artistic nature of film-making. Details should be in an elegant, classic font.",
        "science fair": "displaying innovative experiments, engaging demonstrations, and curious minds at work. Use imagery that represents discovery and invention, with a focus on clarity and a scientific vibe for the text.",
        "book fair": "featuring rows of bookshelves, readers browsing, and a cozy, inviting atmosphere. Emphasize the variety and love of literature. Text should mimic the style of classic book typography.",
        "art exhibition": "with a gallery setting showcasing diverse artworks, sculptures, and visitors admiring the pieces. Use soft lighting and space to highlight the art, with minimalistic, elegant text.",
        "environmental conference": "emphasizing green and sustainable practices with imagery of nature, renewable energy, and eco-friendly innovations. Text overlays should reflect an organic, nature-inspired font.",
        "educational seminar": "highlighting the exchange of ideas with speakers, audience engagement, and educational materials. Focus on a professional and inspiring atmosphere. Use clear, authoritative text.",
        "sports tournament": "showcasing dynamic action shots of athletes, competitive spirit, and team colors. Include imagery of the sport's key elements and enthusiastic fans. Text should be bold and energetic.",
        "corporate event": "with a professional and sleek design showcasing networking, keynote speeches, and brand logos. Use a sophisticated, clean font for details.",
        "charity gala": "emphasizing elegance, philanthropy, and community involvement with imagery of a formal event setting, attendees in formal wear, and silent auctions. Use graceful, refined text.",
        "tech expo": "featuring cutting-edge technology, product demos, and innovative companies. Use futuristic design elements and a modern, accessible font.",
        "health and wellness retreat": "with serene landscapes, peaceful activities, and holistic health practices. Use imagery that promotes tranquility and well-being, with soft, soothing text.",
        "food festival": "showcasing a variety of culinary delights, chefs in action, and a bustling market atmosphere. Use appetizing visuals and a fun, inviting font.",
        "fashion show": "featuring runway models, the latest fashion trends, and designer brands. Emphasize style and glamour with sophisticated, chic text.",
        "literary conference": "highlighting authors, readings, and panel discussions with a focus on the written word. Use imagery that reflects creativity and intellect, with elegant, thoughtful text.",
        "entrepreneurship summit": "showcasing networking, startup pitches, and innovative ideas. Use a dynamic, inspirational design with a bold, forward-thinking font.",
        "photography workshop": "with hands-on demonstrations, photo critiques, and creative sessions. Use imagery that emphasizes visual storytelling and artistic expression, with clear, concise text.",
    }

    for key, enhancement in enhancements.items():
        if key in prompt.lower():
            prompt += " " + enhancement
            break

    prompt += " Ensure high resolution, sharp focus on key elements, and a balanced composition. The style should be realistic yet artistically compelling."
    return prompt
                
# Function to generate images
def generate_images(input_text, num_images, resolution):
    image_urls = []

    for i in range(num_images):
        # Generate a random number between 1 and 10000 and append it to the prompt
        random_number = get_random_number(1, 10000)
        enhanced_prompt = enhance_prompt(input_text)
        prompt = f"{enhanced_prompt} {random_number}"

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
        if resolution == '512x512':
            image = image.resize((512, 512))
        elif resolution == '1024x1024':
            image = image.resize((1024, 1024))
        image_urls.append(image)

    return image_urls

# Streamlit code

st.set_page_config(
    page_icon= "🤖",
    page_title= "ByteBenders Poster Creator"
)

st.title("ByteBenders Poster Creation App")
with st.expander("About the App"):
        st.write("This is a simple image generation app that uses Huggingface API to generate images from text prompts.")
        
st.subheader("Let your creativity enhance with AI")
input_prompt = st.text_input("What kind of poster you want to create?")

num_images = st.slider("Select number of images", 0, 10, 4)
resolution = st.selectbox("Select resolution", ['512x512', '1024x1024'])

if input_prompt is not None:
    if st.button("Generate Image"):
        enhanced_prompt = enhance_prompt(input_prompt)
        image_outputs = generate_images(enhanced_prompt, num_images, resolution)
        st.info("Generating images.....")
        st.success("Images Generated Successfully")
        for idx, image_output in enumerate(image_outputs):
            st.image(image_output, caption=f"Generated Image {idx+1} by Huggingface API")