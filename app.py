import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import io

# 1. Configure the Page
st.set_page_config(page_title="AnyBudget AI Suite", page_icon="🎨")

# 2. Connect to the Brain (Gemini)
api_key = os.environ.get("GOOGLE_API_KEY") 
if not api_key:
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.info("Please add your GOOGLE_API_KEY to the secrets to continue.")
        st.stop()

genai.configure(api_key=api_key)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🤖 AI Tools")
mode = st.sidebar.radio("Select a tool:", ["Print Expert (Chat)", "Nano Banana (Images)"])

# ==========================================
# MODE 1: THE TEXT CHAT (Your existing bot)
# ==========================================
if mode == "Print Expert (Chat)":
    st.title("AnyBudget Assistant 💬")
    
    # Define Persona
    system_instruction = """
    You are the AnyBudget AI Assistant.
    You have vast knowledge, but if asked about printing, strictly follow:
    - Acceptable formats: PDF, AI, PSD, JPG.
    - Bleeds: 0.125 inches.
    - Resolution: 300 DPI minimum.
    For all other topics, be helpful and creative.
    """
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", 
        system_instruction=system_instruction
    )

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "model", "parts": "Hello! I am ready to help with print specs or general knowledge."}
        ]

    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message["parts"])

    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "parts": prompt})

        with st.chat_message("assistant"):
            try:
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["parts"]]} for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "parts": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

# ==========================================
# MODE 2: NANO BANANA (Image Generator)
# ==========================================
elif mode == "Nano Banana (Images)":
    st.title("Nano Banana Art Studio 🎨")
    st.write("Generate high-quality images using the `gemini-2.5-flash-image` model.")

    # Input for image prompt
    img_prompt = st.text_area("Describe the image you want:", height=100, placeholder="A futuristic printing press made of neon lights, cyberpunk style...")

    if st.button("Generate Image ✨"):
        if not img_prompt:
            st.warning("Please describe an image first!")
        else:
            with st.spinner("Nano Banana is painting..."):
                try:
                    # Connect to the Image Model
                    img_model = genai.GenerativeModel("gemini-2.5-flash-image")
                    
                    # Generate
                    response = img_model.generate_content(img_prompt)
                    
                    # Display Result
                    if response.parts:
                        # Streamlit handles the image display automatically from the response
                        st.image(response.parts[0].image, caption=img_prompt, use_column_width=True)
                    else:
                        st.error("The model didn't return an image. It might have been blocked by safety filters.")
                        
                except Exception as e:
                    st.error(f"Generation Error: {e}")
                    st.info("Note: If this model name fails, try 'gemini-pro-vision' or check if your key has image permissions.")
