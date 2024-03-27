import streamlit as st

# Title and description
background_image = """
<style>

[data-testid="stSidebarContent"] {
    background-image: linear-gradient(to bottom right, #290e47, #341c5c);
}

[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://www.siili.com/hubfs/siili-data_and_ai_design_sprint-hero_desktop-1920x1080.gif");
    background-size: cover;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    
}

[data-testid="stHeader"] {
background-color: rgba(0, 0, 0, 0);


</style>
"""

st.markdown(background_image, unsafe_allow_html=True)
st.title("KALAKRITI - A Powerful Tool for Poster Generation")
st.subheader("KALAKRITI is a revolutionary app designed to streamline the poster creation process, offering users a seamless experience from concept to completion. With its intuitive interface and advanced features, KALAKRITI empowers users to effortlessly bring their ideas to life in stunning visual representations.")
st.write("**Here are some key features that make our app stand out:**")

# Features list (replace with your app's unique features)
features = [
    "Smart Text-to-Image Conversion: KALAKRITI's cutting-edge technology allows users to simply input their text prompts, and the app intelligently translates them into captivating visual elements. KALAKRITI automates the process for you, saving time and effort while ensuring professional-quality results.",
    "Dynamic Templates and Customization: Whether you're creating a promotional poster, event announcement, or inspirational quote graphic, KALAKRITI provides the perfect starting point, with options to adjust colors, fonts, layout, and more.",
]
for feature in features:
    st.markdown(f"- {feature}")
    
if st.button("Get Started"):
    st.switch_page("pages/1_👩‍💻_App.py")
# Flag to track redirection

# Separate page content (assuming a file named "about.py")